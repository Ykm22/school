package com.example.parkseein.data

import android.util.Log
import com.example.parkseein.core.Result
import com.example.parkseein.core.TAG
import com.example.parkseein.data.local.ParkDao
import com.example.parkseein.data.remote.ParkEvent
import com.example.parkseein.data.remote.ParkService
import com.example.parkseein.data.remote.ParkWsClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.channels.BufferOverflow
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.withContext

class ParkRepository(
    private val parkService: ParkService,
    private val parkWsClient: ParkWsClient,
    private val parkDao: ParkDao
) {
//    private var parks: List<Park> = listOf()
//
//    private var parksFlow: MutableSharedFlow<Result<List<Park>>> = MutableSharedFlow(
//        replay = 1,
//        onBufferOverflow = BufferOverflow.DROP_OLDEST
//    )

//    var parkStream: Flow<Result<List<Park>>> = parksFlow
    val parkStream by lazy { parkDao.getAll() }

    init {
        Log.d(TAG, "init")
    }

    suspend fun refresh() {
        Log.d(TAG, "refresh started")
        try {
            val parks = parkService.find()
            parkDao.deleteAll()
            parks.forEach{ parkDao.insert(it) }
            Log.d(TAG, "refresh succeeded")
        } catch (e: Exception) {
            Log.w(TAG, "refresh failed", e)
        }
    }

    suspend fun update(park: Park): Park {
        Log.d(TAG, "update $park...")
        val updatedPark = parkService.update(park._id, park)
        Log.d(TAG, "update $park succeeded")
        handleParkUpdated(updatedPark)
        return updatedPark
    }

    suspend fun save(park: Park): Park {
        Log.d(TAG, "save $park...")
        val createdPark = parkService.create(park)
        Log.d(TAG, "save $park succeeded")
        handleParkCreated(createdPark)
        return createdPark
    }

    suspend fun openWsClient() {
        Log.d(TAG, "openWsClient")
        withContext(Dispatchers.IO) {
            getParksEvent().collect {
                Log.d(TAG, "Item event collected $it")
                if (it is Result.Success) {
                    val parkEvent = it.data;
                    when (parkEvent.event) {
                        "created" -> handleParkCreated(parkEvent.payload.park)
                        "updated" -> handleParkUpdated(parkEvent.payload.park)
                        "deleted" -> handleParkDeleted(parkEvent.payload.park)
                    }
                }
            }
        }
    }

    suspend fun closeWsClient() {
        Log.d(TAG, "closeWsClient")
        withContext(Dispatchers.IO) {
            parkWsClient.closeSocket()
        }
    }

    suspend fun getParksEvent(): Flow<Result<ParkEvent>> = callbackFlow {
        Log.d(TAG, "getItemEvents started")
        parkWsClient.openSocket(
            onEvent = {
                Log.d(TAG, "onEvent $it")
                if (it != null) {
                    Log.d(TAG, "onEvent trySend $it")
                    trySend(Result.Success(it))
                }
            },
            onClosed = { close() },
            onFailure = { close() });
        awaitClose { parkWsClient.closeSocket() }
    }

    private suspend fun handleParkCreated(park: Park) {
        Log.d(TAG, "handleParkCreated...")
//        parks = parks.plus(park)
//        parksFlow.emit(Result.Success(parks))
        parkDao.insert(park)
    }


    private suspend fun handleParkUpdated(park: Park) {
        Log.d(TAG, "handleParkUpdated...")
//        parks = parks.map { if (it._id == park._id) park else it }
//        parksFlow.emit(Result.Success(parks))
        parkDao.update(park)
    }

    private suspend fun handleParkDeleted(park: Park) {
        Log.d(TAG, "handleParkDeleted - todo $park")
    }
}