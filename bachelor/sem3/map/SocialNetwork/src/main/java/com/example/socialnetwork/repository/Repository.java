package com.example.socialnetwork.repository;

import com.example.socialnetwork.domain.Friendship;
import com.example.socialnetwork.domain.FriendshipStatus;
import com.example.socialnetwork.domain.User;
import com.example.socialnetwork.domain.validators.ValidationException;

import java.time.LocalDateTime;
import java.util.ArrayList;

public interface Repository {
    /**
     * Saves a user to the repository
     * @param user to be added
     * @return List of user's friends
     * @throws ValidationException if user is invalid
     */
    ArrayList<User> saveUser(User user) throws ValidationException;

    /**
     * Deletes a user from the repository
     * @param email of user to be deleted
     * @return deleted user
     * @throws RepositoryException if user with ID not found
     */
    User deleteUser(String email) throws RepositoryException;

    /**
     * Saves a friend to a user
     * @param user as first end of friendship
     * @param friend as second end of friendship
     * @return List of user's friends
     * @throws ValidationException if either user or friend are invalid
     * @throws RepositoryException if either user or friend are not found
     */
    Friendship saveFriend(User user, User friend, LocalDateTime dateTime, String status) throws ValidationException, RepositoryException;

    /**
     * Deletes a friend from a user
     * @param user from whom to delete friendship
     * @param friend of whom to delete friendship
     * @return List of user's friends
     * @throws ValidationException if either user or friend are invalid
     * @throws RepositoryException if either user or friend are not found
     */
    Friendship deleteFriend(User user, User friend) throws ValidationException, RepositoryException;

    /**
     * Obtains the user with ID
     * @param email of user to be returned
     * @return User with ID
     * @throws RepositoryException if ID is not found
     */
    User getUser(String email) throws RepositoryException;

    /**
     * Obtains the set of users
     * @return set of current users
     */
    ArrayList<User> getAllUsers();

    /**
     * Obtains list of user's friends
     * @param user of friends to obtain
     * @return list of user's friends
     */
    ArrayList<User> getFriends(User user) throws RepositoryException;

    /**
     * Filter users by their first name
     * @param first_name to filter by
     * @return List of users filtered by first name
     */
    ArrayList<User> filterByFirstName(String first_name);

    /**
     * Obtains the friendship of 2 users
     * @param email1 of first user
     * @param email2 of second user
     * @return the friendship between the 2 users
     * @throws RepositoryException if the 2 users don't have a friendship
     */
    Friendship getFriendship(String email1, String email2) throws RepositoryException;

    /**
     * Updates friendship between 2 users with possible statuses:
     * Pending, accepted, declined
     * @param user_sender  user that sent the request
     * @param user_receiver user that received the request
     * @param new_status of the friendship between the 2 users
     * @throws RepositoryException if the friendship doesn't exist
     */
    Friendship updateFriendship(User user_sender, User user_receiver, FriendshipStatus new_status) throws RepositoryException;

    /**
     * Obtains all friendships in the repository no matter their statuses
     * @return a list of Friendship entities
     */
    ArrayList<Friendship> getAllFriendships();

    /**
     * Find a user by email
     * @param email of wanted user
     * @return user if it exists, null otherwise
     */
    User find(String email);

    /**
     * Returns all friendships no matter their statuses with the user
     * @param user of wanted friendships
     * @return ArrayList of user's friendships, null if there are none
     */
    ArrayList<Friendship> getFriendshipsOfUser(User user);
}