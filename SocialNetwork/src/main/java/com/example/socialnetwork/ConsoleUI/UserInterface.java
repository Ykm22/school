package com.example.socialnetwork.ConsoleUI;

import com.example.socialnetwork.business.SocialNetwork;
import com.example.socialnetwork.domain.Friendship;
import com.example.socialnetwork.domain.FriendshipStatus;
import com.example.socialnetwork.domain.User;
import com.example.socialnetwork.domain.validators.ValidationException;
import com.example.socialnetwork.factory.repositoryFactory.RepositoryFactory;
import com.example.socialnetwork.factory.repositoryFactory.RepositoryStrategy;
import com.example.socialnetwork.repository.Repository;
import com.example.socialnetwork.repository.RepositoryException;

import java.sql.SQLOutput;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Set;

public class UserInterface {
    private SocialNetwork socialNetwork;
    private final Scanner input;
    public UserInterface(){
        input = new Scanner(System.in);
    }

    /**
     * Run the UI
     */
    public void run(){
        SocialNetwork socialNetwork = getSocialNetwork();

        int command = -1;
        while(true){
            showCommands();
            try{
                command = Integer.parseInt(input.nextLine());
            } catch (NumberFormatException e){
                e.printStackTrace();
            }
            if(command == 1){
                printUsers();
            } else if(command == 2){
                addUser();
            } else if(command == 3){
                removeUser();
            } else if(command == 4){
                addFriend();
            } else if(command == 5){
                removeFriend();
            } else if(command == 6){
                loginPannel();
            } else if(command == 7){
                printCommunitiesNumber();
            } else if(command == 8){
                printBiggestCommunity();
            } else if(command == 9){
                printAllFriendships();
            } else if(command == 10){
                getFriendshipLength();
            }
            else if(command == 0){
                System.exit(0);
            } else {
                System.out.println("Give a proper command");
            }
            System.out.println();
            if(command != 1)
                printUsers();
        }
    }

    /**
     * Creating the service
     * @return service with wanted repository type
     */
    private SocialNetwork getSocialNetwork() {
        System.out.println("Wanted repository:");
        System.out.println("1 - In memory repository");
        System.out.println("2 - File repository");
        System.out.println("3 - DB repository");
        try{
            System.out.print(">> ");
            int repository_type = Integer.parseInt(input.nextLine());
            Repository repository = createRepository(repository_type);
            socialNetwork = new SocialNetwork(repository);
            System.out.println("alo");
        } catch(NumberFormatException e){
            e.printStackTrace();
        }
        return socialNetwork;
    }

    /**
     * Login pannel for a user
     */
    private void loginPannel() {
        try{
            System.out.print("Email: ");
            String login_email = input.nextLine();
            User login_user = socialNetwork.getUser(login_email);

            System.out.print("Password: ");
            String login_password = input.nextLine();
            if(!login_password.equals(login_user.getPassword())){
                System.out.println("Wrong password");
                return;
            }
            userActions(login_user);
        } catch(RepositoryException e){
            e.printStackTrace();
        }
    }

    /**
     * Possible actions for a user
     * @param login_user that can choose between actions
     */
    private void userActions(User login_user) {
        while(true){
            printUserCommands();
            int command;
            try{
                command = Integer.parseInt(input.nextLine());
                if(command == 1){
                    userViewFriends(login_user);
                } else if(command == 2){
                    sendFriendRequest(login_user);
                } else if(command == 3){
                    updateFriendshipRequest(login_user);
                } else if (command == 0) {
                    return;
                } else {
                    System.out.println("Give a proper command ;)");
                }
            } catch(NumberFormatException e){
                e.printStackTrace();
            } catch(RepositoryException e){
                System.out.println("Repository exception: " + e.getMessage());
            }
        }
    }

    /**
     * Sending a friend request to a user
     * @param login_user from whom to send the request
     */
    private void sendFriendRequest(User login_user) {
        try{
            User user_requested = findUserInRepo(0);
            socialNetwork.saveFriend(login_user.getEmail(), user_requested.getEmail(), LocalDateTime.now(), "PENDING");
        } catch(RepositoryException e){
            System.out.println("Repository exception: " + e.getMessage());
        } catch(ValidationException e){
            System.out.println("Validation exceptoin: " + e.getMessage());
        }
    }

    /**
     * Updates the friendship state of a user with another user
     * @param login_user whom to update friendship state
     */
    private void updateFriendshipRequest(User login_user) {
        try{
            userViewFriends(login_user);
            System.out.print("Email to modify friendship with: ");
            String friend_email = input.nextLine();
            User friend = socialNetwork.getUser(friend_email);

            ArrayList<Friendship> friendships = socialNetwork.getAllFriendships();

            System.out.println("Choose from: accept/decline");
            System.out.print("New friendship status: ");
            String string_status = input.nextLine();
            boolean found = false;
            FriendshipStatus status;
            if(string_status.equals("accept")){
                acceptFriendRequest(login_user, friend);
            } else if(string_status.equals("decline")){
                declineFriendRequest(login_user, friend);
            } else {
                System.out.println("Give a proper command ;)");
            }
        } catch(RepositoryException e){
            System.out.println("Repository exception: " + e.getMessage());
        }
    }

    /**
     * Declines or deletes a friendship between a user and a friend
     * @param login_user on the first end
     * @param friend on the second end
     */
    private void declineFriendRequest(User login_user, User friend) {
        FriendshipStatus status = FriendshipStatus.DECLINED;
        try{
            for(Friendship friendship : socialNetwork.getAllFriendships()){
                if(friendship.getEmail1().equals(login_user.getEmail()) && friendship.getEmail2().equals(friend.getEmail())){
                    socialNetwork.updateFriendship(login_user, friend, status);
                    return;
                }
                if(friendship.getEmail1().equals(friend.getEmail()) && friendship.getEmail2().equals(login_user.getEmail())){
                    socialNetwork.updateFriendship(friend, login_user, status);
                    return;
                }
            }
        } catch (RepositoryException e){
            System.out.println("Repository exception: " + e.getMessage());
        }
        System.out.println("No available friendships to decline or delete");
    }

    /**
     * Accepts the friend request incoming to the user from a possible friend
     * @param login_user who is on the receiving side
     * @param friend who is on the sending side
     */
    private void acceptFriendRequest(User login_user, User friend) {
        FriendshipStatus status = FriendshipStatus.ACCEPTED;
        try{
            for(Friendship friendship : socialNetwork.getAllFriendships()){
                if(friendship.getEmail1().equals(friend.getEmail()) && friendship.getEmail2().equals(login_user.getEmail())){
                    socialNetwork.updateFriendship(friend, login_user, status);
                    return;
                }
            }
        } catch(RepositoryException e){
            System.out.println("Repository exception: " + e.getMessage());
        }
        System.out.println("No available requests to accept");
    }

    /**
     * Prints the pending, incoming and current friendships of a user
     * @param login_user to see friendships of
     */
    private void userViewFriends(User login_user) throws RepositoryException{
        ArrayList<Friendship> friendships = socialNetwork.getAllFriendships();
        if(friendships.size() == 0){
            throw new RepositoryException("No friendships yet");
        }
        friendships.forEach(friendship -> {
            if(friendship.getEmail1().equals(login_user.getEmail()) &&
                    friendship.getStatus() == FriendshipStatus.PENDING){
                System.out.println("Pending to " + friendship.getEmail2() + " since " + friendship.getStringFriendsFrom());
            }
        });
        friendships.forEach(friendship -> {
            if (friendship.getEmail2().equals(login_user.getEmail()) &&
                    friendship.getStatus() == FriendshipStatus.PENDING) {
                System.out.println("Incoming from " + friendship.getEmail1() + " since " + friendship.getStringFriendsFrom());
            }
        });
        friendships.forEach(friendship -> {
            if(friendship.getEmail2().equals(login_user.getEmail()) &&
                    friendship.getStatus() == FriendshipStatus.ACCEPTED){
                System.out.println("Friends with " + friendship.getEmail1() + " since " + friendship.getStringFriendsFrom());
            }
        });
        friendships.forEach(friendship -> {
            if(friendship.getEmail1().equals(login_user.getEmail()) &&
                    friendship.getStatus() == FriendshipStatus.ACCEPTED){
                System.out.println("Friends with " + friendship.getEmail2() + " since " + friendship.getStringFriendsFrom());
            }
        });
    }

    /**
     * Possible commands for a logged in user
     */
    private void printUserCommands() {
        System.out.println("1 - View friends");
        System.out.println("2 - Send a friend request");
        System.out.println("3 - Modify a friend request");
        System.out.println("0 - Logout");
        System.out.print(">> ");
    }

    /**
     * Obtains the duration of a friendship
     */
    private void getFriendshipLength() {
        try{
            User user1 = findUserInRepo(1);
            User user2 = findUserInRepo(2);
            String length = socialNetwork.getFriendshipLength(user1, user2);
            System.out.println(length);
        } catch(RepositoryException e) {
            System.out.println("Repository exception: " + e.getMessage());
            return;

        } catch(IllegalArgumentException e){
            System.out.println("Illegal argument exception: " + e.getMessage());
            return;
        } catch(RuntimeException e){
            System.out.println("Runtime exception: " + e.getMessage());
            return;
        } catch(ValidationException e){
            System.out.println("Validation exception: "+ e.getMessage());
            return;
        }
    }

    /**
     * Obtains a specific type of repository
     * @param repository_type which type of repository wanted
     * @return a Repository of repository_type type
     */
    private Repository createRepository(int repository_type) {
        RepositoryFactory instance = RepositoryFactory.getInstance();
        if(repository_type == 1) {
            return instance.create(RepositoryStrategy.IN_MEMORY_REPOSIORY);
        }
        if(repository_type == 2) {
            return instance.create(RepositoryStrategy.FILE_REPOSITORY);
        }
        if(repository_type == 3) {
            return instance.create(RepositoryStrategy.DB_REPOSITORY);
        }
        System.out.println("Next time give the right index ;)");
        System.exit(0);
        return null;
    }

    /**
     * Prints all users to the console
     */
    private void printUsers() {
        ArrayList<User> users = socialNetwork.getUsers();
        if(users.size() == 0){
            System.out.println("No users currently");
        }
        else{
            int index = 1;
            System.out.println("Current users");
            System.out.println("Index | User");

            for(User user : users){
                System.out.println(index + " | " + user.toString());
                index++;
            }
        }
        System.out.println();
    }

    /**
     * Adding a user after reading it from console
     */
    private void addUser(){
        String first_name, last_name, email, password;
        System.out.print("First name: ");
        first_name = input.nextLine();
        System.out.print("Last name: ");
        last_name = input.nextLine();
        System.out.print("Email: ");
        email = input.nextLine();
        System.out.print("Password: ");
        password = input.nextLine();
        try{
            socialNetwork.saveUser(first_name, last_name, email, password);
        } catch(RepositoryException e){
            System.out.println("Repository exception: " + e.getMessage());
            return;
        } catch(IllegalArgumentException e){
            System.out.println("Illegal argument exception: " + e.getMessage());
            return;
        } catch(ValidationException e){
            System.out.println("Validation exception: " + e.getMessage());
            return;
        }
        System.out.println("User added");
    }

    /**
     * Removing a user
     */
    private void removeUser(){
        try{
            User user_to_delete = findUserInRepo(0);
            socialNetwork.deleteUser(user_to_delete.getEmail());
        } catch(RepositoryException e){
            System.out.println("Repository exception: " + e.getMessage());
            return;
        } catch(ValidationException e){
            System.out.println("Validation exception: " + e.getMessage());
            return;
        }
        catch(IllegalArgumentException e){
            System.out.println("Illegal argument exception: " + e.getMessage());
            return;
        } catch(RuntimeException e){
            //System.out.println("RuntimeException:\n" + e.getMessage());
            return;
        }
        System.out.println("User removed");
    }

    /**
     * Adding a friend
     */
    private void addFriend(){
        try{
            User user1 = findUserInRepo(1);
            User user2 = findUserInRepo(2);
            socialNetwork.saveFriend(user1.getEmail(), user2.getEmail(), LocalDateTime.now(), "PENDING");
        } catch(RepositoryException e){
            System.out.println("Repository exception: " + e.getMessage());
            return;

        } catch(ValidationException e){
            System.out.println("Validation exception: " + e.getMessage());
            return;
        }
        catch(IllegalArgumentException e){
            System.out.println("Illegal argument exception: " + e.getMessage());
            return;
        } catch(RuntimeException e){
            System.out.println("Runtime exception: " + e.getMessage());
            return;
        }
        System.out.println("Friendship realized");
    }

    /**
     * Removing a friend
     */
    private void removeFriend() {
        try{
            User user1 = findUserInRepo(0);
            User user2 = findFriend_of_User(user1);
            socialNetwork.deleteFriend(user1.getEmail(), user2.getEmail());
        } catch(RepositoryException e){
            System.out.println("Repository exception: " + e.getMessage());
            return;

        } catch(ValidationException e){
            System.out.println("Validation exception: " + e.getMessage());
            return;
        }
        catch(IllegalArgumentException e){
            System.out.println("Illegal argument exception: " + e.getMessage());
            return;
        } catch(RuntimeException e){
            System.out.println("RuntimeException: " + e.getMessage());
            return;
        }
        System.out.println("Friendship broken");
    }

    /**
     * Prints to the console a list of users of the biggest community
     */
    private void printBiggestCommunity() {

        ArrayList<User> users = socialNetwork.longestPathCommunity();
        if(users == null){
            //System.out.println("No communities");
            return;
        }
//        if(users.size() == 0){
//            System.out.println("No friendships made");
//            return;
//        }
        for(User user : users){
            System.out.println(user.getFirst_name() + " " + user.getLast_name());
        }
    }

    /**
     * Prints to the console the amount of communities in the network
     */
    private void printCommunitiesNumber() {
        int x = socialNetwork.communitiesAmount();
        System.out.println("Number of communities: " + x);
    }

    /**
     * Prints to the console the current friendships
     */
    public void printAllFriendships(){
        socialNetwork.getAllFriendships().forEach(System.out::println);
    }

    /**
     * Prints to the console a list of commands
     */
    private static void showCommands(){
        System.out.println("Commands available");
        System.out.println("1 - Print all users");
        System.out.println("2 - Add a user");
        System.out.println("3 - Delete a user");
        //System.out.println("4 - Add a friend to a user");
        //System.out.println("5 - Delete a friend from a user");
        System.out.println("6 - Log into a user");
        //System.out.println("7 - Print the number of communities");
        //System.out.println("8 - Print the biggest community");
        System.out.println("9 - Print all friendships and their statuses");
        System.out.println("10 - Print duration of friendship between two users");
        System.out.println("0 - Exit");
        System.out.print(">> ");
    }


    /**
     * Finds a user by filtering after its first name
     */
    private User findUserInRepo(int which) throws RepositoryException, ValidationException{
        if(which == 1){
            System.out.print("First name of first user: ");
        } else if(which == 2){
            System.out.print("First name of second user: ");
        } else if(which == 0){
            System.out.print("First name of user: ");
        }

        String first_name = input.nextLine();
        ArrayList<User> filtered_users = socialNetwork.filterByFirstName(first_name);

        int index = 1;
        System.out.println("Index | User");
        for(User user : filtered_users){
            System.out.println(index + " | " + user.toString());
            index++;
        }
        System.out.print("Index of user: ");
        int first_index = -1;
        try{
            first_index = Integer.parseInt(input.nextLine());
        } catch(NumberFormatException e){
            e.printStackTrace();
        }
        if(first_index < 1 || first_index > filtered_users.size()){
            throw new RuntimeException("First Index out of bounds");
        }
        return filtered_users.get(first_index - 1);
    }

    /**
     * Finds a friend of a user from that user's friends list
     * @param user of whom to find friend
     * @return the friend wanted
     * @throws RepositoryException if the friend wanted doesn't exist
     */
    private User findFriend_of_User(User user) throws RepositoryException{
        System.out.println("\nList of friends of user");
        ArrayList<User> user_friends = socialNetwork.getFriends(user);
        int index = 1;
        for (User friend : user_friends) {
            System.out.println(index + " | " + friend.toString());
            index++;
        }

        System.out.print("Index of user: ");
        int second_index = -1;
        //try{
        second_index = Integer.parseInt(input.nextLine());
        if (second_index < 1 || second_index > user_friends.size()) {
            throw new RuntimeException("Second Index out of bounds");
        }
        return user_friends.get(second_index - 1);
    }
}

