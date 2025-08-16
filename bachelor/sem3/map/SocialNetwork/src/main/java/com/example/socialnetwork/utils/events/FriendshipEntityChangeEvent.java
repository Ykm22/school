package com.example.socialnetwork.utils.events;

import com.example.socialnetwork.domain.User;

public class FriendshipEntityChangeEvent implements Event{
    private ChangeEventType type;
    private User data, oldData;

    public FriendshipEntityChangeEvent(ChangeEventType type, User data) {
        this.type = type;
        this.data = data;
    }
    public FriendshipEntityChangeEvent(ChangeEventType type, User data, User oldData) {
        this.type = type;
        this.data = data;
        this.oldData=oldData;
    }

    public ChangeEventType getType() {
        return type;
    }

    public User getData() {
        return data;
    }

    public User getOldData() {
        return oldData;
    }
}
