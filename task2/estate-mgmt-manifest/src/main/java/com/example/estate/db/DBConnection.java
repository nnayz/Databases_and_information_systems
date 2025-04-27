package com.example.estate.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.io.InputStream;
import java.util.Properties;

public final class DBConnection {
    private static Connection instance;

    private DBConnection() {}

    public static Connection get() throws SQLException {
        if (instance == null || instance.isClosed()) {
            try (InputStream in = DBConnection.class.getClassLoader().getResourceAsStream("db.properties")) {
                if (in == null) throw new IllegalStateException("db.properties not found");
                Properties props = new Properties();
                props.load(in);
                instance = DriverManager.getConnection(props.getProperty("url"), props);
            } catch (Exception e) {
                throw new SQLException(e);
            }
        }
        return instance;
    }
}
