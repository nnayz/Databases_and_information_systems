package com.example.estate.dao;

import com.example.estate.db.DBConnection;
import com.example.estate.model.*;

import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class ContractDAO {

    public int createContract(Contract c) throws SQLException {
        String sql = "INSERT INTO contract(contract_date,place) VALUES (?,?)";
        Connection con = DBConnection.get();
        try (
             PreparedStatement ps = con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setDate(1, Date.valueOf(c.getDate()));
            ps.setString(2, c.getPlace());
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
        Connection con = DBConnection.get();
        con.setAutoCommit(false);
        int cid = createContract(tc);
        String sql = "INSERT INTO tenancy_contract(contract_no,start_date,duration,additional_costs, person_id, apartment_id) VALUES (?,?,?,?,?,?)";
        try (
             PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, cid);
            ps.setDate(2, Date.valueOf(tc.getStartDate()));
            ps.setInt(3, tc.getDuration());
            ps.setDouble(4, tc.getAdditionalCosts());
            ps.setInt(5, tc.getPersonId());
            ps.setInt(6, tc.getEstateId());
            ps.executeUpdate();
        }
        con.commit();
        con.setAutoCommit(true);
    }

    public void createPurchase(PurchaseContract pc) throws SQLException {
        int cid = createContract(pc);
        String sql = "INSERT INTO purchase_contract(contract_no,no_of_installments,interest_rate, person_id, house_id) VALUES (?,?,?,?,?)";
        Connection con = DBConnection.get();
        try (
             PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, cid);
            ps.setInt(2, pc.getInstallments());
            ps.setDouble(3, pc.getInterestRate());
            ps.setInt(4, pc.getPersonId());
            ps.setInt(5, pc.getEstateId());
            ps.executeUpdate();
        }
    }

    public List<String> overview() throws SQLException {
        List<String> list = new ArrayList<>();
        String sql = 
        
        "SELECT c.contract_no, 'tenancy'          AS type, " +
        "       p.first_name || ' ' || p.name     AS person, " +
        "       e.city, e.street, e.street_number           " +
        "FROM   contract           c                          " +
        "JOIN   tenancy_contract   t  ON t.contract_no = c.contract_no " +
        "JOIN   person             p  ON p.person_id  = t.person_id    " +
        "JOIN   apartment          a  ON a.estate_id  = t.apartment_id " +
        "JOIN   estate             e  ON e.estate_id  = a.estate_id    " +

        "UNION ALL                                                 " +

        "SELECT c.contract_no, 'purchase'         AS type, " +
        "       p.first_name || ' ' || p.name     AS person, " +
        "       e.city, e.street, e.street_number           " +
        "FROM   contract            c                         " +
        "JOIN   purchase_contract   pc ON pc.contract_no = c.contract_no " +
        "JOIN   person              p  ON p.person_id  = pc.person_id    " +
        "JOIN   house               h  ON h.estate_id  = pc.house_id     " +
        "JOIN   estate              e  ON e.estate_id  = h.estate_id     " +
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
