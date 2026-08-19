package ca.talendus.app;

import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Build;
import android.os.SystemClock;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public final class NotifPoller {
    public static final String CHANNEL_ID = "talendus";
    private static final String PREFS = "talendus_native";
    private static final String KEY_TOKEN = "access_token";
    private static final String KEY_SEEN = "seen_ids";
    private static final String API = "https://talendus.ca/api/notifications?unread=true";
    private static final int ALARM_ID = 71;

    private NotifPoller() {}

    public static SharedPreferences prefs(Context ctx) {
        return ctx.getApplicationContext().getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }

    public static void setToken(Context ctx, String token) {
        prefs(ctx).edit().putString(KEY_TOKEN, token == null ? "" : token).apply();
        if (token != null && !token.isEmpty()) {
            schedule(ctx);
            pollAsync(ctx);
        }
    }

    public static void clearToken(Context ctx) {
        prefs(ctx).edit().remove(KEY_TOKEN).apply();
    }

    public static void schedule(Context ctx) {
        AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
        if (am == null) {
            return;
        }
        Intent intent = new Intent(ctx, NotifAlarmReceiver.class);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 23) {
            flags |= PendingIntent.FLAG_IMMUTABLE;
        }
        PendingIntent pending = PendingIntent.getBroadcast(ctx, ALARM_ID, intent, flags);
        am.setRepeating(
            AlarmManager.ELAPSED_REALTIME_WAKEUP,
            SystemClock.elapsedRealtime() + 15000,
            15 * 60 * 1000L,
            pending
        );
    }

    public static void pollAsync(Context ctx) {
        Context app = ctx.getApplicationContext();
        new Thread(() -> poll(app), "talendus-notif").start();
    }

    public static void poll(Context ctx) {
        String token = prefs(ctx).getString(KEY_TOKEN, "");
        if (token == null || token.isEmpty()) {
            return;
        }
        HttpURLConnection conn = null;
        try {
            conn = (HttpURLConnection) new URL(API).openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");
            conn.setRequestProperty("Authorization", "Bearer " + token);
            conn.setConnectTimeout(12000);
            conn.setReadTimeout(12000);
            int code = conn.getResponseCode();
            if (code == 401) {
                return;
            }
            if (code < 200 || code >= 300) {
                return;
            }
            String body = readStream(conn.getInputStream());
            JSONObject root = new JSONObject(body);
            JSONArray data = root.optJSONArray("data");
            if (data == null) {
                return;
            }
            for (int i = 0; i < data.length(); i++) {
                JSONObject row = data.optJSONObject(i);
                if (row == null) {
                    continue;
                }
                post(
                    ctx,
                    row.optString("title", "Talendus"),
                    row.optString("message", ""),
                    appHref(row.optString("href", "")),
                    row.optString("id", "")
                );
            }
        } catch (Exception ignored) {
        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }
    }

    public static void ensureChannel(Context ctx) {
        if (Build.VERSION.SDK_INT < 26) {
            return;
        }
        NotificationManager manager = (NotificationManager) ctx.getSystemService(Context.NOTIFICATION_SERVICE);
        if (manager == null) {
            return;
        }
        NotificationChannel channel = new NotificationChannel(
            CHANNEL_ID,
            "Talendus",
            NotificationManager.IMPORTANCE_HIGH
        );
        channel.setDescription("Suivis Talendus");
        channel.enableVibration(true);
        channel.setLightColor(Color.parseColor("#FF6B00"));
        manager.createNotificationChannel(channel);
    }

    public static void post(Context ctx, String title, String body, String href) {
        post(ctx, title, body, href, "");
    }

    public static void post(Context ctx, String title, String body, String href, String notifId) {
        ensureChannel(ctx);
        NotificationManager manager = (NotificationManager) ctx.getSystemService(Context.NOTIFICATION_SERVICE);
        if (manager == null) {
            return;
        }
        if (Build.VERSION.SDK_INT >= 24 && !manager.areNotificationsEnabled()) {
            return;
        }
        String safeTitle = title == null || title.isEmpty() ? "Talendus" : title;
        String safeBody = body == null ? "" : body;
        String safeHref = href == null || href.isEmpty() ? "/m.html#/notifs" : href;
        String key = notifId != null && !notifId.isEmpty() ? notifId : (safeTitle + "\n" + safeBody);
        List<String> seen = seenIds(ctx);
        if (seen.contains(key)) {
            return;
        }
        seen.add(key);
        storeSeen(ctx, seen);
        int id = Math.abs(key.hashCode());
        if (id == 0 || id == Integer.MIN_VALUE) {
            id = 1;
        }
        Intent open = new Intent(ctx, MainActivity.class);
        open.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP | Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);
        open.putExtra("href", safeHref);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 23) {
            flags |= PendingIntent.FLAG_IMMUTABLE;
        }
        PendingIntent pending = PendingIntent.getActivity(ctx, id, open, flags);
        Notification.Builder builder;
        if (Build.VERSION.SDK_INT >= 26) {
            builder = new Notification.Builder(ctx, CHANNEL_ID);
        } else {
            builder = new Notification.Builder(ctx);
        }
        builder.setSmallIcon(android.R.drawable.ic_popup_reminder)
            .setContentTitle(safeTitle)
            .setContentText(safeBody)
            .setAutoCancel(true)
            .setContentIntent(pending);
        if (Build.VERSION.SDK_INT >= 21) {
            builder.setColor(0xFFFF6B00);
            builder.setStyle(new Notification.BigTextStyle().bigText(safeBody));
            builder.setPriority(Notification.PRIORITY_HIGH);
        }
        manager.notify(id, builder.build());
    }

    static String appHref(String href) {
        if (href == null || href.isEmpty()) {
            return "/m.html#/notifs";
        }
        if (href.startsWith("/m.html")) {
            return href;
        }
        String hash = "";
        int hashAt = href.indexOf('#');
        if (hashAt >= 0) {
            hash = href.substring(hashAt + 1);
        }
        if (hash.startsWith("/")) {
            hash = hash.substring(1);
        }
        if (hash.isEmpty()) {
            return "/m.html#/notifs";
        }
        if (hash.startsWith("dashboard")) {
            hash = "home" + hash.substring("dashboard".length());
        } else if (hash.startsWith("documents")) {
            hash = "cv" + hash.substring("documents".length());
        } else if (hash.startsWith("applications")) {
            hash = "apps" + hash.substring("applications".length());
        } else if (hash.startsWith("application")) {
            hash = "app" + hash.substring("application".length());
        }
        return "/m.html#/" + hash;
    }

    private static List<String> seenIds(Context ctx) {
        String raw = prefs(ctx).getString(KEY_SEEN, "");
        List<String> out = new ArrayList<>();
        if (raw == null || raw.isEmpty()) {
            return out;
        }
        for (String part : raw.split(",")) {
            if (!part.isEmpty()) {
                out.add(part);
            }
        }
        return out;
    }

    private static void storeSeen(Context ctx, List<String> ids) {
        int start = Math.max(0, ids.size() - 80);
        StringBuilder sb = new StringBuilder();
        for (int i = start; i < ids.size(); i++) {
            if (sb.length() > 0) {
                sb.append(',');
            }
            sb.append(ids.get(i));
        }
        prefs(ctx).edit().putString(KEY_SEEN, sb.toString()).apply();
    }

    private static String readStream(InputStream in) throws Exception {
        BufferedReader reader = new BufferedReader(new InputStreamReader(in));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line);
        }
        return sb.toString();
    }
}
