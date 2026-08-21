package ca.talendus.app;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.DownloadManager;
import android.content.ClipData;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.database.Cursor;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.provider.MediaStore;
import android.provider.OpenableColumns;
import android.util.Base64;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
import android.webkit.MimeTypeMap;
import android.webkit.PermissionRequest;
import android.webkit.URLUtil;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends Activity {
    public static final String APP_URL = "https://talendus.ca/m.html";
    private static final int NOTIF_PERMISSION = 91;
    private static final int MEDIA_PERMISSION = 92;
    private static final int FILE_CHOOSER = 93;
    private static final int NATIVE_PICK = 94;
    private static final int DL_PERMISSION = 95;
    private WebView web;
    private String webUserAgent = "";
    private String pendingDlUrl;
    private String pendingDlName;
    private String pendingDlToken;
    private PermissionRequest pendingWebPermission;
    private static ValueCallback<Uri[]> fileCallback;
    private String nativePickId;
    private String nativePickKind;
    private String nativePickToken;
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
        webUserAgent = (ua == null ? "" : ua) + " TalendusApp/1.8";
        settings.setUserAgentString(webUserAgent);
        CookieManager cookies = CookieManager.getInstance();
        cookies.setAcceptCookie(true);
        cookies.setAcceptThirdPartyCookies(web, true);
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
                    startActivityForResult(Intent.createChooser(getContentIntent(fileChooserParams), "Talendus"), FILE_CHOOSER);
                } catch (Exception ignored) {
                    try {
                        startActivityForResult(openDocumentIntent(fileChooserParams), FILE_CHOOSER);
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
                if (isDownloadPath(path)) {
                    enqueueDownload(uri.toString(), filenameFrom(path, uri.getLastPathSegment()), NotifPoller.token(MainActivity.this));
                    return true;
                }
                return false;
            }
        });
        web.setDownloadListener((url, userAgent, contentDisposition, mimeType, contentLength) -> {
            String name = URLUtil.guessFileName(url, contentDisposition, mimeType);
            enqueueDownload(url, name, NotifPoller.token(MainActivity.this));
        });
        String start = urlFromIntent(getIntent());
        web.loadUrl(start != null ? start : APP_URL);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == NATIVE_PICK) {
            deliverNativeFiles(resultCode, data);
            return;
        }
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
        if (requestCode == DL_PERMISSION) {
            String url = pendingDlUrl;
            String name = pendingDlName;
            String token = pendingDlToken;
            pendingDlUrl = pendingDlName = pendingDlToken = null;
            if (url != null && grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                enqueueDownload(url, name, token);
            } else if (url != null) {
                Toast.makeText(this, "Téléchargement impossible.", Toast.LENGTH_LONG).show();
            }
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

    private static boolean isDownloadPath(String path) {
        if (path == null) {
            return false;
        }
        return path.startsWith("/download/")
            || path.startsWith("/assets/app/")
            || path.endsWith("/file")
            || path.endsWith("/pdf");
    }

    private static String filenameFrom(String path, String fallback) {
        if (fallback != null && !fallback.isEmpty() && !fallback.equals("file") && fallback.contains(".")) {
            return fallback;
        }
        if (path != null) {
            if (path.endsWith("/pdf") || path.contains("/pdf")) {
                return path.contains("invoice") || path.contains("facture") ? "facture.pdf" : "document.pdf";
            }
            int slash = path.lastIndexOf('/');
            if (slash >= 0 && slash < path.length() - 1) {
                String last = path.substring(slash + 1);
                if (!last.isEmpty() && !last.equals("file") && last.contains(".")) {
                    return last;
                }
            }
        }
        return (fallback == null || fallback.isEmpty() || "file".equals(fallback)) ? "document" : fallback;
    }

    private boolean ensureStoragePermission() {
        if (Build.VERSION.SDK_INT >= 29) {
            return true;
        }
        if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
            return true;
        }
        requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, DL_PERMISSION);
        return false;
    }

    private static String safeFilename(String name) {
        String clean = name == null ? "" : name.replaceAll("[\\\\/:*?\"<>|]", "_").trim();
        return clean.isEmpty() ? "document" : clean;
    }

    private static String mimeFromName(String filename) {
        String name = filename == null ? "" : filename.toLowerCase();
        int dot = name.lastIndexOf('.');
        String ext = dot >= 0 ? name.substring(dot + 1) : "";
        String mime = MimeTypeMap.getSingleton().getMimeTypeFromExtension(ext);
        if (mime != null && !mime.isEmpty()) {
            return mime;
        }
        if ("pdf".equals(ext)) return "application/pdf";
        if ("doc".equals(ext)) return "application/msword";
        if ("docx".equals(ext)) return "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
        if ("png".equals(ext)) return "image/png";
        if ("jpg".equals(ext) || "jpeg".equals(ext)) return "image/jpeg";
        return "application/octet-stream";
    }

    private void enqueueDownload(String url, String filename, String token) {
        if (url == null || url.isEmpty() || url.startsWith("blob:") || url.startsWith("data:")) {
            return;
        }
        if (url.startsWith("/")) {
            url = "https://talendus.ca" + url;
        }
        String name = safeFilename(filenameFrom(url, filename));
        if (!ensureStoragePermission()) {
            pendingDlUrl = url;
            pendingDlName = name;
            pendingDlToken = token;
            return;
        }
        final String finalUrl = url;
        final String finalName = name;
        final String finalToken = token == null ? "" : token;
        new Thread(() -> {
            if (saveAuthenticatedFile(finalUrl, finalName, finalToken)) {
                return;
            }
            runOnUiThread(() -> downloadViaManager(finalUrl, finalName, finalToken));
        }, "talendus-dl").start();
    }

    private boolean saveAuthenticatedFile(String url, String filename, String token) {
        HttpURLConnection conn = null;
        InputStream in = null;
        OutputStream out = null;
        Uri pendingUri = null;
        File destFile = null;
        try {
            conn = (HttpURLConnection) new URL(url).openConnection();
            conn.setInstanceFollowRedirects(true);
            conn.setConnectTimeout(20000);
            conn.setReadTimeout(60000);
            conn.setRequestProperty("Accept", "*/*");
            if (webUserAgent != null && !webUserAgent.isEmpty()) {
                conn.setRequestProperty("User-Agent", webUserAgent);
            }
            if (token != null && !token.isEmpty()) {
                conn.setRequestProperty("Authorization", "Bearer " + token);
            }
            String cookie = CookieManager.getInstance().getCookie(url);
            if (cookie != null && !cookie.isEmpty()) {
                conn.setRequestProperty("Cookie", cookie);
            }
            int code = conn.getResponseCode();
            if (code >= 400) {
                return false;
            }
            String mime = conn.getContentType();
            if (mime != null && mime.contains(";")) {
                mime = mime.split(";")[0].trim();
            }
            if (mime == null || mime.isEmpty() || "application/octet-stream".equals(mime)) {
                mime = mimeFromName(filename);
            }
            if (mime.contains("text/html")) {
                return false;
            }
            in = conn.getInputStream();
            if (Build.VERSION.SDK_INT >= 29) {
                ContentValues values = new ContentValues();
                values.put(MediaStore.Downloads.DISPLAY_NAME, filename);
                values.put(MediaStore.Downloads.MIME_TYPE, mime);
                values.put(MediaStore.Downloads.IS_PENDING, 1);
                pendingUri = getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values);
                if (pendingUri == null) {
                    return false;
                }
                out = getContentResolver().openOutputStream(pendingUri);
            } else {
                File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
                if (dir == null || (!dir.exists() && !dir.mkdirs())) {
                    return false;
                }
                destFile = new File(dir, filename);
                out = new FileOutputStream(destFile);
            }
            if (out == null) {
                return false;
            }
            byte[] buf = new byte[8192];
            int n;
            long total = 0;
            while ((n = in.read(buf)) > 0) {
                out.write(buf, 0, n);
                total += n;
            }
            out.flush();
            if (total == 0) {
                return false;
            }
            if (Build.VERSION.SDK_INT >= 29 && pendingUri != null) {
                ContentValues done = new ContentValues();
                done.put(MediaStore.Downloads.IS_PENDING, 0);
                getContentResolver().update(pendingUri, done, null, null);
            }
            runOnUiThread(() -> Toast.makeText(this, "Fichier enregistré dans Téléchargements.", Toast.LENGTH_SHORT).show());
            return true;
        } catch (Exception ignored) {
            if (pendingUri != null && Build.VERSION.SDK_INT >= 29) {
                try {
                    getContentResolver().delete(pendingUri, null, null);
                } catch (Exception ignoredToo) {}
            }
            if (destFile != null && destFile.exists()) {
                destFile.delete();
            }
            return false;
        } finally {
            try { if (out != null) out.close(); } catch (Exception ignored) {}
            try { if (in != null) in.close(); } catch (Exception ignored) {}
            if (conn != null) conn.disconnect();
        }
    }

    private void downloadViaManager(String url, String filename, String token) {
        try {
            DownloadManager manager = (DownloadManager) getSystemService(DOWNLOAD_SERVICE);
            if (manager == null) {
                Toast.makeText(this, "Téléchargement impossible.", Toast.LENGTH_LONG).show();
                return;
            }
            DownloadManager.Request request = new DownloadManager.Request(Uri.parse(url));
            if (token != null && !token.isEmpty()) {
                request.addRequestHeader("Authorization", "Bearer " + token);
            }
            String cookie = CookieManager.getInstance().getCookie(url);
            if (cookie != null && !cookie.isEmpty()) {
                request.addRequestHeader("Cookie", cookie);
            }
            if (webUserAgent != null && !webUserAgent.isEmpty()) {
                request.addRequestHeader("User-Agent", webUserAgent);
            }
            request.setTitle(filename);
            request.setDescription("Talendus");
            request.allowScanningByMediaScanner();
            request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
            request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, filename);
            request.setAllowedOverMetered(true);
            request.setAllowedOverRoaming(true);
            manager.enqueue(request);
            Toast.makeText(this, "Fichier enregistré dans Téléchargements.", Toast.LENGTH_SHORT).show();
        } catch (Exception ignored) {
            try {
                startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
            } catch (Exception failed) {
                Toast.makeText(this, "Téléchargement impossible.", Toast.LENGTH_LONG).show();
            }
        }
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

    private void startNativePick(String requestId, boolean multiple, boolean imagesOnly, String kind, String token) {
        nativePickId = requestId;
        nativePickKind = kind;
        nativePickToken = token;
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType(imagesOnly ? "image/*" : "*/*");
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, multiple);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        try {
            startActivityForResult(Intent.createChooser(intent, "Talendus"), NATIVE_PICK);
        } catch (Exception ignored) {
            try {
                Intent open = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                open.addCategory(Intent.CATEGORY_OPENABLE);
                open.setType(imagesOnly ? "image/*" : "*/*");
                open.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, multiple);
                open.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                startActivityForResult(open, NATIVE_PICK);
            } catch (Exception failed) {
                evalNativeFiles(requestId, new JSONArray(), "Impossible d’ouvrir le sélecteur de fichiers.");
            }
        }
    }

    private void deliverNativeFiles(int resultCode, Intent data) {
        final String id = nativePickId;
        final String kind = nativePickKind;
        final String token = nativePickToken;
        nativePickId = null;
        nativePickKind = null;
        nativePickToken = null;
        if (id == null) {
            return;
        }
        if (resultCode != RESULT_OK || data == null) {
            evalNativeFiles(id, new JSONArray(), null);
            return;
        }
        final Uri[] uris = fileChooserUris(RESULT_OK, data);
        if (isDirectUploadKind(kind)) {
            uploadNativeFiles(id, uris, kind, token);
            return;
        }
        new Thread(() -> {
            JSONArray rows = new JSONArray();
            String error = null;
            try {
                if (uris != null) {
                    for (Uri uri : uris) {
                        if (uri != null) {
                            rows.put(readUriAsJson(uri));
                        }
                    }
                }
            } catch (Exception e) {
                error = "Impossible de lire le fichier.";
            }
            final JSONArray out = rows;
            final String err = error;
            runOnUiThread(() -> evalNativeFiles(id, out, err));
        }).start();
    }

    private static boolean isDirectUploadKind(String kind) {
        return "cv".equals(kind) || "doc".equals(kind) || "avatar".equals(kind);
    }

    private void uploadNativeFiles(String id, Uri[] uris, String kind, String token) {
        new Thread(() -> {
            if (uris == null || uris.length == 0) {
                runOnUiThread(() -> evalNativeFiles(id, new JSONArray(), null));
                return;
            }
            String error = null;
            try {
                for (Uri uri : uris) {
                    if (uri == null) {
                        continue;
                    }
                    String fail = postStoredFile(uri, kind, token);
                    if (fail != null) {
                        error = fail;
                        break;
                    }
                }
            } catch (Exception e) {
                error = "Impossible d’envoyer le fichier.";
            }
            final String err = error;
            runOnUiThread(() -> evalUploadDone(id, err == null, err));
        }, "talendus-ul").start();
    }

    private void evalUploadDone(String id, boolean ok, String message) {
        if (web == null) {
            return;
        }
        String msgArg = message == null ? "null" : JSONObject.quote(message);
        web.evaluateJavascript(
            "window.__tnUploadDone&&window.__tnUploadDone(" + JSONObject.quote(id) + "," +
                (ok ? "true" : "false") + "," + msgArg + ")",
            null
        );
    }

    private String postStoredFile(Uri uri, String kind, String token) {
        try {
            try {
                getContentResolver().takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION);
            } catch (Exception ignored) {}
            byte[] data = readUriBytes(uri, 8 * 1024 * 1024);
            String name = displayName(uri);
            String mime = getContentResolver().getType(uri);
            if (mime == null || mime.isEmpty()) {
                mime = mimeFromName(name);
            }
            if (name == null || name.isEmpty() || name.equals("document")) {
                name = "cv".equals(kind) ? "cv.pdf" : ("avatar".equals(kind) ? "photo.jpg" : "document.pdf");
                if (mime.contains("pdf")) name = name.replaceAll("\\.[^.]+$", ".pdf");
                else if (mime.contains("jpeg") || mime.contains("jpg")) name = name.replaceAll("\\.[^.]+$", ".jpg");
                else if (mime.contains("png")) name = name.replaceAll("\\.[^.]+$", ".png");
                else if (mime.contains("wordprocessingml")) name = name.replaceAll("\\.[^.]+$", ".docx");
            }
            String path;
            String extraKind = null;
            if ("cv".equals(kind)) {
                path = "/api/candidates/me/resume";
            } else if ("doc".equals(kind)) {
                path = "/api/documents";
                extraKind = "other";
            } else if ("avatar".equals(kind)) {
                path = "/api/users/me/avatar";
            } else {
                return "Envoi impossible.";
            }
            String auth = (token != null && !token.isEmpty()) ? token : NotifPoller.token(this);
            return postMultipart("https://talendus.ca" + path, auth, data, name, mime, extraKind);
        } catch (Exception e) {
            return "Impossible d’envoyer le fichier.";
        }
    }

    private String postMultipart(String url, String token, byte[] data, String filename, String mime, String extraKind) {
        HttpURLConnection conn = null;
        try {
            String boundary = "talendus" + System.currentTimeMillis();
            String safeName = (filename == null ? "document" : filename).replace("\"", "").replace("\r", "").replace("\n", "");
            String safeMime = (mime == null || mime.isEmpty()) ? "application/octet-stream" : mime;
            conn = (HttpURLConnection) new URL(url).openConnection();
            conn.setConnectTimeout(20000);
            conn.setReadTimeout(60000);
            conn.setDoOutput(true);
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Accept", "application/json");
            conn.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);
            if (webUserAgent != null && !webUserAgent.isEmpty()) {
                conn.setRequestProperty("User-Agent", webUserAgent);
            }
            if (token != null && !token.isEmpty()) {
                conn.setRequestProperty("Authorization", "Bearer " + token);
            }
            String cookie = CookieManager.getInstance().getCookie(url);
            if (cookie != null && !cookie.isEmpty()) {
                conn.setRequestProperty("Cookie", cookie);
            }
            OutputStream out = conn.getOutputStream();
            if (extraKind != null) {
                writeFormField(out, boundary, "kind", extraKind);
            }
            out.write(("--" + boundary + "\r\n").getBytes(StandardCharsets.UTF_8));
            out.write(("Content-Disposition: form-data; name=\"file\"; filename=\"" + safeName + "\"\r\n").getBytes(StandardCharsets.UTF_8));
            out.write(("Content-Type: " + safeMime + "\r\n\r\n").getBytes(StandardCharsets.UTF_8));
            out.write(data);
            out.write(("\r\n--" + boundary + "--\r\n").getBytes(StandardCharsets.UTF_8));
            out.flush();
            int code = conn.getResponseCode();
            InputStream resp = code >= 400 ? conn.getErrorStream() : conn.getInputStream();
            String body = readStream(resp);
            if (code >= 400) {
                return jsonMessage(body, "Envoi impossible.");
            }
            if (body != null && body.contains("\"success\":false")) {
                return jsonMessage(body, "Envoi impossible.");
            }
            return null;
        } catch (Exception e) {
            return "Impossible d’envoyer le fichier.";
        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }
    }

    private static void writeFormField(OutputStream out, String boundary, String name, String value) throws Exception {
        out.write(("--" + boundary + "\r\n").getBytes(StandardCharsets.UTF_8));
        out.write(("Content-Disposition: form-data; name=\"" + name + "\"\r\n\r\n").getBytes(StandardCharsets.UTF_8));
        out.write((value + "\r\n").getBytes(StandardCharsets.UTF_8));
    }

    private static String readStream(InputStream in) {
        if (in == null) {
            return "";
        }
        try {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] buf = new byte[2048];
            int n;
            while ((n = in.read(buf)) != -1) {
                out.write(buf, 0, n);
            }
            return out.toString(StandardCharsets.UTF_8.name());
        } catch (Exception e) {
            return "";
        }
    }

    private static String jsonMessage(String body, String fallback) {
        if (body == null || body.isEmpty()) {
            return fallback;
        }
        try {
            return new JSONObject(body).optString("message", fallback);
        } catch (Exception e) {
            return fallback;
        }
    }

    private void evalNativeFiles(String id, JSONArray rows, String error) {
        if (web == null) {
            return;
        }
        String errArg = error == null ? "null" : JSONObject.quote(error);
        web.evaluateJavascript(
            "window.__tnReceiveFiles&&window.__tnReceiveFiles(" + JSONObject.quote(id) + "," + rows.toString() + "," + errArg + ")",
            null
        );
    }

    private JSONObject readUriAsJson(Uri uri) throws Exception {
        String name = displayName(uri);
        String type = getContentResolver().getType(uri);
        if (type == null || type.isEmpty()) {
            String ext = MimeTypeMap.getFileExtensionFromUrl(name.replace(" ", "_"));
            type = ext == null || ext.isEmpty()
                ? "application/octet-stream"
                : MimeTypeMap.getSingleton().getMimeTypeFromExtension(ext.toLowerCase());
            if (type == null) {
                type = "application/octet-stream";
            }
        }
        JSONObject row = new JSONObject();
        row.put("name", name);
        row.put("type", type);
        row.put("data", Base64.encodeToString(readUriBytes(uri, 8 * 1024 * 1024), Base64.NO_WRAP));
        return row;
    }

    private String displayName(Uri uri) {
        String name = "document";
        try (Cursor cursor = getContentResolver().query(uri, new String[]{OpenableColumns.DISPLAY_NAME}, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) {
                int idx = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                if (idx >= 0) {
                    String value = cursor.getString(idx);
                    if (value != null && !value.isEmpty()) {
                        name = value;
                    }
                }
            }
        } catch (Exception ignored) {
        }
        return name;
    }

    private byte[] readUriBytes(Uri uri, int maxBytes) throws Exception {
        try (InputStream in = getContentResolver().openInputStream(uri)) {
            if (in == null) {
                throw new Exception("no stream");
            }
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] buf = new byte[8192];
            int n;
            int total = 0;
            while ((n = in.read(buf)) != -1) {
                total += n;
                if (total > maxBytes) {
                    throw new Exception("too large");
                }
                out.write(buf, 0, n);
            }
            return out.toByteArray();
        }
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
        public void openDocumentPicker(String requestId, int multiple, int imagesOnly, String kind, String token) {
            runOnUiThread(() -> startNativePick(requestId, multiple != 0, imagesOnly != 0, kind, token));
        }

        @JavascriptInterface
        public boolean canPickFiles() {
            return true;
        }

        @JavascriptInterface
        public void downloadUrl(String url, String filename, String token) {
            runOnUiThread(() -> enqueueDownload(url, filename, token));
        }

        @JavascriptInterface
        public boolean notificationsEnabled() {
            return notificationsAllowed();
        }
    }
}
