package com.example.socialnetwork;

import com.example.socialnetwork.business.SocialNetwork;
import com.example.socialnetwork.controller.UserController;
import com.example.socialnetwork.repository.DBRepository;
import com.example.socialnetwork.repository.Repository;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;

import java.io.IOException;

public class MainApplication extends Application {
    SocialNetwork service;
    Repository repository;
    @Override
    public void start(Stage primaryStage) throws IOException {
        String url = "jdbc:postgresql://localhost:5432/SocialNetwork";
        repository = new DBRepository(url, "postgres", "postgres");
        repository.getAllUsers().forEach(System.out::println);
        service = new SocialNetwork(repository);
        initView(primaryStage);
        primaryStage.show();
    }

    private void initView(Stage primaryStage) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(MainApplication.class.getResource("views/UserView.fxml"));
        AnchorPane userLayout = fxmlLoader.load();
        primaryStage.setScene(new Scene(userLayout));
        UserController userController = fxmlLoader.getController();
        userController.setSocialNetwork(service);
    }

    public static void main(String[] args){
        launch(args);
    }
}
