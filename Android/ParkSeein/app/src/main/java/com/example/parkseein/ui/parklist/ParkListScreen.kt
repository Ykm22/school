package com.example.parkseein.ui.parklist

import android.util.Log
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.parkseein.R
import com.example.parkseein.core.TAG
import com.example.parkseein.core.Result
import com.example.parkseein.data.Park

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ParkListScreen(onParkClick: (id: String?) -> Unit, onAddPark: () -> Unit) {
    Log.d("ParkListScreen", "recompose")
    val parkListViewModel = viewModel<ParkListViewModel>(factory = ParkListViewModel.Factory)
    val parkListUiState by parkListViewModel.uiState.collectAsStateWithLifecycle(
        initialValue = listOf()
    )

    Scaffold(
        topBar = {
            TopAppBar(title = { Text(text = stringResource(id = R.string.parks))})
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = {
                    Log.d("ParkListScreen", "add")
                    onAddPark()
                },
            ) { Icon(Icons.Rounded.Add, "Add") }
        }
    ) {
//        when (parkListUiState) {
//            is Result.Success ->
//                ParkList(
//                    parkList = (parkListUiState as Result.Success<List<Park>>).data,
//                    onParkClick = onParkClick,
//                    modifier = Modifier.padding(it)
//                )
//
//            is Result.Loading -> CircularProgressIndicator(modifier = Modifier.padding(it))
//            is Result.Error -> Text(
//                text = "Failed to load parks - ${(parkListUiState as Result.Error).exception?.message}",
//                modifier = Modifier.padding(it)
//            )
//        }
        ParkList(
            parkList = parkListUiState,
            onParkClick = onParkClick,
            modifier = Modifier.padding(it)
        )
    }
}

@Preview
@Composable
fun PreviewItemsScreen() {
    ParkListScreen(onParkClick = {}, onAddPark = {})
}