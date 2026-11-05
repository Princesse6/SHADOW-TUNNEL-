package com.shadow.tunnel
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            val prefs = context.getSharedPreferences("shadow", Context.MODE_PRIVATE)
            val auto = prefs.getBoolean("auto_connect", false)
            val last = prefs.getString("last_config", "")
            if (auto && !last.isNullOrEmpty()) {
                val i = Intent(context, ShadowVpnService::class.java)
                i.putExtra("config", last)
                context.startService(i)
            }
        }
    }
}
