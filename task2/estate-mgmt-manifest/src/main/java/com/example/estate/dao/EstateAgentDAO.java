package com.example.estate.dao;

import com.example.estate.db.DBConnection;
import com.example.estate.model.EstateAgent;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class EstateAgentDAO {
    private static EstateAgent map(ResultSet rs) throws SQLException {
        return new EstateAgent(
            rs.getInt("agent_id"),
            rs.getString("name"),
            rs.getString("address"),
            rs.getString("username"),
            rs.getString("password")
        );
    }

    public void create(EstateAgent a) throws SQLException {
        String sql = "INSERT INTO estateagent(name,address,username,password) VALUES (?,?,?,?)";
        try (Connection c = DBConnection.get(); PreparedStatement ps =
                c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, a.getName());
            ps.setString(2, a.getAddress());
            ps.setString(3, a.getLogin());
            ps.setString(4, a.getPassword());
            ps.executeUpdate();
            try (ResultSet rs = ps.getGeneratedKeys()) { if (rs.next()) a.setId(rs.getInt(1)); }
                }
        // } catch (SQLException ex) {
            
        //     if ("23505".equals(ex.getSQLState())) {
        //         throw new IllegalArgumentException("Username already in use.", ex);
        //     }
        //     throw ex;   
        // }
    }

    public EstateAgent findByLogin(String login) throws SQLException {
        String sql = "SELECT * FROM estateagent WHERE username=?";
        try (Connection c = DBConnection.get(); PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, login);
            try (ResultSet rs = ps.executeQuery()) { if (rs.next()) return map(rs); }
        }
        return null;
    }

    public List<EstateAgent> findAll() throws SQLException {
        List<EstateAgent> list = new ArrayList<>();
        try (Connection c = DBConnection.get(); Statement st = c.createStatement();
             ResultSet rs = st.executeQuery("SELECT * FROM estateagent ORDER BY agent_id")) {
            while (rs.next()) list.add(map(rs));
        }
        return list;
    }

    public void update(EstateAgent a) throws SQLException {
        String sql = "UPDATE estateagent SET name=?, address=?, password=? WHERE agent_id=?";
        try (Connection c = DBConnection.get(); PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, a.getName());
            ps.setString(2, a.getAddress());
            ps.setString(3, a.getPassword());
            ps.setInt(4, a.getId());
            ps.executeUpdate();
        }
    }

    public void delete(int username) throws SQLException {
        try (Connection c = DBConnection.get(); PreparedStatement ps =
                c.prepareStatement("DELETE FROM estateagent WHERE username=?")) {
            ps.setInt(1, username);
            ps.executeUpdate();
        }
    }
}
