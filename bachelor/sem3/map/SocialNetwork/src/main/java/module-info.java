module com.example.socialnetwork {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;
    requires com.dlsc.formsfx;
    requires org.kordamp.bootstrapfx.core;
    requires java.sql;

    opens com.example.socialnetwork to javafx.fxml;
    opens com.example.socialnetwork.controller to javafx.fxml;
    opens com.example.socialnetwork.repository to javafx.fxml;
    opens com.example.socialnetwork.business to javafx.fxml;
    opens com.example.socialnetwork.domain to javafx.fxml;

    exports com.example.socialnetwork;
    exports com.example.socialnetwork.controller;
    exports com.example.socialnetwork.repository;
    exports com.example.socialnetwork.business;
    exports com.example.socialnetwork.domain;
}