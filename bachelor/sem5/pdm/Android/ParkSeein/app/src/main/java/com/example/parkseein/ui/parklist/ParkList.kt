package com.example.parkseein.ui.parklist

import android.util.Log
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.ClickableText
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.parkseein.data.Park

typealias OnParkFn = (id: String?) -> Unit

@Composable
fun ParkList(parkList: List<Park>, onParkClick: OnParkFn, modifier: Modifier) {
    Log.d("ParkList", "recompose")
    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(12.dp)
    ) {
        items(parkList) {park ->
            ParkDetail(park, onParkClick)
        }
    }
}

@Composable
fun ParkDetail(park: Park, onParkClick: OnParkFn) {
    Log.d("ParkDetail", "recompose id = ${park._id}")
    Row {
        ClickableText(text = AnnotatedString(park.description),
            style = TextStyle(
                fontSize = 24.sp,
            ), onClick = { onParkClick(park._id) })
    }
}