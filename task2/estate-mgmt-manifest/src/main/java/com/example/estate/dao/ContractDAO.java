package com.example.estate.dao;

import com.example.estate.db.DBConnection;
import com.example.estate.model.*;

import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class ContractDAO {

    public int createContract(Contract c) throws SQLException {
        String sql = "INSERT INTO contract(date,place,person_id,estate_id) VALUES (?,?,?,?,?)";
        Connection con = DBConnection.get();
        try (
             PreparedStatement ps = con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setDate(2, Date.valueOf(c.getDate()));
            ps.setString(3, c.getPlace());
            ps.setInt(4, c.getPersonId());
            ps.setInt(5, c.getEstateId());
            ps.executeUpdate();
            try (ResultSet rs = ps.getGeneratedKeys()) {
                if (rs.next()) {
                    int contract_no = rs.getInt(1);
                    c.setContractNo(contract_no);
                    return contract_no;
                }
            }
        }
        return 0;
    }

    public void createTenancy(TenancyContract tc) throws SQLException {
        int cid = createContract(tc);
        String sql = "INSERT INTO tenancycontract(contract_no,start_date,duration,additional_costs) VALUES (?,?,?,?)";
        Connection con = DBConnection.get();
        try (
             PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, cid);
            ps.setDate(2, Date.valueOf(tc.getStartDate()));
            ps.setInt(3, tc.getDuration());
            ps.setDouble(4, tc.getAdditionalCosts());
            ps.executeUpdate();
        }
    }

    public void createPurchase(PurchaseContract pc) throws SQLException {
        int cid = createContract(pc);
        String sql = "INSERT INTO purchasecontract(contract_no,installments,interest_rate) VALUES (?,?,?)";
        Connection con = DBConnection.get();
        try (
             PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, cid);
            ps.setInt(2, pc.getInstallments());
            ps.setDouble(3, pc.getInterestRate());
            ps.executeUpdate();
        }
    }

    public List<String> overview() throws SQLException {
        List<String> list = new ArrayList<>();
        String sql = 
            "SELECT c.contract_no, 'tenancy' AS type, p.first_name||' '||p.name AS person, e.city, e.street, e.street_number " +
            "FROM contract c " +
            "JOIN tenancy_contract t ON t.contract_id=c.id " +
            "JOIN person p ON p.id=c.person_id " +
            "JOIN estate e ON e.id=c.estate_id " +
            "UNION ALL " +
            "SELECT c.contract_no, 'purchase', p.first_name||' '||p.name, e.city, e.street, e.street_number " +
            "FROM contract c " +
            "JOIN purchase_contract pc ON pc.contract_id=c.id " +
            "JOIN person p ON p.id=c.person_id " +
            "JOIN estate e ON e.id=c.estate_id " +
            "ORDER BY contract_no";
        Connection con = DBConnection.get();
        
        try (
             Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                list.add(String.format("%s (%s) – %s – %s %s %s",
                    rs.getString(1), rs.getString(2), rs.getString(3),
                    rs.getString(4), rs.getString(5), rs.getString(6)));
            }
        }
        return list;
    }
}
