package com.example.estate.dao;

import com.example.estate.db.DBConnection;
import com.example.estate.model.House;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class HouseDAO {

    public void create(House h) throws SQLException {
        Connection c = DBConnection.get();
        c.setAutoCommit(false);
        try {
            try (PreparedStatement pst = c.prepareStatement(
                    "INSERT INTO estate(city, postal_code, street, street_number, square_area, agent_id) " +
                    "VALUES (?,?,?,?,?,?)", Statement.RETURN_GENERATED_KEYS)) {
                pst.setString(1, h.getCity());
                pst.setString(2, h.getPostalCode());
                pst.setString(3, h.getStreet());
                pst.setString(4, h.getStreetNumber());
                pst.setDouble(5, h.getSquareArea());
                pst.setInt(6, h.getAgentId());
                pst.executeUpdate();
                try (ResultSet rs = pst.getGeneratedKeys()) {
                    if (rs.next()) h.setId(rs.getInt(1));
                }
            }
            try (PreparedStatement pst = c.prepareStatement(
                    "INSERT INTO house(estate_id,floors,price,garden) VALUES (?,?,?,?)")) {
                pst.setInt(1, h.getId());
                pst.setInt(2, h.getFloors());
                pst.setDouble(3, h.getPrice());
                pst.setBoolean(4, h.isGarden());
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

    public List<House> findByAgent(int agentId) throws SQLException {
        String sql = 
            "SELECT e.*, h.* FROM estate e " +
            "JOIN house h ON h.estate_id=e.id WHERE e.agent_id=?";
        List<House> list = new ArrayList<>();
        try (Connection c = DBConnection.get(); PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setInt(1, agentId);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) list.add(map(rs));
            }
        }
        return list;
    }

    public void delete(int estateId) throws SQLException {
        try (Connection c = DBConnection.get();
             PreparedStatement ps = c.prepareStatement("DELETE FROM estate WHERE id=?")) {
            ps.setInt(1, estateId);
            ps.executeUpdate();
        }
    }

    private House map(ResultSet rs) throws SQLException {
        return new House(
            rs.getInt("id"),
            rs.getString("city"),
            rs.getString("postal_code"),
            rs.getString("street"),
            rs.getString("street_number"),
            rs.getDouble("square_area"),
            rs.getInt("agent_id"),
            rs.getInt("floors"),
            rs.getDouble("price"),
            rs.getBoolean("garden")
        );
    }
}
