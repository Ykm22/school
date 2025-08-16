package com.example.parkseein.ui.park

import android.util.Log
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.parkseein.R
import com.example.parkseein.core.Result

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ParkScreen(parkId: String?, onClose: () -> Unit) {
    val parkViewModel = viewModel<ParkViewModel>(factory = ParkViewModel.Factory(parkId))
    val parkUiState = parkViewModel.uiState
    var text by rememberSaveable { mutableStateOf(parkUiState.park.description) }

    Log.d("ParkScreen", "recompose, text = $text")

    LaunchedEffect(parkUiState.submitResult) {
        Log.d("ParkScreen", "Submit = ${parkUiState.submitResult}");
        if (parkUiState.submitResult is Result.Success) {
            Log.d("ParkScreen", "Closing screen");
            onClose();
        }
    }

    var textInitialized by remember { mutableStateOf(parkId == null) }

    LaunchedEffect(parkId, parkUiState.loadResult) {
        Log.d("ParkScreen", "Text initialized = ${parkUiState.loadResult}");
        if (textInitialized) {
            return@LaunchedEffect
        }
        if (!(parkUiState.loadResult is Result.Loading)) {
            text = parkUiState.park.description
            textInitialized = true
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(text = stringResource(id = R.string.park)) },
                actions = {
                    Button(onClick = {
                        Log.d("ParkScreen", "save item text = $text");
                        parkViewModel.saveOrUpdatePark(text)
                    }) { Text("Save") }
                }
            )
        }
    ) {
        Column(
            modifier = Modifier
                .padding(it)
                .fillMaxSize()
        ) {
            if (parkUiState.loadResult is Result.Loading) {
                CircularProgressIndicator()
                return@Scaffold
            }
            if (parkUiState.submitResult is Result.Loading) {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) { LinearProgressIndicator() }
            }
            if (parkUiState.loadResult is Result.Error) {
                Text(text = "Failed to load park - ${(parkUiState.loadResult as Result.Error).exception?.message}")
            }
            Row {
                TextField(
                    value = text,
                    onValueChange = { text = it }, label = { Text("Text") },
                    modifier = Modifier.fillMaxWidth(),
                )
            }
            if (parkUiState.submitResult is Result.Error) {
                Text(
                    text = "Failed to submit park - ${(parkUiState.submitResult as Result.Error).exception?.message}",
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        }
    }
}


@Preview
@Composable
fun PreviewItemScreen() {
    ParkScreen(parkId = "0", onClose = {})
}
