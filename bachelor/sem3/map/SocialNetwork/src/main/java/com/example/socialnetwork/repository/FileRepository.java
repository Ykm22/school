package com.example.socialnetwork.repository;

import com.example.socialnetwork.domain.*;
import com.example.socialnetwork.domain.validators.UserValidator;
import com.example.socialnetwork.domain.validators.ValidationException;

import java.io.*;
import java.nio.file.*;
import java.sql.SQLOutput;
import java.time.DateTimeException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

public class FileRepository extends InMemoryRepository {
    private final String userFileName;
    private final String friendshipFileName;

    public FileRepository(String userFileName, String friendshipFileName) {
        this.userFileName = userFileName;
        this.friendshipFileName = friendshipFileName;
        loadData();
        saveUserData();
        saveFriendshipData();
    }

    /**
     * Loads data from file to the repository
     */
    private void loadData(){
        try{
            Path path_user = Paths.get(userFileName);
            BufferedReader bufferedReader = Files.newBufferedReader(path_user);
            //Read a line
            String line = bufferedReader.readLine();

            //Read til we're out of users
            while(line != null && !line.equals("")){

                //Saving user
                String[] user_string = line.split(";");
//                String user_email = user_string[2];
                User user = null;

                //*********If he doesn't exist, make new one
                UUID user_uuid = UUID.randomUUID();
                user = new User(user_uuid, user_string[0], user_string[1], user_string[2], user_string[3]);

                UserValidator validator = new UserValidator();
                try{
                    validator.validate(user);
                } catch(ValidationException e){
                    System.out.println("In: " + userFileName);
                    System.out.println("User: " + user.toString());
                    System.out.println("Validation exception: "+ e.getMessage());
                    System.exit(1);
                }
                super.saveUser(user);
                line = bufferedReader.readLine();
            }
            bufferedReader.close();
        } catch (IOException e){
            e.printStackTrace();
        }

        try{
            int row_count = 1;
            Path path_friendships = Paths.get(friendshipFileName);
            BufferedReader bufferedReader = Files.newBufferedReader(path_friendships);
            String line = bufferedReader.readLine();
            while(line != null && !line.equals("")){
                String[] friendship_line = line.split(";");
                String email_sender = friendship_line[0];
                String email_receiver = friendship_line[1];
                User user_sender = null;
                User user_receiver = null;
                try{
                    user_sender = getUser(email_sender);
                } catch(RepositoryException e){
                    System.out.println("In: " + friendshipFileName);
                    System.out.println("Email: " + email_sender);
                    System.out.println("Repository exception: " + e.getMessage());
                    System.exit(1);
                }
                try{
                    user_receiver = getUser(email_receiver);
                } catch(RepositoryException e){
                    System.out.println("In: " + friendshipFileName);
                    System.out.println("Email: " + email_receiver);
                    System.out.println("Repository exception: " + e.getMessage());
                    System.exit(1);
                }
                //status part
                String status = friendship_line[3];
                Friendship friendship = new Friendship(email_sender, email_receiver);
                if(!status.equals("ACCEPTED") && !status.equals("PENDING")){
                    System.out.println("At line " + row_count);
                    System.out.println("Repository exception: invalid friendship status");
                    System.exit(1);
                }
                LocalDateTime dateTime = null;
                try{
                    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm");
                    dateTime = LocalDateTime.parse(friendship_line[2], formatter);
                    System.out.println(email_sender);
                } catch(DateTimeException e){
                    System.out.println("At line " + row_count);
                    System.out.println("DateTimeException: " + e.getMessage());
                }
                if(status.equals("ACCEPTED")){
                    saveFriend(user_sender, user_receiver, dateTime, "ACCEPTED");
                } else{
                    saveFriend(user_sender, user_receiver, dateTime, "PENDING");
                }
                //next line
                line = bufferedReader.readLine();
            }
            bufferedReader.close();
        } catch(IOException e){
            e.printStackTrace();
        }
    }

    /**
     * Saves data from repository to file
     */
    private void saveUserData() {
        try {
            BufferedWriter bufferedWriter = Files.newBufferedWriter(Paths.get(userFileName));
            bufferedWriter.flush();

            getUsers().forEach(user -> {
//                System.out.println("save user: " + user);
                try {
                    bufferedWriter.write(user.toString() + "\n");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
            bufferedWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Saves data about friendships in a file
     */
    private void saveFriendshipData(){
        try{
            BufferedWriter bufferedWriter = Files.newBufferedWriter(Paths.get(friendshipFileName));
            bufferedWriter.flush();
            getAllFriendships().forEach(friendship -> {
                try{
                    bufferedWriter.write(friendship.toString() + "\n");
                } catch(IOException e){
                    e.printStackTrace();
                }
            });
            bufferedWriter.close();
        } catch(IOException e){
            e.printStackTrace();
        }
    }

    @Override
    public ArrayList<User> saveUser(User user) throws IllegalArgumentException{
        ArrayList<User> friends = super.saveUser(user);
        saveUserData();
        return friends;
    }

    @Override
    public User deleteUser(String email) throws RepositoryException, IllegalArgumentException{
        User deleted_user = super.deleteUser(email);
        saveUserData();
        saveFriendshipData();
        return deleted_user;
    }

    @Override
    public Friendship saveFriend(User user, User friend, LocalDateTime dateTime, String status) throws IllegalArgumentException  {
        Friendship friendship = super.saveFriend(user, friend, dateTime, status);
        saveFriendshipData();
        return friendship;
    }

    @Override
    public Friendship deleteFriend(User user, User friend) throws IllegalArgumentException, RepositoryException{
        Friendship friendship = super.deleteFriend(user, friend);
        saveFriendshipData();
        return friendship;
    }

    @Override
    public Friendship updateFriendship(User user_sender, User user_receiver, FriendshipStatus new_status) throws RepositoryException{
        Friendship friendship = super.updateFriendship(user_sender, user_receiver, new_status);
        saveFriendshipData();
        return friendship;
    }
}
