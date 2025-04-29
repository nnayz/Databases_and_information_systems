package com.example.estate.dao;

import com.example.estate.db.DBConnection;
import com.example.estate.model.Apartment;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ApartmentDAO {

    public void create(Apartment a) throws SQLException {
        Connection c = DBConnection.get();
        c.setAutoCommit(false);
        try {
            try (PreparedStatement pst = c.prepareStatement(
                    "INSERT INTO estate(city, postal_code, street, street_number, square_area, agent_id) " +
                    "VALUES (?,?,?,?,?,?)", Statement.RETURN_GENERATED_KEYS)) {
                pst.setString(1, a.getCity());
                pst.setString(2, a.getPostalCode());
                pst.setString(3, a.getStreet());
                pst.setString(4, a.getStreetNumber());
                pst.setDouble(5, a.getSquareArea());
                pst.setInt(6, a.getAgentId());
                pst.executeUpdate();
                try (ResultSet rs = pst.getGeneratedKeys()) {
                    if (rs.next()) a.setId(rs.getInt(1));
                }
            }
            try (PreparedStatement pst = c.prepareStatement(
                    "INSERT INTO apartment(estate_id,floor_number,rent,rooms,balcony,built_in_kitchen) VALUES (?,?,?,?,?,?)")) {
                pst.setInt(1, a.getId());
                pst.setInt(2, a.getFloor());
                pst.setDouble(3, a.getRent());
                pst.setInt(4, a.getRooms());
                pst.setBoolean(5, a.isBalcony());
                pst.setBoolean(6, a.isBuiltInKitchen());
                pst.executeUpdate();
            }
            c.commit();
        } catch (SQLException e) {
            c.rollback();
            throw e;
        } finally {
            c.setAutoCommit(true);
        }
    }

    public List<Apartment> findByAgent(int agentId) throws SQLException {
        String sql = 
            "SELECT e.*, ap.* FROM estate e " +
            "JOIN apartment ap ON ap.estate_id=e.estate_id " +
            "WHERE e.agent_id=?";
        List<Apartment> list = new ArrayList<>();
        try (Connection c = DBConnection.get(); PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setInt(1, agentId);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    list.add(map(rs));
                }
            }
        }
        return list;
    }

    public void delete(int estateId) throws SQLException {
        try (Connection c = DBConnection.get();
             PreparedStatement ps = c.prepareStatement("DELETE FROM estate WHERE estate_id=?")) {
            ps.setInt(1, estateId);
            ps.executeUpdate();
        }
    }

    private Apartment map(ResultSet rs) throws SQLException {
        return new Apartment(
            rs.getInt("apartment_id"),
            rs.getString("city"),
            rs.getString("postal_code"),
            rs.getString("street"),
            rs.getString("street_number"),
            rs.getDouble("square_area"),
            rs.getInt("agent_id"),
            rs.getInt("floor_number"),
            rs.getDouble("rent"),
            rs.getInt("rooms"),
            rs.getBoolean("balcony"),
            rs.getBoolean("built_in_kitchen")
        );
    }
}
