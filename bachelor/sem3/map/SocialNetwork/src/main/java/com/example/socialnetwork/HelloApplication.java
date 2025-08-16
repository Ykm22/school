package com.example.socialnetwork;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Group;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.HBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Rectangle;
import javafx.stage.Stage;

import java.io.IOException;

public class HelloApplication extends Application {
    @Override
    public void start(Stage stage) throws IOException {
//        FXMLLoader fxmlLoader = new FXMLLoader(HelloApplication.class.getResource("hello-view.fxml"));
//        Scene scene = new Scene(fxmlLoader.load(), 320, 240);
//        stage.setTitle("Hello!");
//        stage.setScene(scene);
//        stage.show();
        Group root = new Group();

        Rectangle r = new Rectangle(25, 25, 100, 100);
        Circle c = new Circle(50, 50, 50, Color.web("blue", 0.5f));
        r.setFill(Color.BLUE);
        root.getChildren().add(r);
        root.getChildren().add(c);

        HBox root2 = new HBox(5);
        root2.setPadding(new Insets(200));
        root2.setAlignment(Pos.BASELINE_RIGHT);

        Button prevBtn = new Button("Previous");
        Button nextBtn = new Button("Next");
        root2.getChildren().addAll(prevBtn, nextBtn);

        AnchorPane root3 = new AnchorPane();
        HBox hBox = new HBox(5, prevBtn, nextBtn);
        AnchorPane.setRightAnchor(hBox, 100d);
        AnchorPane.setBottomAnchor(hBox, 10d);
        root3.getChildren().add(hBox);

        Scene scene = new Scene( root3 , 500 , 500 , Color.PINK);
        stage.setTitle("Welcome");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) { launch();}
}