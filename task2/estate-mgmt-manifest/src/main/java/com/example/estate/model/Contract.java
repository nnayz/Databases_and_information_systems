package com.example.estate.model;

import java.time.LocalDate;

public class Contract {
    private int id;
    private int contractNo;
    private LocalDate date;
    private String place;
  

    public Contract() {}
    public Contract(LocalDate date, String place) {
        this(0, date, place);  
    }

    public Contract(int contractNo, LocalDate date, String place) {
        this.contractNo = contractNo;
        this.date = date;
        this.place = place;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public int getContractNo() { return contractNo; }
    public void setContractNo(int no) { this.contractNo = no; }
    public LocalDate getDate() { return date; }
    public void setDate(LocalDate d) { this.date = d; }
    public String getPlace() { return place; }
    public void setPlace(String p) { this.place = p; }

}
