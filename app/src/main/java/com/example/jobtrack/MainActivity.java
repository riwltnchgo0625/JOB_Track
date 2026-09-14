package com.example.jobtrack;

import android.app.Activity;
import android.appwidget.AppWidgetManager;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView webView;

    public class WidgetBridge {
        private final Context context;
        WidgetBridge(Context c) { context = c; }

        @JavascriptInterface
        public void updateWidget(int total, int progress, int documentPass, int finalPass) {
            getSharedPreferences("jobtrack_widget", MODE_PRIVATE).edit()
                .putInt("total", total).putInt("progress", progress)
                .putInt("documentPass", documentPass).putInt("finalPass", finalPass).apply();
            Intent intent = new Intent(context, JobTrackWidgetProvider.class);
            intent.setAction(AppWidgetManager.ACTION_APPWIDGET_UPDATE);
            int[] ids = AppWidgetManager.getInstance(context)
                .getAppWidgetIds(new ComponentName(context, JobTrackWidgetProvider.class));
            intent.putExtra(AppWidgetManager.EXTRA_APPWIDGET_IDS, ids);
            context.sendBroadcast(intent);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.rgb(11,15,23));
        getWindow().setNavigationBarColor(Color.rgb(11,15,23));
        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(11,15,23));
        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);
        WebSettings s=webView.getSettings();
        s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true); s.setAllowFileAccess(true); s.setTextZoom(100);
        webView.addJavascriptInterface(new WidgetBridge(this), "JobTrackWidget");
        webView.setWebViewClient(new WebViewClient(){
            private boolean openExternal(String url){
                if(url!=null&&(url.startsWith("http://")||url.startsWith("https://"))){
                    try{startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));}catch(Exception ignored){}
                    return true;
                } return false;
            }
            @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r){return openExternal(r.getUrl().toString());}
            @Override @SuppressWarnings("deprecation") public boolean shouldOverrideUrlLoading(WebView v,String u){return openExternal(u);}
        });
        webView.loadUrl("file:///android_asset/index.html");
        setContentView(webView);
    }

    @Override @SuppressWarnings("deprecation")
    public void onBackPressed(){
        if(webView!=null){
            webView.evaluateJavascript("window.handleAndroidBack ? window.handleAndroidBack() : false", value -> {
                if(!"true".equals(value)) MainActivity.super.onBackPressed();
            });
        } else super.onBackPressed();
    }
}
