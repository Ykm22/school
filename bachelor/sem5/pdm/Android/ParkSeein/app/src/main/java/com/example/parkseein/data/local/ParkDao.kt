package com.example.parkseein.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.example.parkseein.data.Park
import kotlinx.coroutines.flow.Flow

@Dao
interface ParkDao {
    @Query("SELECT * FROM parks")
    fun getAll(): Flow<List<Park>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(park: Park)

    @Update
    suspend fun update(park: Park): Int

    @Query("DELETE FROM parks WHERE _id = :id")
    suspend fun deleteById(id: String): Int

    @Query("DELETE FROM parks")
    suspend fun deleteAll()
}