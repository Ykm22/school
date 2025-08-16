package com.example.socialnetwork.factory;

import com.example.socialnetwork.repository.Repository;

public interface Factory<Type, Strategy> {
    Type create(Strategy strategy);
}
