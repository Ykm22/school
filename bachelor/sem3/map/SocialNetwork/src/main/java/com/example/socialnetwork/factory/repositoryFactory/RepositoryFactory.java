package com.example.socialnetwork.factory.repositoryFactory;

import com.example.socialnetwork.factory.Factory;
import com.example.socialnetwork.repository.*;

public class RepositoryFactory implements Factory<Repository, RepositoryStrategy> {
    private RepositoryFactory(){};
    private static RepositoryFactory instance = new RepositoryFactory();

    public Repository create(RepositoryStrategy repositoryStrategy){
        if(repositoryStrategy == RepositoryStrategy.IN_MEMORY_REPOSIORY){
            return new InMemoryRepository();
        }
        if(repositoryStrategy == RepositoryStrategy.FILE_REPOSITORY){
            return new FileRepository("users.csv", "friendships.csv");
        }
        //to implement
        if(repositoryStrategy == RepositoryStrategy.DB_REPOSITORY){
            String url = "jdbc:postgresql://localhost:5432/SocialNetwork";
            return new DBRepository(url, "postgres", "postgres");
        }
        return null;
    }
    public static RepositoryFactory getInstance(){
        return instance;
    }
}
