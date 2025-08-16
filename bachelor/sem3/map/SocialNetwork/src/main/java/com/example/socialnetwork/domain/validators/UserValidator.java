package com.example.socialnetwork.domain.validators;

import com.example.socialnetwork.domain.User;

public class UserValidator implements Validator<User>{
    /**
     * Validates a user
     * @param user to be validated
     * @throws ValidationException if user is invalid
     */
    public void validate(User user) throws ValidationException {
        String errors = "";
        //errors = idValidate(errors, user.getID());
        errors = first_nameValidate(errors, user.getFirst_name());
        errors = last_nameValidate(errors, user.getLast_name());
        errors = emailValidate(errors, user.getEmail());
        errors =  passwordValidate(errors, user.getPassword());
        if(!errors.equals("")){
            throw new ValidationException(errors);
        }
    }

    /**
     * Validates the password of a user
     * @param errors which are found
     * @param password to validate
     */
    public static String passwordValidate(String errors, String password) {
        for(char ch : password.toCharArray()){
            if(ch == ' '){
                errors += "Password cannot include spaces\n";
                return errors;
            }
        }
        if(password.length() < 5 || password.length() > 15){
            errors += "Password length needs to be between 5 and 15 characters\n";
        }
        return errors;
    }

    /**
     * Validates email of a user
     * @param errors which are found
     * @param email to validate
     */
    public static String emailValidate(String errors, String email) {
        boolean found_at = false, found_dot = false;
        for(char ch : email.toCharArray()){
            if(ch == ' '){
                errors += "Email cannot include spaces\n";
                return errors;
            }else if(ch == '@'){
                found_at = true;
            } else if(ch == '.' && found_at){
                found_dot = true;
            }
        }
        if(!found_at){
            errors += "Email needs to include @\n";
        }
        if(!found_dot && found_at){
            errors += "Email needs to include dot\n";
        }
        return errors;

    }

    /**
     * Validates ID of a user
     * @param errors which are found
     * @param ID to validate
     */
//    public static String idValidate(String errors, UUID ID){
//       if(ID <= 0)
//          errors += "ID cannot be less than zero";
//        ;
//        return errors;
//    }

    /**
     * Validates first name of a user
     * @param errors which are found
     * @param first_name to validate
     */
    public static String first_nameValidate(String errors, String first_name) {
        if(first_name.equals("")){
            errors += "First name cannot be null\n";
            return errors;
        }
        for(char ch : first_name.toCharArray()){
            if(ch == ' '){
                errors += "First name cannot include spaces\n";
                return errors;
            }
        }
        return errors;
    }

    /**
     * Validates last name of user
     * @param errors which are found
     * @param last_name to validate
     */
    public static String last_nameValidate(String errors, String last_name){
        if(last_name.equals("")){
            errors += "Last name cannot be null\n";
            return errors;
        }
        for(char ch : last_name.toCharArray()){
            if(ch == ' '){
                errors += "Last name cannot include spaces\n";
                return errors;
            }
        }
        return errors;
    }
}
