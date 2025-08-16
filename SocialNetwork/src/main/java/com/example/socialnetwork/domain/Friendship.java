package com.example.socialnetwork.domain;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.UUID;

public class Friendship {
    private final String email1, email2;
    private LocalDateTime friendsFrom;
    private FriendshipStatus status;

    public Friendship(String email1, String email2){
        this.email1 = email1;
        this.email2 = email2;
//        this.friendsFrom = LocalDateTime.now();
        this.status = FriendshipStatus.PENDING;
    }

    @Override
    public String toString() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm");
        String formatted_dateTime = friendsFrom.format(formatter);
        return email1 + ";" + email2 + ";" + formatted_dateTime + ";" + status;
    }

    public FriendshipStatus getStatus() {
        return status;
    }

    public void setStatus(FriendshipStatus status) {
        this.status = status;
    }

    public void setStatus(String status) {
        if(status.equals("ACCEPTED")){
            this.status = FriendshipStatus.ACCEPTED;
        } else if(status.equals("PENDING")){
            this.status = FriendshipStatus.PENDING;
        } else {
            this.status = FriendshipStatus.DECLINED;
        }
    }

    public void setStatusFromString(String status){
        if(status.equals("ACCEPTED")){
            this.status = FriendshipStatus.ACCEPTED;
        } else if(status.equals("PENDING")){
            this.status = FriendshipStatus.PENDING;
        } else {
            this.status = FriendshipStatus.DECLINED;
        }
    }

    public String getEmail1() {
        return email1;
    }

    public String getEmail2() {
        return email2;
    }

    public LocalDateTime getFriendsFrom() {
        return friendsFrom;
    }

    public void setFriendsFrom(LocalDateTime friendsFrom){
        this.friendsFrom = friendsFrom;
    }

    public String getStatusToString(){
        if(status == FriendshipStatus.DECLINED){
            return "DECLINED";
        }
        if(status == FriendshipStatus.ACCEPTED){
            return "ACCEPTED";
        }
        return "PENDING";
    }

    public String getStringFriendsFrom() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'hh-mm");
        return getFriendsFrom().format(formatter);
    }

//    private final UUID uuid1, uuid2;
//    private final LocalDateTime friendsFrom;
//    public Friendship(UUID uuid1, UUID uuid2){
//        this.uuid1 = uuid1;
//        this.uuid2 = uuid2;
//        friendsFrom = LocalDateTime.now();
//    }
//
//    public UUID getUuid1() {
//        return uuid1;
//    }
//
//    public UUID getUuid2() {
//        return uuid2;
//    }
}
