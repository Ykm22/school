package com.example.socialnetwork.domain;

import java.util.Objects;
import java.util.UUID;

public class User {
    private UUID ID;
    private String first_name;
    private String last_name;
    private String email;
    private String password;

    /**
     * User constructor
     * @param ID of new User
     * @param first_name of new User
     * @param last_name of new User
     * @param email of new user
     * @param password of new User
     */
    public User(UUID ID, String first_name, String last_name, String email, String password) {
        this.ID = ID;
        this.first_name = first_name;
        this.last_name = last_name;
        this.email = email;
        this.password = password;
    }

    /**
     * Returns last name of user
     * @return last_name of user
     */
    public String getLast_name() {
        return last_name;
    }

    /**
     * Sets new last name to user
     * @param last_name new last name
     */
    public void setLast_name(String last_name) {
        this.last_name = last_name;
    }

    /**
     * Returns email of user
     * @return email
     */
    public String getEmail() {
        return email;
    }

    /**
     * Sets the new email to user
     * @param email new email
     */
    public void setEmail(String email) {
        this.email = email;
    }

    /**
     * Returns the password of a user
     * @return password of user
     */
    public String getPassword() {
        return password;
    }

    /**
     * Sets new user password
     * @param password new password
     */
    public void setPassword(String password) {
        this.password = password;
    }

    /**
     * Returns ID of user
     * @return ID
     */
    public UUID getID() {
        return ID;
    }

    /**
     * Sets new user ID
     * @param ID to be set
     */
    public void setID(UUID ID) {
        this.ID = ID;
    }

    /**
     * Returns user name
     * @return name
     */
    public String getFirst_name() {
        return first_name;
    }

    /**
     * Sets new User first_name
     * @param first_name to be set
     */
    public void setFirst_name(String first_name) {
        this.first_name = first_name;
    }

    /**
     * Override of toString() method
     * @return attributes as string
     */
    @Override
    public String toString() {
        return first_name + ";" + last_name + ";" + email + ";" + password;
    }

    /**
     * Comparing 2 Users
     * @param o other user
     * @return true if the 2 users are equal, false otherwise
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof User user)) return false;
        return getID() == user.getID() && Objects.equals(getFirst_name(), user.getFirst_name()) && Objects.equals(getLast_name(), user.getLast_name()) && Objects.equals(getEmail(), user.getEmail()) && Objects.equals(getPassword(), user.getPassword());
    }

    /**
     * Obtaining hashCode of a user
     * @return hashCode of a user
     */
    @Override
    public int hashCode() {
        return Objects.hash(getID(), getFirst_name(), getLast_name(), getEmail(), getPassword());
    }
}
