package com.example.socialnetwork.controller;

import com.example.socialnetwork.MainApplication;
import com.example.socialnetwork.business.SocialNetwork;
import com.example.socialnetwork.domain.Friendship;
import com.example.socialnetwork.domain.User;
import com.example.socialnetwork.domain.validators.ValidationException;
import com.example.socialnetwork.repository.RepositoryException;
import com.example.socialnetwork.utils.events.UserEntityChangeEvent;
import com.example.socialnetwork.utils.observer.Observer;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

import java.io.IOException;
import java.util.ArrayList;

public class UserController implements Observer<UserEntityChangeEvent> {
    SocialNetwork socialNetwork;
    ObservableList<User> model = FXCollections.observableArrayList();
    ArrayList<LoginController> loggedUsers = new ArrayList<>();
    private static final int MAX_USERS_TABLE_ITEMS = 7;
    private int current_page, page_before_filter;
    private boolean filtering_status = false;
    private String filtering_FirstName = null;
    @FXML
    TableView<User> tableView_Users;
    @FXML
    TableColumn<User, String> tableColumn_Users_FirstName;
    @FXML
    TableColumn<User, String> tableColumn_Users_LastName;
    @FXML
    TableColumn<User, String> tableColumn_Users_Email;
    @FXML
    TextField textField_FirstName_CRUD;
    @FXML
    TextField textField_LastName_CRUD;
    @FXML
    PasswordField passwordField_Password_CRUD;
    @FXML
    TextField textField_Email_CRUD;
    @FXML
    Label label_UsersPage;
    @FXML
    TextField textField_FirstName_Filter;
    @FXML
    TextField textField_Email_Login;
    @FXML
    PasswordField passwordField_Password_Login;

    /**
     * Initializes the model
     * @param filtering_status whether there is filtering in progress or not
     */
    private void initModel(boolean filtering_status) {
        ArrayList<User> users_to_show = null;
        if(!filtering_status){
            users_to_show = socialNetwork.getUsers();
        } else{
            try{
                users_to_show = socialNetwork.filterByFirstName(filtering_FirstName);
            } catch(RepositoryException e){
                AlertMessage.showErrorMessage(null, e.getMessage());
            } catch(ValidationException e){
                AlertMessage.showErrorMessage(null, e.getMessage());
            }
        }

        model.setAll(users_to_show);
    }

    @FXML
    public void initialize(){
        initializeUsersTable();
    }

    private void initializeUsersTable() {
        tableColumn_Users_FirstName.setCellValueFactory(new PropertyValueFactory<User, String>("First_name"));
        tableColumn_Users_LastName.setCellValueFactory(new PropertyValueFactory<User, String>("Last_name"));
        tableColumn_Users_Email.setCellValueFactory(new PropertyValueFactory<User, String>("Email"));
        FilteredList<User> firstUserPage = getUsersPage(1);
        tableView_Users.setItems(firstUserPage);
        updateUsersTableOnSelectionEvent();
    }

    public void setSocialNetwork(SocialNetwork socialNetwork){
        current_page = 1;
        label_UsersPage.setText(Integer.toString(current_page));
        this.socialNetwork = socialNetwork;
        socialNetwork.addObserver(this);
        initModel(false);
    }

    @Override
    public void update(UserEntityChangeEvent userEntityChangeEvent) {
        initModel(filtering_status);
    }



    public void handleLogin(ActionEvent actionEvent){
        String login_email = textField_Email_Login.getText();
        String login_password = passwordField_Password_Login.getText();
        try{
            User login_user = socialNetwork.getUser(login_email);
            if(!login_user.getPassword().equals(login_password)){
                throw new RepositoryException("Wrong password");
            }
            FXMLLoader fxmlLoader = new FXMLLoader(MainApplication.class.getResource("views/LoginView.fxml"));
            Parent loginLayout = fxmlLoader.load();
            Stage loginStage = new Stage();
            loginStage.setScene(new Scene(loginLayout));
            loginStage.initStyle(StageStyle.DECORATED);
            LoginController loginController = fxmlLoader.getController();
            loginController.setLoggedUser(login_user);
            loginController.setSocialNetwork(socialNetwork);
            if(!loggedUsers.contains(loginController)){
                loggedUsers.add(loginController);
            }
            loginController.setStage(loginStage);
            updateUsersTableOnSelectionEvent();
            loginStage.show();
        } catch(RepositoryException e){
            AlertMessage.showErrorMessage(null, e.getMessage());
        } catch(IOException e){
            System.out.println(e.getMessage());
        }
    }

    private void updateUsersTableOnSelectionEvent() {
        tableView_Users.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                User selected_user = tableView_Users.getSelectionModel().getSelectedItem();
                String first_name = selected_user.getFirst_name();
                String last_name = selected_user.getLast_name();
                String password = selected_user.getPassword();
                String email = selected_user.getEmail();
                textField_FirstName_CRUD.setText(first_name);
                textField_LastName_CRUD.setText(last_name);
                passwordField_Password_CRUD.setText(password);
                textField_Email_CRUD.setText(email);
                for(LoginController loginController : loggedUsers){
                    loginController.getTextField_Email_SendFriendRequest().setText(email);
                }
            }
        });
    }

    public void handleShowUsers(ActionEvent actionEvent){
        current_page = page_before_filter;
        model.setAll(socialNetwork.getUsers());
        updateUsersTableItemsAndItsLabel(current_page);
        filtering_status = false;
    }

    public void handleAddUser(ActionEvent actionEvent){
        String first_name = textField_FirstName_CRUD.getText();
        String last_name = textField_LastName_CRUD.getText();
        String email = textField_Email_CRUD.getText();
        String password = passwordField_Password_CRUD.getText();
        try{
            socialNetwork.saveUser(first_name, last_name, email, password);
        } catch(RepositoryException e){
            AlertMessage.showErrorMessage(null, e.getMessage());
        } catch(ValidationException e){
            AlertMessage.showErrorMessage(null, e.getMessage());
        }
    }

    public void handleFilterUser(ActionEvent actionEvent){
        String first_name = textField_FirstName_Filter.getText();
        try{
            ArrayList<User> filtered_users = socialNetwork.filterByFirstName(first_name);
            model.setAll(filtered_users);
            page_before_filter = current_page;
            current_page = 1;
            updateUsersTableItemsAndItsLabel(current_page);
            filtering_status = true;
            filtering_FirstName = first_name;
        } catch (RepositoryException e){
            AlertMessage.showErrorMessage(null, e.getMessage());
        } catch (ValidationException e){
            AlertMessage.showErrorMessage(null, e.getMessage());
        }
    }

    private void updateUsersTableItemsAndItsLabel(int page){
        label_UsersPage.setText(Integer.toString(page));
        tableView_Users.setItems(getUsersPage(page));
    }

    public void handleDeleteUser(ActionEvent actionEvent){
        String first_name = textField_FirstName_CRUD.getText();
        String last_name = textField_LastName_CRUD.getText();
        String email = textField_Email_CRUD.getText();
        String password = passwordField_Password_CRUD.getText();
        try{
            socialNetwork.deleteUser(email);
        } catch(RepositoryException e){
            AlertMessage.showErrorMessage(null, e.getMessage());
        } catch(ValidationException e){
            AlertMessage.showErrorMessage(null, e.getMessage());
        }
    }

    public void handleTurnToFirstPage(ActionEvent actionEvent){
        current_page = 1;
        updateUsersTableItemsAndItsLabel(current_page);
    }
    public void handleTurnToBackPage(ActionEvent actionEvent){
        if(current_page == 1){
            AlertMessage.showErrorMessage(null, "No page to turn to!");
            return;
        }
        current_page--;
        updateUsersTableItemsAndItsLabel(current_page);
    }
    public void handleTurnToNextPage(ActionEvent actionEvent){
        if(current_page == getMaxUsersPage()){
            AlertMessage.showErrorMessage(null, "No page to turn to!");
            return;
        }
        current_page++;
        updateUsersTableItemsAndItsLabel(current_page);
    }
    public void handleTurnToLastPage(ActionEvent actionEvent){
        current_page = getMaxUsersPage();
        updateUsersTableItemsAndItsLabel(current_page);
    }
    private FilteredList<User> getUsersPage(int page_number){
        FilteredList<User> userPage = new FilteredList<>(
                model, user -> model.indexOf(user) < MAX_USERS_TABLE_ITEMS * page_number && model.indexOf(user) >= MAX_USERS_TABLE_ITEMS * (page_number - 1)
        );
        return userPage;
    }
    private int getMaxUsersPage(){
        int maxUsersPage = model.size() / MAX_USERS_TABLE_ITEMS;
        if(model.size() % MAX_USERS_TABLE_ITEMS != 0){
            maxUsersPage++;
        }
        return maxUsersPage;
    }

}
