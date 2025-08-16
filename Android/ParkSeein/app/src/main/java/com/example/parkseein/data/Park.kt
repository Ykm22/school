package com.example.parkseein.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.TypeConverter
import com.google.gson.Gson

data class Photo(val filepath: String = "", val webviewPath: String = "", val base64String: String = "")

data class MarkerCoordinates(val lat: Float = 0.0f, val lng: Float = 0.0f)

class Converters {
    @TypeConverter
    fun fromPhoto(photo: Photo?): String? {
        return Gson().toJson(photo)
    }

    @TypeConverter
    fun toPhoto(photoString: String?): Photo? {
        return Gson().fromJson(photoString, Photo::class.java)
    }

    @TypeConverter
    fun fromMarkerCoordinates(coordinates: MarkerCoordinates?): String? {
        return Gson().toJson(coordinates)
    }

    @TypeConverter
    fun toMarkerCoordinates(coordinatesString: String?): MarkerCoordinates? {
        return Gson().fromJson(coordinatesString, MarkerCoordinates::class.java)
    }
}
@Entity(tableName = "parks")
data class Park(
    @PrimaryKey
    val _id: String = "",
    val description: String = "",
    val photo: Photo = Photo(),
    val coordinates: MarkerCoordinates = MarkerCoordinates()
)