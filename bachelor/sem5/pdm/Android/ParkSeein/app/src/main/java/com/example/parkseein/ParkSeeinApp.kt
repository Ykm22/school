package com.example.parkseein

import android.app.Application
import android.util.Log
import com.example.parkseein.core.TAG

class ParkSeeinApp: Application() {
    lateinit var container: ParkSeeinAppContainer

    override fun onCreate() {
        super.onCreate()
        Log.d(TAG, "init")
        container = ParkSeeinAppContainer(this)
    }
}