package com.example.parkseein.ui.parklist

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.parkseein.ParkSeeinApp
import com.example.parkseein.data.ParkRepository
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import com.example.parkseein.core.Result
import com.example.parkseein.core.TAG
import com.example.parkseein.data.Park
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class ParkListViewModel(private val parkRepository: ParkRepository): ViewModel() {
//    val uiState: StateFlow<Result<List<Park>>> = parkRepository.parkStream.stateIn(
//        scope = viewModelScope,
//        started = SharingStarted.WhileSubscribed(),
//        initialValue = Result.Loading
//    )
    val uiState: Flow<List<Park>> = parkRepository.parkStream
    init {
        Log.d(TAG, "init")
        loadParks()
    }

    fun loadParks() {
        Log.d(TAG, "loadParks...")
        viewModelScope.launch {
            parkRepository.refresh()
        }
    }

    companion object {
        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val app = (this[ViewModelProvider.AndroidViewModelFactory.APPLICATION_KEY] as ParkSeeinApp)
                ParkListViewModel(app.container.parkRepository)
            }
        }
    }
}