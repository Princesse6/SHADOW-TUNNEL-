package com.shadow.tunnel
import android.content.Intent
import android.net.VpnService
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
class MainActivity : AppCompatActivity() {
    private lateinit var configInput: EditText
    private lateinit var btnConnect: Button
    private lateinit var statusText: TextView
    private var isConnected = false
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        configInput = findViewById(R.id.configInput)
        btnConnect = findViewById(R.id.btnConnect)
        statusText = findViewById(R.id.statusText)
        btnConnect.setOnClickListener {
            if (!isConnected) {
                val config = configInput.text.toString()
                if (config.isEmpty()) { Toast.makeText(this, "Colle ta config", Toast.LENGTH_SHORT).show(); return@setOnClickListener }
                getSharedPreferences("shadow", MODE_PRIVATE).edit().putString("last_config", config).putBoolean("auto_connect", true).apply()
                val intent = VpnService.prepare(this)
                if (intent != null) startActivityForResult(intent, 100) else startVpn(config)
            } else stopVpn()
        }
    }
    private fun startVpn(config: String) {
        val intent = Intent(this, ShadowVpnService::class.java)
        intent.putExtra("config", config)
        startService(intent)
        isConnected = true; btnConnect.text = "DECONNECTER"; statusText.text = "Connecté"
    }
    private fun stopVpn() {
        stopService(Intent(this, ShadowVpnService::class.java))
        isConnected = false; btnConnect.text = "CONNECTER"; statusText.text = "Déconnecté"
    }
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 100 && resultCode == RESULT_OK) startVpn(configInput.text.toString())
    }
}
