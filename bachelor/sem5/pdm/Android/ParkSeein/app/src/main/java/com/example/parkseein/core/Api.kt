package com.example.parkseein.core

import com.google.gson.GsonBuilder
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object Api {
    private val url = "192.168.1.123:3000/"
    private val httpUrl = "http://$url"
    val wsUrl = "ws://$url"

    private var gson = GsonBuilder().create()

    val retrofit = Retrofit.Builder()
        .baseUrl(httpUrl)
        .addConverterFactory(GsonConverterFactory.create(gson))
        .build()

    val okHttpClient = OkHttpClient.Builder()
        .build()
}