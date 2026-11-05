package com.shadow.tunnel
import android.content.Intent
import android.net.VpnService
import android.os.ParcelFileDescriptor
class ShadowVpnService : VpnService() {
    private var vpnInterface: ParcelFileDescriptor? = null
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val config = intent?.getStringExtra("config") ?: ""
        val builder = Builder()
        builder.setSession("SHADOW TUNNEL")
        builder.addAddress("10.0.0.2", 32)
        builder.addRoute("0.0.0.0", 0)
        builder.addDnsServer("8.8.8.8")
        builder.addDnsServer("1.1.1.1")
        vpnInterface = builder.establish()
        return START_STICKY
    }
    override fun onDestroy() { vpnInterface?.close(); super.onDestroy() }
}
