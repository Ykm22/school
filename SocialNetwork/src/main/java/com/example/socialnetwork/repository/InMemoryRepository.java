package com.example.socialnetwork.repository;

import com.example.socialnetwork.domain.*;

import java.time.*;
import java.util.*;

public class InMemoryRepository implements Repository{
    protected final Map<User, ArrayList<User>> friendships;
    protected ArrayList<Friendship> friendshipsDurations;

    @Override
    public ArrayList<Friendship> getFriendshipsOfUser(User user) {
        return null;
    }

    @Override
    public User find(String email) {
        return null;
    }

    public InMemoryRepository() {
        friendships = new HashMap<>();
        friendshipsDurations = new ArrayList<>();
    }

    @Override
    public ArrayList<User> saveUser(User user) throws IllegalArgumentException {
        if(user == null){
            throw new IllegalArgumentException("User cannot be null");
        }
        try{
            notFound(user.getEmail());
        } catch (RepositoryException e){
            System.out.println("Repository exception: " + e.getMessage());
        }
        if(friendships.containsKey(user)){
            return friendships.get(user);
        }
        friendships.put(user, new ArrayList<>());
        return friendships.get(user);
    }

    @Override
    public User deleteUser(String email) throws RepositoryException, IllegalArgumentException {
        User user = getUser(email);
        ArrayList<User> friends_of_user = friendships.get(user);
        for(User friend_of_user : friends_of_user){
//            friendships.get(friend_of_user).remove(user);
            deleteFriend(user, friend_of_user);
        }
        friendships.remove(user);
        return user;
    }

    @Override
    public Friendship saveFriend(User user, User friend, LocalDateTime dateTime, String status) throws IllegalArgumentException  {
        if(user == null || friend == null){
            throw new IllegalArgumentException("User cannot be null");
        }
        try{
            checkNoFriendship(user, friend);
        } catch (RepositoryException e){
            System.out.println("Repository exception: " + e.getMessage());
        }
        friendships.get(user).add(friend);
        friendships.get(friend).add(user);

        Friendship friendship = new Friendship(user.getEmail(), friend.getEmail());
        friendship.setFriendsFrom(dateTime);
        friendship.setStatus(status);
        friendshipsDurations.add(friendship);

        return friendship;
    }

    @Override
    public Friendship updateFriendship(User user_sender, User user_receiver, FriendshipStatus new_status) throws RepositoryException{
        if(user_sender == null || user_receiver == null){
            throw new IllegalArgumentException("User cannot be null");
        }
        Friendship friendship = getFriendship(user_sender.getEmail(), user_receiver.getEmail());
        if(new_status == FriendshipStatus.DECLINED){
            removeFriendship(user_sender.getEmail(), user_receiver.getEmail());
        }
        else{
            friendships.get(user_sender).add(user_receiver);
            friendships.get(user_receiver).add(user_sender);
            friendship.setStatus(new_status);
            friendship.setFriendsFrom(LocalDateTime.now());
        }
        return friendship;
    }

    private void removeFriendship(String email1, String email2) throws RepositoryException{
        Friendship friendship = getFriendship(email1, email2);
        getAllFriendships().remove(friendship);
    }

    @Override
    public Friendship deleteFriend(User user, User friend) throws IllegalArgumentException, RepositoryException{
        if(user == null || friend == null){
            throw new IllegalArgumentException("User cannot be null");
        }
        try{
            checkFriendship(user, friend);
        } catch (RepositoryException e){
            System.out.println("Repository exception: " + e.getMessage());
        }

        friendships.get(user).remove(friend);
        friendships.get(friend).remove(user);

        Friendship friendship = getFriendship(user.getEmail(), friend.getEmail());

        friendshipsDurations.remove(friendship);

        return friendship;
    }

    @Override
    public User getUser(String email) throws RepositoryException, IllegalArgumentException{
        Set<User> users = friendships.keySet();
        for(User user : users){
            if(user.getEmail().equals(email))
                return user;
        }
        throw new RepositoryException("User not found");
    }

    /**
     * Tests if email exists
     * @param email to get tested
     * @return true if ID doesn't exist
     * @throws RepositoryException if ID exists
     */
    public boolean notFound(String email) throws RepositoryException, IllegalArgumentException{
        Set<User> users = friendships.keySet();
        for(User user : users){
            if(user.getEmail().equals(email)){
                throw new RepositoryException("Email already exists");
            }
        }
        return true;
    }

    @Override
    public ArrayList<User> getAllUsers() {
        List<User> list_users = friendships.keySet().stream()
                .toList();
        return new ArrayList<User>(list_users);
    }

    public Set<User> getUsers(){
        return friendships.keySet();
    }

    @Override
    public ArrayList<User> getFriends(User user) throws RepositoryException{
        ArrayList<User> result = new ArrayList<>();
        for(User friend : friendships.get(user)){
            result.add(friend);
        }
        return result;
    }

    /**
     * Tests if there is no friendship between 2 users
     * @param user as first end of friendship
     * @param friend as second end of friendship
     * @return true if there is no friendship between the users
     * @throws RepositoryException if friendships exists
     */
    public boolean checkNoFriendship(User user, User friend) throws RepositoryException{
        if(user.equals(friend)){
            throw new RepositoryException("Cannot create friendship between a user and himself");
        }
//        ArrayList<User> friends = friendships.get(user);
//        for(User friend1 : friends){
//            if(friend.equals(friend1)){
//                throw new RepositoryException("Friendship exists");
//            }
//        }
        ArrayList<Friendship> friendships = getAllFriendships();
        for(Friendship friendship : friendships){
            if(friendship.getEmail1().equals(user.getEmail()) && friendship.getEmail2().equals(friend.getEmail()))
                throw new RepositoryException("Friendship exists");
            if(friendship.getEmail2().equals(user.getEmail()) && friendship.getEmail1().equals(friend.getEmail()))
                throw new RepositoryException("Friendship exists");
        }
        return true;
    }

    /**
     * Tests if friendship between 2 users exists
     * @param user as first end of friendship
     * @param friend as second end of friendship
     * @return true if there is friendship between the users
     * @throws RepositoryException if friendships doesn't exist
     */
    public boolean checkFriendship(User user, User friend) throws RepositoryException{
        ArrayList<User> friends = friendships.get(user);
        for(User friend1 : friends){
            if(friend1.equals(friend))
                return true;
        }
        throw new RepositoryException("Friendship doesn't exist");
    }

    @Override
    public ArrayList<User> filterByFirstName(String first_name){
        ArrayList<User> filtered_users = new ArrayList<>();
        Set<User> users = getUsers();
        for(User user : users){
            if(user.getFirst_name().equals(first_name))
                filtered_users.add(user);
        }
        return filtered_users;
    }

    @Override
    public Friendship getFriendship(String email1, String email2) throws RepositoryException{
        for(Friendship friendship : friendshipsDurations){
            if(friendship.getEmail1().equals(email1) && friendship.getEmail2().equals(email2)){
                return friendship;
            }
        }
        throw new RepositoryException("Non-existent friendship");
    }

    @Override
    public ArrayList<Friendship> getAllFriendships(){
        return friendshipsDurations;
    }
}