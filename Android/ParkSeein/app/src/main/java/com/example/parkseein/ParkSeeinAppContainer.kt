package com.example.parkseein

import android.content.Context
import android.util.Log
import com.example.parkseein.core.Api
import com.example.parkseein.core.TAG
import com.example.parkseein.data.ParkRepository
import com.example.parkseein.data.local.ParkSeeinAppDatabase
import com.example.parkseein.data.remote.ParkService
import com.example.parkseein.data.remote.ParkWsClient

class ParkSeeinAppContainer(val context: Context) {
    init {
        Log.d(TAG, "init")
    }

    val parkService: ParkService = Api.retrofit.create(ParkService::class.java)
    val parkWsClient: ParkWsClient = ParkWsClient(Api.okHttpClient)

    val database: ParkSeeinAppDatabase by lazy { ParkSeeinAppDatabase.getDatabase(context) }

    val parkRepository: ParkRepository by lazy {
        ParkRepository(parkService, parkWsClient, database.parkDao())
    }
}