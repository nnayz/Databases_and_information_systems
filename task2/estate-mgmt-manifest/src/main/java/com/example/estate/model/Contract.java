package com.example.estate.model;

import java.time.LocalDate;

public class Contract {
    private int id;
    private int contractNo;
    private LocalDate date;
    private String place;
    private int personId;
    private int estateId;

    public Contract() {}
    public Contract(int id, int contractNo, LocalDate date, String place,
                    int personId, int estateId) {
        this.id = id; this.contractNo = contractNo; this.date = date;
        this.place = place; this.personId = personId; this.estateId = estateId;
    }
    public Contract(int contractNo, LocalDate date, String place,
                    int personId, int estateId) {
        this(0, contractNo, date, place, personId, estateId);
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public int getContractNo() { return contractNo; }
    public void setContractNo(int no) { this.contractNo = no; }
    public LocalDate getDate() { return date; }
    public void setDate(LocalDate d) { this.date = d; }
    public String getPlace() { return place; }
    public void setPlace(String p) { this.place = p; }
    public int getPersonId() { return personId; }
    public void setPersonId(int pid) { this.personId = pid; }
    public int getEstateId() { return estateId; }
    public void setEstateId(int eid) { this.estateId = eid; }
}
