package com.example.parkseein.data.remote

import com.example.parkseein.data.Park
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Headers
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path

interface ParkService {
    @GET("/api/parks")
    suspend fun find(): List<Park>
    // TODO: other api calls

    @Headers("Content-Type: application/json")
    @POST("/api/parks")
    suspend fun create(@Body park: Park): Park

    @Headers("Content-Type: application/json")
    @PUT("/api/parks/{id}")
    suspend fun update(@Path("id") parkId: String?, @Body park: Park): Park
}