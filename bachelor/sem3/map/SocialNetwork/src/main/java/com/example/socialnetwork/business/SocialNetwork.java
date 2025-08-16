package com.example.socialnetwork.business;

import com.example.socialnetwork.domain.*;
import com.example.socialnetwork.domain.validators.UserValidator;
import com.example.socialnetwork.domain.validators.ValidationException;
import com.example.socialnetwork.repository.*;
import com.example.socialnetwork.utils.events.ChangeEventType;
import com.example.socialnetwork.utils.events.Event;
import com.example.socialnetwork.utils.events.UserEntityChangeEvent;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.UUID;
import com.example.socialnetwork.utils.observer.Observable;
import com.example.socialnetwork.utils.observer.Observer;

public class SocialNetwork implements Observable<UserEntityChangeEvent> {
    private final UserValidator userValidator;
    private final Repository repository;
    private final List<Observer<UserEntityChangeEvent>> observers = new ArrayList<>();

    public SocialNetwork(Repository repository) {
        this.repository = repository;
        this.userValidator = new UserValidator();
    }

    /**
     * Validates and adds a new user into the repository
     * @param first_name of new user
     * @param last_name of new user
     * @param email of new user
     * @param password of new user
     * @throws RepositoryException if user with that ID already exists
     * @throws ValidationException if user is invalid
     */
    public void saveUser(String first_name, String last_name, String email, String password)
            throws RepositoryException, ValidationException{
        UUID id = UUID.randomUUID();
        User user = new User(id, first_name, last_name, email, password);
        userValidator.validate(user);
        if(repository.find(email) != null){
            throw new RepositoryException("Email already registered");
        }
        repository.saveUser(user);
        UserEntityChangeEvent event = new UserEntityChangeEvent(ChangeEventType.ADD, user);
        notifyObservers(event);
    }
    /**
     * Removes a user with ID from repository
     * @param email of user to be deleted
     * @throws RepositoryException if ID doesn't exist
     */
    public void deleteUser(String email) throws RepositoryException, ValidationException {
        String error = UserValidator.emailValidate("", email);
        if(!error.equals("")){
            throw new ValidationException(error);
        }
        User deleted_user = repository.deleteUser(email);
        UserEntityChangeEvent event = new UserEntityChangeEvent(ChangeEventType.DELETE, deleted_user);
        notifyObservers(event);
    }

    /**
     * Add a friend to a user
     * @param email1 of user
     * @param email2 of friend
     * @throws RepositoryException if either ID1 or ID2 don't exist
     * @throws ValidationException if either ID1 or ID2 are invalid
     */
    public void saveFriend(String email1, String email2, LocalDateTime dateTime, String status) throws RepositoryException, ValidationException{
        User user = repository.getUser(email1);
        User friend = repository.getUser(email2);

        userValidator.validate(user);
        userValidator.validate(friend);
        Friendship friendship1 = null, friendship2 = null;
        try{
            friendship1 = repository.getFriendship(email1, email2);
        } catch(RepositoryException e){
            ;
        }
        try{
            friendship2 = repository.getFriendship(email2, email1);
        } catch(RepositoryException e){
            ;
        }
        if(friendship1 != null || friendship2 != null){
            throw new RepositoryException("Friendship already exists");
        }
        if(email1.equals(email2)){
            throw new RepositoryException("Cannot have friendship with yourself");
        }

        repository.saveFriend(user, friend, dateTime, status);
        UserEntityChangeEvent event = new UserEntityChangeEvent(ChangeEventType.ADD, user);
        notifyObservers(event);
    }

    /**
     * Remove a friend from a user
     * @param email1 of user
     * @param email2 of friend
     * @throws RepositoryException if either ID1 or ID2 don't exist
     * @throws ValidationException if either ID1 or ID2 are invalid
     */
    public void deleteFriend(String email1, String email2) throws RepositoryException, ValidationException{
        User user = repository.getUser(email1);
        User friend = repository.getUser(email2);

        userValidator.validate(user);
        userValidator.validate(friend);

        repository.deleteFriend(user, friend);
    }

    /**
     * Filters current users by a give first_name
     * @param first_name to filter users by
     * @return ArrayList of Users with that first_name
     * @throws ValidationException if given first_name is invalid
     * @throws RepositoryException if no user with given first_name is found
     */
    public ArrayList<User> filterByFirstName(String first_name) throws ValidationException, RepositoryException{
        String error =  UserValidator.first_nameValidate("", first_name);
        if(!error.equals("")){
            throw new ValidationException(error);
        }
        boolean found = false;
        for(User user : repository.getAllUsers()){
            if(user.getFirst_name().equals(first_name)){
                found = true;
                break;
            }
        }
        if(!found){
            throw new RepositoryException("First name not found");
        }
        return repository.filterByFirstName(first_name);
    }

    public ArrayList<Friendship> getFriendshipsOfUser(User user) {
        return repository.getFriendshipsOfUser(user);
    }

    /**
     * Obtaining the number of communities in the network
     * @return the amount of communities in the repository
     */
    public int communitiesAmount(){
        Map<User, Integer> marked_communities = getAmount();
        if(marked_communities == null){
            return 0;
        }
        Collection<Integer> coll = marked_communities.values();
        int k = 1;
        for(int i : coll){
            if(i > k) k = i;
        }
        return k;
    }

    /**
     * Calculates the longest path of friendships in the social network
     * @return ArrayList of users in the longest path friendships
     */
    public ArrayList<User> longestPathCommunity(){
        ArrayList<User> longestPathUsers = new ArrayList<>();
        ArrayList<User> friends;
        ArrayList<User> users = getUsers();
        int longestPath = -1;
        int longestPathCommunity = -1;
        User finishUser = null;

        //Map with keys as users, and values as their community number
        //key = user
        //value = community number
        Map<User, Integer> userCommunities = getAmount();
        if(userCommunities == null){
            return null;
        }

        //key = user
        //value = user's parent
        Map<User, User> parent = new HashMap<>();
        Map<User, User> finishParent = new HashMap<>();

        //key = user
        //value = distance from root to user
        Map<User, Integer> distance = new HashMap<>();

        //key = user
        //value = visited state(T/F)
        Map<User, Boolean> visited = new HashMap<>();

        //BFS with backtracking
        Stack<User> stack = new Stack<>();
        for(User user : users){
            stack.push(user);
            resetMaps(parent, distance, visited);
            distance.put(user, 0);
            visited.put(user, true);
            while(!stack.isEmpty()){

                user = stack.pop();
                friends = null;
                try{
                    friends = getFriends(user);
                } catch (RepositoryException e){
                    System.out.println("No communities");
                    return null;
                }

                for(User friend : friends){
                    if(!visited.get(friend)){
                        stack.push(friend);
                        distance.put(friend, distance.get(user) + 1);
                        visited.put(friend, true);
                        parent.put(friend, user);
                    }
                }
            }
            for(Map.Entry<User, Integer> entry : distance.entrySet()){
                if(entry.getValue() > longestPath){
                    finishUser = entry.getKey();

                    finishParent.clear();
                    finishParent = parent;

                    longestPath = entry.getValue();

                    longestPathCommunity = userCommunities.get(entry.getKey());
                }
            }
        }
        for(Map.Entry<User, Integer> entry : userCommunities.entrySet()){
            if(entry.getValue() == longestPathCommunity){
                longestPathUsers.add(entry.getKey());
            }
        }
        return longestPathUsers;
    }

    /**
     * Mapping the community numbers to each user
     * @return a map where the keys are users and values their community number
     */
    private Map<User, Integer> getAmount(){
        int k = 1;
        Map<User, Integer> checked = new HashMap<>();
        Map<User, User> checked_connection = new HashMap<>();
//        Set<User> users = inMemoryRepository.getUsers();
//        Set<User> users = fileRepository.getUsers();
        ArrayList<User> users = repository.getAllUsers();
        for(User user : users){
            try{

                if(!checked.containsKey(user)){
                    checkCommunity(user, checked, k, checked_connection);
                    k++;
                }
            } catch(RepositoryException e){
                System.out.println("No communities");
                return null;
            }
        }
        return checked;
    }

    //Recursive method used in getAmount() method
    private void checkCommunity(User user, Map<User, Integer> checked, int k, Map<User, User> checked_connection) throws RepositoryException{
        checked.put(user, k);
        ArrayList<User> friends = repository.getFriends(user);
        for(User friend : friends){
            //if we haven't checked the friend, check him
            if(!checked.containsKey(friend))
                checkCommunity(friend, checked, k, checked_connection);
        }
    }
    /**
     * Obtains a set of users in repository
     * @return a set of users in repository
     */
    public ArrayList<User> getUsers(){
        return repository.getAllUsers();
    }

    /**
     * Obtains the friends of a user
     * @param user whose friends to obtain
     * @return ArrayList of user's friends
     */
    public ArrayList<User> getFriends(User user) throws RepositoryException{
        return repository.getFriends(user);
    }

    private void resetMaps(Map<User, User> parent, Map<User, Integer> distance, Map<User, Boolean> visited) {
        for(User user : getUsers()){
            parent.put(user, null);
            distance.put(user, -1);
            visited.put(user, false);
        }
    }

    /**
     * Finds duration of friendship between 2 users
     * @param user as first end of friendship
     * @param friend as second end of friendship
     * @return Friendship duration
     * @throws RepositoryException if the 2 users aren't friends
     */
    public String getFriendshipLength(User user, User friend) throws RepositoryException{
        String length = "";
        String email1 = user.getEmail();
        String email2 = friend.getEmail();
        for(Friendship friendship : repository.getAllFriendships()) {
            if ((friendship.getEmail1().equals(email1) && friendship.getEmail2().equals(email2))
                    || (friendship.getEmail1().equals(email2) && friendship.getEmail1().equals(email1))) {
                long years = ChronoUnit.YEARS.between(friendship.getFriendsFrom(), LocalDateTime.now());
                long months = ChronoUnit.MONTHS.between(friendship.getFriendsFrom(), LocalDateTime.now());
                long weeks = ChronoUnit.WEEKS.between(friendship.getFriendsFrom(), LocalDateTime.now());
                long days = ChronoUnit.DAYS.between(friendship.getFriendsFrom(), LocalDateTime.now());
                long hours = ChronoUnit.HOURS.between(friendship.getFriendsFrom(), LocalDateTime.now());
                long minutes = ChronoUnit.MINUTES.between(friendship.getFriendsFrom(), LocalDateTime.now());
                long seconds = ChronoUnit.SECONDS.between(friendship.getFriendsFrom(), LocalDateTime.now());
                length += "years: " + Long.toString(years) + "\n";
                length += "months: " + Long.toString(months) + "\n";
                length += "weeks: " + Long.toString(weeks) + "\n";
                length += "days: " + Long.toString(days) + "\n";
                length += "hours: " + Long.toString(hours) + "\n";
                length += "minutes: " + Long.toString(minutes) + "\n";
                length += "seconds: " + Long.toString(seconds) + "\n";
                return length;
            }
        }
        throw new RepositoryException("No friendship between the users");
    }

    public ArrayList<Friendship> getAllFriendships(){
        return repository.getAllFriendships();
    }

    public User getUser(String login_email) throws RepositoryException{
        String errors = UserValidator.emailValidate("", login_email);
        if(!errors.equals("")){
            throw new RepositoryException(errors);
        }
        return repository.getUser(login_email);
    }
    public void updateFriendship(User user1, User user2, FriendshipStatus status) throws RepositoryException{
        repository.updateFriendship(user1, user2, status);
        UserEntityChangeEvent event = new UserEntityChangeEvent(ChangeEventType.UPDATE, user1);
        notifyObservers(event);
    }

    @Override
    public void addObserver(Observer<UserEntityChangeEvent> e) {
        observers.add(e);
    }

    @Override
    public void removeObserver(Observer<UserEntityChangeEvent> e) {
        observers.remove(e);
    }

    @Override
    public void notifyObservers(UserEntityChangeEvent t) {
        observers.forEach(x -> x.update(t));
    }
}
