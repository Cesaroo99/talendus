package ca.talendus.app;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    public static final String APP_URL = "https://talendus.ca/m.html";
    private WebView web;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        setContentView(web);
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setSupportZoom(false);
        settings.setMediaPlaybackRequiresUserGesture(false);
        String ua = settings.getUserAgentString();
        settings.setUserAgentString((ua == null ? "" : ua) + " TalendusApp/1.0");
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
        web.loadUrl(APP_URL);
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) {
            web.goBack();
            return;
        }
        super.onBackPressed();
    }
}
