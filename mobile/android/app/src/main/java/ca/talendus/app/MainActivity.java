package ca.talendus.app;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    public static final String APP_URL = "https://talendus.ca/m.html";
    public static final String CHANNEL_ID = "talendus";
    private static final int NOTIF_PERMISSION = 91;
    private WebView web;
    private int notifSeq = 1000;

    @SuppressLint({"SetJavaScriptEnabled", "AddJavascriptInterface"})
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ensureChannel();
        requestNotifPermission();
        web = new WebView(this);
        setContentView(web);
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setSupportZoom(false);
        settings.setMediaPlaybackRequiresUserGesture(false);
        String ua = settings.getUserAgentString();
        settings.setUserAgentString((ua == null ? "" : ua) + " TalendusApp/1.0");
        web.addJavascriptInterface(new TalendusNative(), "TalendusNative");
        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(PermissionRequest request) {
                runOnUiThread(() -> request.grant(request.getResources()));
            }
        });
        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                String scheme = uri.getScheme() == null ? "" : uri.getScheme();
                String host = uri.getHost() == null ? "" : uri.getHost();
                String path = uri.getPath() == null ? "/" : uri.getPath();
                if (scheme.equals("tel") || scheme.equals("mailto") || host.contains("wa.me") || scheme.equals("sms")) {
                    startActivity(new Intent(Intent.ACTION_VIEW, uri));
                    return true;
                }
                if (host.contains("talendus.ca") && (
                    path.equals("/") || path.equals("/index.html") || path.equals("/app.html")
                    || path.equals("/en/") || path.equals("/en/index.html") || path.equals("/en/app.html")
                )) {
                    view.loadUrl(APP_URL);
                    return true;
                }
                return false;
            }
        });
        String start = urlFromIntent(getIntent());
        web.loadUrl(start != null ? start : APP_URL);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        String url = urlFromIntent(intent);
        if (url != null && web != null) {
            web.loadUrl(url);
        }
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) {
            web.goBack();
            return;
        }
        super.onBackPressed();
    }

    private String urlFromIntent(Intent intent) {
        if (intent == null) {
            return null;
        }
        String extra = intent.getStringExtra("href");
        if (extra != null && extra.length() > 0) {
            if (extra.startsWith("http")) {
                return extra;
            }
            if (extra.startsWith("/")) {
                return "https://talendus.ca" + extra;
            }
            if (extra.startsWith("#")) {
                return APP_URL + extra;
            }
            return APP_URL + "#/" + extra.replaceFirst("^/+", "");
        }
        Uri data = intent.getData();
        return data != null ? data.toString() : null;
    }

    private void ensureChannel() {
        if (Build.VERSION.SDK_INT < 26) {
            return;
        }
        NotificationManager manager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
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

    private void requestNotifPermission() {
        if (Build.VERSION.SDK_INT < 33) {
            return;
        }
        if (checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED) {
            return;
        }
        requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, NOTIF_PERMISSION);
    }

    private boolean notificationsAllowed() {
        NotificationManager manager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        if (manager == null) {
            return false;
        }
        if (Build.VERSION.SDK_INT >= 24 && !manager.areNotificationsEnabled()) {
            return false;
        }
        if (Build.VERSION.SDK_INT >= 33) {
            return checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED;
        }
        return true;
    }

    private void postNotification(String title, String body, String href) {
        if (!notificationsAllowed()) {
            requestNotifPermission();
            return;
        }
        NotificationManager manager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        if (manager == null) {
            return;
        }
        String safeTitle = title == null || title.isEmpty() ? "Talendus" : title;
        String safeBody = body == null ? "" : body;
        String safeHref = href == null || href.isEmpty() ? "/m.html#/notifs" : href;
        int id = notifSeq++;
        Intent open = new Intent(this, MainActivity.class);
        open.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP | Intent.FLAG_ACTIVITY_CLEAR_TOP);
        open.putExtra("href", safeHref);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 23) {
            flags |= PendingIntent.FLAG_IMMUTABLE;
        }
        PendingIntent pending = PendingIntent.getActivity(this, id, open, flags);
        Notification.Builder builder;
        if (Build.VERSION.SDK_INT >= 26) {
            builder = new Notification.Builder(this, CHANNEL_ID);
        } else {
            builder = new Notification.Builder(this);
        }
        builder.setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle(safeTitle)
            .setContentText(safeBody)
            .setAutoCancel(true)
            .setContentIntent(pending);
        if (Build.VERSION.SDK_INT >= 21) {
            builder.setColor(0xFFFF6B00);
            builder.setStyle(new Notification.BigTextStyle().bigText(safeBody));
        }
        manager.notify(id, builder.build());
    }

    public class TalendusNative {
        @JavascriptInterface
        public void showNotification(String title, String body, String href) {
            runOnUiThread(() -> postNotification(title, body, href));
        }

        @JavascriptInterface
        public void requestPermission() {
            runOnUiThread(MainActivity.this::requestNotifPermission);
        }

        @JavascriptInterface
        public boolean notificationsEnabled() {
            return notificationsAllowed();
        }
    }
}
