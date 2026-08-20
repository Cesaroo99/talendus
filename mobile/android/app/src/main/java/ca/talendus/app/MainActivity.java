package ca.talendus.app;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ClipData;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.webkit.JavascriptInterface;
import android.webkit.PermissionRequest;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends Activity {
    public static final String APP_URL = "https://talendus.ca/m.html";
    private static final int NOTIF_PERMISSION = 91;
    private static final int MEDIA_PERMISSION = 92;
    private static final int FILE_CHOOSER = 93;
    private WebView web;
    private PermissionRequest pendingWebPermission;
    private static ValueCallback<Uri[]> fileCallback;
    private final Handler ticker = new Handler(Looper.getMainLooper());
    private final Runnable pollTick = new Runnable() {
        @Override
        public void run() {
            NotifPoller.pollAsync(MainActivity.this);
            ticker.postDelayed(this, 20000);
        }
    };

    @SuppressLint({"SetJavaScriptEnabled", "AddJavascriptInterface"})
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        NotifPoller.ensureChannel(this);
        requestNotifPermission();
        NotifPoller.schedule(this);
        web = new WebView(this);
        setContentView(web);
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setSupportZoom(false);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        String ua = settings.getUserAgentString();
        settings.setUserAgentString((ua == null ? "" : ua) + " TalendusApp/1.5");
        web.addJavascriptInterface(new TalendusNative(), "TalendusNative");
        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(PermissionRequest request) {
                runOnUiThread(() -> grantWebMedia(request));
            }

            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
                if (fileCallback != null) {
                    fileCallback.onReceiveValue(null);
                }
                fileCallback = filePathCallback;
                try {
                    startActivityForResult(openDocumentIntent(fileChooserParams), FILE_CHOOSER);
                } catch (Exception ignored) {
                    try {
                        startActivityForResult(Intent.createChooser(getContentIntent(fileChooserParams), "Talendus"), FILE_CHOOSER);
                    } catch (Exception ignoredToo) {
                        fileCallback.onReceiveValue(null);
                        fileCallback = null;
                        return false;
                    }
                }
                return true;
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
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode != FILE_CHOOSER) {
            return;
        }
        ValueCallback<Uri[]> callback = fileCallback;
        fileCallback = null;
        if (callback == null) {
            return;
        }
        Uri[] uris = WebChromeClient.FileChooserParams.parseResult(resultCode, data);
        if (uris == null || uris.length == 0) {
            uris = fileChooserUris(resultCode, data);
        }
        if (uris != null) {
            for (Uri uri : uris) {
                if (uri == null) {
                    continue;
                }
                try {
                    getContentResolver().takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION);
                } catch (Exception ignored) {
                }
            }
        }
        callback.onReceiveValue(uris);
    }

    @Override
    protected void onResume() {
        super.onResume();
        ticker.removeCallbacks(pollTick);
        ticker.post(pollTick);
        NotifPoller.pollAsync(this);
    }

    @Override
    protected void onPause() {
        ticker.removeCallbacks(pollTick);
        super.onPause();
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

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == MEDIA_PERMISSION && pendingWebPermission != null) {
            pendingWebPermission.grant(pendingWebPermission.getResources());
            pendingWebPermission = null;
        }
        if (requestCode == NOTIF_PERMISSION) {
            NotifPoller.pollAsync(this);
        }
    }

    private void grantWebMedia(PermissionRequest request) {
        pendingWebPermission = request;
        List<String> needed = new ArrayList<>();
        for (String resource : request.getResources()) {
            if (PermissionRequest.RESOURCE_VIDEO_CAPTURE.equals(resource)
                && checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                needed.add(Manifest.permission.CAMERA);
            }
            if (PermissionRequest.RESOURCE_AUDIO_CAPTURE.equals(resource)
                && checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                needed.add(Manifest.permission.RECORD_AUDIO);
            }
        }
        if (needed.isEmpty()) {
            request.grant(request.getResources());
            pendingWebPermission = null;
            return;
        }
        requestPermissions(needed.toArray(new String[0]), MEDIA_PERMISSION);
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

    private Intent openDocumentIntent(WebChromeClient.FileChooserParams params) {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        fillFileIntent(intent, params);
        intent.addFlags(Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
        return intent;
    }

    private Intent getContentIntent(WebChromeClient.FileChooserParams params) {
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        fillFileIntent(intent, params);
        return intent;
    }

    private static void fillFileIntent(Intent intent, WebChromeClient.FileChooserParams params) {
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType(imagesOnly(params) ? "image/*" : "*/*");
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, params != null
            && params.getMode() == WebChromeClient.FileChooserParams.MODE_OPEN_MULTIPLE);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
    }

    private static boolean imagesOnly(WebChromeClient.FileChooserParams params) {
        if (params == null) {
            return false;
        }
        String[] types = params.getAcceptTypes();
        if (types == null || types.length == 0) {
            return false;
        }
        boolean sawImage = false;
        for (String raw : types) {
            if (raw == null || raw.isEmpty() || raw.equals("*/*")) {
                return false;
            }
            String type = raw.toLowerCase();
            if (type.startsWith(".")) {
                return false;
            }
            if (type.startsWith("image/")) {
                sawImage = true;
            } else {
                return false;
            }
        }
        return sawImage;
    }

    private static Uri[] fileChooserUris(int resultCode, Intent data) {
        if (resultCode != RESULT_OK || data == null) {
            return null;
        }
        ClipData clip = data.getClipData();
        if (clip != null && clip.getItemCount() > 0) {
            Uri[] uris = new Uri[clip.getItemCount()];
            for (int i = 0; i < clip.getItemCount(); i++) {
                uris[i] = clip.getItemAt(i).getUri();
            }
            return uris;
        }
        Uri uri = data.getData();
        return uri != null ? new Uri[]{uri} : null;
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

    private void requestMediaPermission() {
        List<String> needed = new ArrayList<>();
        if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            needed.add(Manifest.permission.CAMERA);
        }
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            needed.add(Manifest.permission.RECORD_AUDIO);
        }
        if (!needed.isEmpty()) {
            requestPermissions(needed.toArray(new String[0]), MEDIA_PERMISSION);
        }
    }

    private boolean notificationsAllowed() {
        android.app.NotificationManager manager =
            (android.app.NotificationManager) getSystemService(NOTIFICATION_SERVICE);
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

    public class TalendusNative {
        @JavascriptInterface
        public void showNotification(String title, String body, String href) {
            runOnUiThread(() -> NotifPoller.post(MainActivity.this, title, body, href));
        }

        @JavascriptInterface
        public void requestPermission() {
            runOnUiThread(MainActivity.this::requestNotifPermission);
        }

        @JavascriptInterface
        public void requestMedia() {
            runOnUiThread(MainActivity.this::requestMediaPermission);
        }

        @JavascriptInterface
        public void setAuthToken(String token) {
            NotifPoller.setToken(MainActivity.this, token);
        }

        @JavascriptInterface
        public void clearAuth() {
            NotifPoller.clearToken(MainActivity.this);
        }

        @JavascriptInterface
        public boolean notificationsEnabled() {
            return notificationsAllowed();
        }
    }
}
