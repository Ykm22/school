package com.example.parkseein.ui.park

import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.parkseein.ParkSeeinApp
import com.example.parkseein.data.Park
import com.example.parkseein.data.ParkRepository
import kotlinx.coroutines.launch
import com.example.parkseein.core.Result
import com.example.parkseein.core.TAG

data class ParkUiState(
    val parkId: String? = null,
    val park: Park = Park(),
    var loadResult: Result<Park>? = null,
    var submitResult: Result<Park>? = null,
)

class ParkViewModel(private val parkId: String?, private val parkRepository: ParkRepository) : ViewModel() {

    var uiState: ParkUiState by mutableStateOf(ParkUiState(loadResult = Result.Loading))
        private set

    init {
        Log.d(TAG, "init")
        if (parkId != null) {
            loadPark()
        } else {
            uiState = uiState.copy(loadResult = Result.Success(Park()))
        }
    }

    fun loadPark() {
        viewModelScope.launch {
            parkRepository.parkStream.collect { parks ->
                if (!(uiState.loadResult is Result.Loading)) {
                    return@collect
                }
//                if (result is Result.Success) {
//                    val parkList = result.data
//                    val park = parkList.find { it._id == parkId } ?: Park()
//                    uiState = uiState.copy(loadResult = Result.Success(park), park = park)
//                } else if (result is Result.Error) {
//                    uiState =
//                        uiState.copy(loadResult = Result.Error(result.exception))
//                }
                val park = parks.find{ it._id == parkId} ?: Park()
                uiState = uiState.copy(park = park, loadResult = Result.Success(park))
            }
        }
    }

    fun saveOrUpdatePark(text: String) {
        viewModelScope.launch {
            Log.d(TAG, "saveOrUpdatePark...");
            try {
                uiState = uiState.copy(submitResult = Result.Loading)
                val park = uiState.park.copy(description = text)
                val savedPark: Park;
                if (parkId == null) {
                    savedPark = parkRepository.save(park)
                } else {
                    savedPark = parkRepository.update(park)
                }
                Log.d(TAG, "saveOrUpdatePark succeeded");
                uiState = uiState.copy(submitResult = Result.Success(savedPark))
            } catch (e: Exception) {
                Log.d(TAG, "saveOrUpdatePark failed");
                uiState = uiState.copy(submitResult = Result.Error(e))
            }
        }
    }

    companion object {
        fun Factory(parkId: String?): ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val app = (this[ViewModelProvider.AndroidViewModelFactory.APPLICATION_KEY] as ParkSeeinApp)
                ParkViewModel(parkId, app.container.parkRepository)
            }
        }
    }
}
