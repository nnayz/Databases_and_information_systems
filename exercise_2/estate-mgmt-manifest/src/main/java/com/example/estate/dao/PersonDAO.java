package com.example.estate.dao;

import com.example.estate.db.DBConnection;
import com.example.estate.model.Person;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class PersonDAO {
    public void create(Person p) throws SQLException {
        String sql = "INSERT INTO person(first_name,name,address) VALUES (?,?,?)";
        Connection c = DBConnection.get();
        try (
             PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, p.getFirstName());
            ps.setString(2, p.getName());
            ps.setString(3, p.getAddress());
            ps.executeUpdate();
            try (ResultSet rs = ps.getGeneratedKeys()) {
                if (rs.next()) p.setId(rs.getInt(1));
            }
        }
    }

    public List<Person> all() throws SQLException {
        List<Person> list = new ArrayList<>();
        Connection c = DBConnection.get();
        try (
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery("SELECT * FROM person ORDER BY person_id")) {
            while (rs.next()) {
                list.add(new Person(rs.getInt("person_id"), rs.getString("first_name"),
                        rs.getString("name"), rs.getString("address")));
            }
        }
        return list;
    }
}
