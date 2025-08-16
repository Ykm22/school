package com.example.parkseein

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.example.parkseein.ui.park.ParkScreen
import com.example.parkseein.ui.parklist.ParkListScreen

val parksRoute = "parks"

@Composable
fun ParkSeeinNavHost() {
    val navController = rememberNavController()
    val onCloseItem = {
        Log.d("ParkSeeinNavHost", "navigate back to list")
        navController.popBackStack()
    }
    NavHost(
        navController = navController,
        startDestination = parksRoute
    ) {
        composable(parksRoute)
        {
            ParkListScreen(
                onParkClick = { parkId ->
                    Log.d("ParkSeeinNavHost", "navigate to park $parkId")
                    navController.navigate("$parksRoute/$parkId")
                },
                onAddPark = {
                    Log.d("ParkSeeinNavHost", "navigate to new park")
                    navController.navigate("$parksRoute-new")
                }
            )
        }
        composable(
            route = "$parksRoute/{id}",
            arguments = listOf(navArgument("id") { type = NavType.StringType })
        )
        {
            ParkScreen(
                parkId = it.arguments?.getString("id"),
                onClose = { onCloseItem() }
            )
        }
        composable(route = "$parksRoute-new")
        {
            ParkScreen(
                parkId = null,
                onClose = { onCloseItem() }
            )
        }
    }
}