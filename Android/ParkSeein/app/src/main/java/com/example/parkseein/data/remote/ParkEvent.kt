package com.example.parkseein.data.remote

import com.example.parkseein.data.Park

data class Payload(val park: Park)
data class ParkEvent(val event: String, val payload: Payload)