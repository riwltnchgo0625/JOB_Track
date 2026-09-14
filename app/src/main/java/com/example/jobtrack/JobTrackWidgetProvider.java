package com.example.jobtrack;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.widget.RemoteViews;

public class JobTrackWidgetProvider extends AppWidgetProvider {
    @Override public void onUpdate(Context context, AppWidgetManager manager, int[] ids) {
        SharedPreferences p=context.getSharedPreferences("jobtrack_widget",Context.MODE_PRIVATE);
        int total=p.getInt("total",0), progress=p.getInt("progress",0), doc=p.getInt("documentPass",0), fin=p.getInt("finalPass",0);
        for(int id:ids){
            RemoteViews v=new RemoteViews(context.getPackageName(),R.layout.widget_jobtrack);
            v.setTextViewText(R.id.widget_total,String.valueOf(total));
            v.setTextViewText(R.id.widget_progress,String.valueOf(progress));
            v.setTextViewText(R.id.widget_doc,String.valueOf(doc));
            v.setTextViewText(R.id.widget_final,String.valueOf(fin));
            Intent i=new Intent(context,MainActivity.class);
            PendingIntent pi=PendingIntent.getActivity(context,0,i,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
            v.setOnClickPendingIntent(R.id.widget_root,pi);
            manager.updateAppWidget(id,v);
        }
    }
}
