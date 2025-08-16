package com.example.parkseein.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.example.parkseein.data.Converters
import com.example.parkseein.data.Park

@Database(entities = arrayOf(Park::class), version = 1, exportSchema = false)
@TypeConverters(Converters::class)
abstract class ParkSeeinAppDatabase: RoomDatabase() {

    abstract fun parkDao(): ParkDao

    companion object {
        @Volatile
        private var INSTANCE: ParkSeeinAppDatabase? = null

        fun getDatabase(context: Context): ParkSeeinAppDatabase {
            return INSTANCE?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context,
                    ParkSeeinAppDatabase::class.java,
                    "park_seein_app_database")
                    .build()
                INSTANCE = instance
                instance
            }
        }
    }
}