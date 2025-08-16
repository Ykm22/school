package com.example.parkseein

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.lifecycleScope
import com.example.parkseein.core.TAG
import com.example.parkseein.ui.theme.ParkSeeinTheme
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Log.d(TAG, "onCreate")
            ParkSeein {
                ParkSeeinNavHost()
            }
        }
    }

    override fun onResume() {
        super.onResume()
        lifecycleScope.launch {
            (application as ParkSeeinApp).container.parkRepository.openWsClient()
        }
    }

    override fun onPause() {
        super.onPause()
        lifecycleScope.launch {
            (application as ParkSeeinApp).container.parkRepository.closeWsClient()
        }
    }
}

@Composable
fun ParkSeein(content: @Composable () -> Unit) {
    Log.d("MyApp", "recompose")
    ParkSeeinTheme {
        Surface {
            content()
        }
    }
}

@Preview
@Composable
fun PreviewMyApp() {
    ParkSeein {
        ParkSeeinNavHost()
    }
}