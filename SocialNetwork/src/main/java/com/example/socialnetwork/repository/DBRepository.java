package com.example.socialnetwork.repository;

import com.example.socialnetwork.domain.*;
import com.example.socialnetwork.domain.validators.*;


import java.sql.*;
import java.time.DateTimeException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class DBRepository implements Repository{
    private final String db_url;
    private final String db_username;
    private final String db_password;


    public DBRepository(String db_url, String db_username, String db_password) {
        this.db_url = db_url;
        this.db_username = db_username;
        this.db_password = db_password;
    }

    @Override
    public ArrayList<User> getAllUsers(){
        ArrayList<User> users = new ArrayList<>();
        int row = 1;
        try(Connection connection = DriverManager.getConnection(db_url, db_username, db_password);
            PreparedStatement preparedStatementUsers = connection.prepareStatement("SELECT * FROM users");
            ResultSet resultSetUsers = preparedStatementUsers.executeQuery()){
            //first load users
            while (resultSetUsers.next()) {
                String first_name = resultSetUsers.getString("first_name");
                String last_name = resultSetUsers.getString("last_name");
                String password = resultSetUsers.getString("password");
                String email = resultSetUsers.getString("email");
                UserValidator validator = new UserValidator();
                UUID uuid = UUID.randomUUID();
                User user = new User(uuid, first_name, last_name, email, password);
                try {
                    validator.validate(user);
                } catch (ValidationException e) {
                    System.out.println("Row " + row + " invalid");
                    System.out.println("Validation exception in users table of SocialNetwork DB\n" + e.getMessage());
                    System.exit(1);
                }
                users.add(user);
                row++;
            }
        } catch (SQLException e){
            e.printStackTrace();
        }
        return users;
    }

    @Override
    public ArrayList<Friendship> getAllFriendships() {
        ArrayList<Friendship> friendships = new ArrayList<>();
        int entry = 1;
        try(Connection connection = DriverManager.getConnection(db_url, db_username, db_password);
            PreparedStatement preparedStatementFriendships = connection.prepareStatement("SELECT * FROM friendships");
            ResultSet resultSetFriendships = preparedStatementFriendships.executeQuery()){
            while(resultSetFriendships.next()){
                try{
                    Friendship friendship = getFriendshipFromResultSet(resultSetFriendships, entry);
                    friendships.add(friendship);
                } catch(RepositoryException e){
                    System.out.println("Repository exception " + e.getMessage());
                } catch(DateTimeException e){
                    System.out.println("DateTimeException " + e.getMessage());
                }
                entry++;
            }
        } catch(SQLException e){
            System.out.println("SQLException: " + e.getMessage());
        }
        return friendships;
    }

    private Friendship getFriendshipFromResultSet(ResultSet resultSetFriendships, int entry) throws RepositoryException, SQLException, DateTimeException {
        System.out.println("alooooooo");
        String email_sender = resultSetFriendships.getString("email_sender");
        User user_sender = getUser(email_sender);

        String email_receiver = resultSetFriendships.getString("email_receiver");
        User user_receiver = getUser(email_receiver);

        if(email_sender.equals(email_receiver)){
            throw new RepositoryException("Entry: " + entry + " - Cannot have friendship between a user and himself: " + email_sender + " and " + email_receiver);
        }

        String friends_from = resultSetFriendships.getString("friends_from");
        LocalDateTime dateTime = null;
        try{
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm");
            dateTime = LocalDateTime.parse(friends_from, formatter);
        } catch(DateTimeException e){
            throw new DateTimeException("Entry: " + entry + " - Invalid date time");
        }

        String status = resultSetFriendships.getString("status");
        if(!status.equals("ACCEPTED") && !status.equals("PENDING")){
            throw new RepositoryException("Entry: " + entry + " - Status invalid");
        }
        Friendship friendship = new Friendship(email_sender, email_receiver);
        friendship.setFriendsFrom(dateTime);
        friendship.setStatus(status);
        return friendship;
    }

    /**
     * Saving a user to the database
     * @param user to save to the database
     */
    private void saveUserToDB(User user){
        String sql = "INSERT INTO users (first_name, last_name, password, email) VALUES (?, ?, ?, ?)";
        try(Connection connection = DriverManager.getConnection(db_url, db_username, db_password);
            PreparedStatement preparedStatement = connection.prepareStatement(sql)){
            preparedStatement.setString(1, user.getFirst_name());
            preparedStatement.setString(2, user.getLast_name());
            preparedStatement.setString(3, user.getPassword());
            preparedStatement.setString(4, user.getEmail());
            preparedStatement.executeUpdate();
        }catch (SQLException e){
            e.printStackTrace();
        }
    }
    @Override
    public ArrayList<User> saveUser(User user) throws IllegalArgumentException {
        saveUserToDB(user);
        return null;
    }

    @Override
    public User deleteUser(String email) throws RepositoryException, IllegalArgumentException {
        User user = getUser(email);
        deleteUserFromDB(user);
        return user;
    }

    /**
     * Deleting a user from the database
     * @param user to delete
     */
    private void deleteUserFromDB(User user) {
        String sql = "DELETE FROM users WHERE email = (?)";
        try(Connection connection = DriverManager.getConnection(db_url, db_username, db_password);
            PreparedStatement preparedStatement = connection.prepareStatement(sql)){
            preparedStatement.setString(1, user.getEmail());
            preparedStatement.executeUpdate();
        } catch (SQLException e){
            e.printStackTrace();
        }
    }

    @Override
    public ArrayList<User> getFriends(User user) throws RepositoryException {
        ArrayList<User> friends = new ArrayList<>();
        String sql = "SELECT email_sender AS email_friend FROM friendships\n" +
                "WHERE email_receiver = (?)\n" +
                "AND status = 'ACCEPTED'\n" +
                "UNION\n" +
                "SELECT email_receiver FROM friendships\n" +
                "WHERE email_sender = (?)\n" +
                "AND status = 'ACCEPTED'";
        try(Connection connection = DriverManager.getConnection(db_url, db_username, db_password);
            PreparedStatement ps = connection.prepareStatement(sql)){
            ps.setString(1, user.getEmail());
            ps.setString(2, user.getEmail());
            ResultSet friendsResultSet = ps.executeQuery();
            while(friendsResultSet.next()){
                String email_friend = friendsResultSet.getString("email_friend");
                User friend = getUser(email_friend);
                friends.add(friend);
            }
        } catch (SQLException e){
            //e.printStackTrace();
        }
        return friends;
    }

    @Override
    public ArrayList<User> filterByFirstName(String first_name) {
        List<User> users = getAllUsers().stream()
                .filter(user -> user.getFirst_name().equals(first_name))
                .toList();
        return new ArrayList<User>(users);
    }

    @Override
    public User getUser(String email) throws RepositoryException {
        String sql = "SELECT * FROM users";
        try(Connection connection = DriverManager.getConnection(db_url, db_username, db_password);
            PreparedStatement ps = connection.prepareStatement(sql)){
            ResultSet usersResultSet = ps.executeQuery();
            while(usersResultSet.next()){
                String email_DB = usersResultSet.getString("email");
                if(email.equals(email_DB)){
                    String first_name = usersResultSet.getString("first_name");
                    String last_name = usersResultSet.getString("last_name");
                    String password = usersResultSet.getString("password");
                    UUID uuid = UUID.randomUUID();
                    return new User(uuid, first_name,  last_name, email, password);
                }
            }
        } catch (SQLException e){
            e.printStackTrace();
        }
        throw new RepositoryException("Email not found");
    }

    @Override
    public Friendship saveFriend(User user, User friend, LocalDateTime dateTime, String status) throws IllegalArgumentException {
        Friendship friendship = new Friendship(user.getEmail(), friend.getEmail());
        friendship.setFriendsFrom(dateTime);
        friendship.setStatus(status);
        saveFriendshipToDB(friendship);
        return friendship;
    }

    /**
     * Saving a friendship to the database
     * @param friendship to save
     */
    private void saveFriendshipToDB(Friendship friendship) {
        String sql = "INSERT INTO friendships (email_sender, email_receiver, friends_from, status) VALUES (?, ?, ?, ?)";
        try(Connection connection = DriverManager.getConnection(db_url, db_username, db_password);
            PreparedStatement preparedStatement = connection.prepareStatement(sql)){
            preparedStatement.setString(1, friendship.getEmail1());
            preparedStatement.setString(2, friendship.getEmail2());
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm");
            String stringDateTime = friendship.getFriendsFrom().format(formatter);
            preparedStatement.setString(3, stringDateTime);
            String stringStatus = friendship.getStatusToString();
            preparedStatement.setString(4, stringStatus);
            preparedStatement.executeUpdate();
        } catch (SQLException e){
            e.printStackTrace();
        }
    }

    @Override
    public Friendship deleteFriend(User user, User friend) throws IllegalArgumentException, RepositoryException {
        Friendship friendship = new Friendship(user.getEmail(), user.getEmail());
        deleteFriendshipFromDB(friendship);
        return friendship;
    }

    /**
     * Deleting a friendship from the database
     * @param friendship to delete
     */
    private void deleteFriendshipFromDB(Friendship friendship) {
        String sql = "DELETE FROM friendships WHERE email_sender = (?) AND email_receiver = (?)";
        try(Connection connection = DriverManager.getConnection(db_url, db_username, db_password);
            PreparedStatement preparedStatement = connection.prepareStatement(sql)){
            preparedStatement.setString(1, friendship.getEmail1());
            preparedStatement.setString(2, friendship.getEmail2());
            preparedStatement.executeUpdate();
        } catch (SQLException e){
            e.printStackTrace();
        }
    }

    @Override
    public Friendship updateFriendship(User user_sender, User user_receiver, FriendshipStatus new_status) throws RepositoryException {
        System.out.println("sender " + user_sender.getEmail());
        System.out.println("receiver " + user_receiver.getEmail());
        Friendship friendship = getFriendship(user_sender.getEmail(), user_receiver.getEmail());
        System.out.println("alo");
        friendship.setStatus(new_status);
        if(new_status == FriendshipStatus.DECLINED){
            deleteFriendshipFromDB(friendship);
        }else {
            updateFriendshipToDB(friendship);
        }
        return friendship;
    }

    @Override
    public Friendship getFriendship(String email_sender, String email_receiver) throws RepositoryException {
        String sql = "SELECT * FROM friendships\n" +
                "WHERE email_sender = (?)\n" +
                "AND email_receiver = (?)";
        try(Connection connection = DriverManager.getConnection(db_url, db_username, db_password);
            PreparedStatement ps = connection.prepareStatement(sql)){
            ps.setString(1, email_sender);
            ps.setString(2, email_receiver);
            ResultSet friendshipResultSet = ps.executeQuery();
            friendshipResultSet.next();
            return getFriendshipFromResultSet(friendshipResultSet, 0);
        } catch(SQLException e){
            //e.printStackTrace();
        }
        throw new RepositoryException("Friendship non-existent");
    }

    /**
     * Updating the state of a friendship in the database
     * @param friendship to update
     */
    private void updateFriendshipToDB(Friendship friendship) {
        String sql = "UPDATE friendships SET status = (?), friends_from = (?) WHERE email_sender = (?) AND email_receiver = (?)";
        try(Connection connection = DriverManager.getConnection(db_url, db_username, db_password);
            PreparedStatement preparedStatement = connection.prepareStatement(sql)){
            preparedStatement.setString(1, friendship.getStatusToString());

            LocalDateTime now = LocalDateTime.now();
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm");
            preparedStatement.setString(2, now.format(formatter));

            preparedStatement.setString(3, friendship.getEmail1());
            preparedStatement.setString(4, friendship.getEmail2());
            preparedStatement.executeUpdate();
        } catch(SQLException e){
            e.printStackTrace();
        }
    }

    @Override
    public User find(String email) {
        User wanted_user = null;
        for(User user : getAllUsers()){
            if(user.getEmail().equals(email)){
                wanted_user = user;
            }
        }
        return wanted_user;
    }

    @Override
    public ArrayList<Friendship> getFriendshipsOfUser(User user) {
        ArrayList<Friendship> friendships = new ArrayList<>();
        for(Friendship friendship : getAllFriendships()){
            if(friendship.getEmail1().equals(user.getEmail()) ||
                friendship.getEmail2().equals(user.getEmail())){
                friendships.add(friendship);
            }
        }
        return friendships;
    }
}
