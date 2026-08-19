package ca.talendus.app;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class NotifAlarmReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        NotifPoller.pollAsync(context);
    }
}
