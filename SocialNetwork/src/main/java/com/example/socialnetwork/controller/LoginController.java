package com.example.socialnetwork.controller;

import com.example.socialnetwork.business.SocialNetwork;
import com.example.socialnetwork.domain.Friendship;
import com.example.socialnetwork.domain.FriendshipStatus;
import com.example.socialnetwork.domain.User;
import com.example.socialnetwork.domain.validators.ValidationException;
import com.example.socialnetwork.repository.RepositoryException;
import com.example.socialnetwork.utils.events.FriendshipEntityChangeEvent;
import com.example.socialnetwork.utils.events.UserEntityChangeEvent;
import com.example.socialnetwork.utils.observer.Observer;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.MouseEvent;
import javafx.stage.Stage;

import java.time.LocalDateTime;
import java.util.ArrayList;

public class LoginController implements Observer<UserEntityChangeEvent> {
    SocialNetwork socialNetwork;
    ObservableList<Friendship> model = FXCollections.observableArrayList();
    private int current_page = 1;
    private static final int MAX_FRIENDSHIPS_TABLE_ITEMS = 10;
    private User logged_user;
    private Stage loginStage;
    @FXML
    Label label_FriendshipsPage;
    @FXML
    TableView<Friendship> tableView_Friendships;
    @FXML
    TableColumn<Friendship, String> tableColumn_Friendships_EmailSender;
    @FXML
    TableColumn<Friendship, String> tableColumn_Friendships_EmailReceiver;
    @FXML
    TableColumn<Friendship, String> tableColumn_Friendships_FriendsFrom;
    @FXML
    TableColumn<Friendship, String> tableColumn_Friendships_Status;
    @FXML
    TextField textField_Email_ModifyRequest;
    @FXML
    Label label_LoggedUser;
    @FXML
    TextField textField_Email_SendFriendRequest;

    public void setStage(Stage stage){
        loginStage = stage;
    }

    public TextField getTextField_Email_SendFriendRequest(){
        return textField_Email_SendFriendRequest;
    }

    private void initModel() {
        model.setAll(socialNetwork.getFriendshipsOfUser(logged_user));
    }

    @FXML
    private void initialize(){
        tableColumn_Friendships_EmailSender.setCellValueFactory(new PropertyValueFactory<Friendship, String>("Email1"));
        tableColumn_Friendships_EmailReceiver.setCellValueFactory(new PropertyValueFactory<Friendship, String>("Email2"));
        tableColumn_Friendships_FriendsFrom.setCellValueFactory(new PropertyValueFactory<Friendship, String>("FriendsFrom"));
        tableColumn_Friendships_Status.setCellValueFactory(new PropertyValueFactory<Friendship, String>("Status"));
        FilteredList<Friendship> firstFriendshipsPage = getFriendshipsPage(1);
        tableView_Friendships.setItems(firstFriendshipsPage);
        label_FriendshipsPage.setText(Integer.toString(current_page));
        tableView_Friendships.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                Friendship selected_friendship = tableView_Friendships.getSelectionModel().getSelectedItem();
                String email_friend = null;
                if(selected_friendship.getEmail1().equals(logged_user.getEmail())){
                    email_friend = selected_friendship.getEmail2();
                } else{
                    email_friend = selected_friendship.getEmail1();
                }
                textField_Email_ModifyRequest.setText(email_friend);
            }
        });
    }

    public void setSocialNetwork(SocialNetwork socialNetwork) {
        //updateFriendshipsTableItemsAndItsLabel(current_page);
        this.socialNetwork = socialNetwork;
        socialNetwork.addObserver(this);
        initModel();
    }
    public void setLoggedUser(User user){
        logged_user = user;
        label_LoggedUser.setText(user.getEmail());
    }

    public void update(UserEntityChangeEvent event){
        initModel();
    }

    public void handleSendFriendRequest(ActionEvent actionEvent){
        String email_receiver = textField_Email_SendFriendRequest.getText();
        try{
            socialNetwork.saveFriend(logged_user.getEmail(), email_receiver, LocalDateTime.now(), "PENDING");
        } catch(RepositoryException e){
            AlertMessage.showErrorMessage(null, e.getMessage());
        } catch(ValidationException e){
            AlertMessage.showErrorMessage(null, e.getMessage());
        }
    }

    public void handleAcceptFriendRequest(ActionEvent actionEvent){
        String email_sender = textField_Email_ModifyRequest.getText();
        try{
            User user_sender = socialNetwork.getUser(email_sender);
            socialNetwork.updateFriendship(user_sender, logged_user, FriendshipStatus.ACCEPTED);
        } catch(RepositoryException e){
            AlertMessage.showErrorMessage(null, e.getMessage());
        }

    }

    public void handleDeleteFriend(ActionEvent actionEvent){
        try{
            String email_to_delete = textField_Email_ModifyRequest.getText();
            User user_to_delete = socialNetwork.getUser(email_to_delete);
            for(Friendship friendship : socialNetwork.getFriendshipsOfUser(logged_user)) {
                if (friendship.getEmail1().equals(logged_user.getEmail()) && friendship.getEmail2().equals(user_to_delete.getEmail())) {
//                    System.out.println("intrat1");
                    socialNetwork.updateFriendship(logged_user, user_to_delete, FriendshipStatus.DECLINED);
//                    System.out.println("iesit1");
                    return;
                }
                if (friendship.getEmail1().equals(user_to_delete.getEmail()) && friendship.getEmail2().equals(logged_user.getEmail())) {
//                    System.out.println("intrat2");
                    socialNetwork.updateFriendship(user_to_delete, logged_user, FriendshipStatus.DECLINED);
//                    System.out.println("iesit2");
                    return;
                }
            }
        } catch(RepositoryException e){
            AlertMessage.showErrorMessage(null, e.getMessage());
        }
    }

    public void handleLogout(ActionEvent actionEvent){
        loginStage.close();
    }

    public void handleTurnToFirstPage(ActionEvent actionEvent){
        current_page = 1;
        updateFriendshipsTableItemsAndItsLabel(current_page);
    }
    public void handleTurnToBackPage(ActionEvent actionEvent){
        if(current_page == 1){
            AlertMessage.showErrorMessage(null, "No page to turn to!");
            return;
        }
        current_page--;
        updateFriendshipsTableItemsAndItsLabel(current_page);
    }
    public void handleTurnToNextPage(ActionEvent actionEvent){
        if(current_page == getMaxFriendshipsPage()){
            AlertMessage.showErrorMessage(null, "No page to turn to!");
            return;
        }
        current_page++;
        updateFriendshipsTableItemsAndItsLabel(current_page);
    }
    public void handleTurnToLastPage(ActionEvent actionEvent){
        current_page = getMaxFriendshipsPage();
        updateFriendshipsTableItemsAndItsLabel(current_page);
    }

    private void updateFriendshipsTableItemsAndItsLabel(int page){
        label_FriendshipsPage.setText(Integer.toString(page));
        tableView_Friendships.setItems(getFriendshipsPage(page));
    }

    private FilteredList<Friendship> getFriendshipsPage(int page) {
        FilteredList<Friendship> friendshipsPage = new FilteredList<>(
                model, friendship -> model.indexOf(friendship) < MAX_FRIENDSHIPS_TABLE_ITEMS * page && model.indexOf(friendship) >= MAX_FRIENDSHIPS_TABLE_ITEMS * (page - 1)
        );
        return friendshipsPage;
    }
    private int getMaxFriendshipsPage(){
        int maxFriendshipsPage = model.size() / MAX_FRIENDSHIPS_TABLE_ITEMS;
        if(maxFriendshipsPage == 0 || model.size() % MAX_FRIENDSHIPS_TABLE_ITEMS != 0){
            maxFriendshipsPage++;
        }
        return maxFriendshipsPage;
    }
}
