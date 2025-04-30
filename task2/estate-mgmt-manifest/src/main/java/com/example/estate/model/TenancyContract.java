package com.example.estate.model;

import java.time.LocalDate;

public class TenancyContract extends Contract {
    private LocalDate startDate;
    private int duration;
    private double additionalCosts;
    private int personId;    
    private int apartmentId;
    public TenancyContract() {}
    public TenancyContract(int contractNo, LocalDate date, String place,
    int personId, int estateId,
    LocalDate startDate, int duration, double additionalCosts) {
        super(contractNo, date, place);
        this.startDate = startDate;
        this.duration  = duration;
        this.additionalCosts = additionalCosts;
        this.personId = personId;
        this.apartmentId = apartmentId;
}
public TenancyContract(LocalDate date, String place,
int personId, int estateId,
LocalDate startDate, int duration, double additionalCosts) {
this(0, date, place, personId, estateId, startDate, duration, additionalCosts);
}

    public LocalDate getStartDate() { return startDate; }
    public void setStartDate(LocalDate sd) { this.startDate = sd; }
    public int getDuration() { return duration; }
    public void setDuration(int d) { this.duration = d; }
    public double getAdditionalCosts() { return additionalCosts; }
    public void setAdditionalCosts(double c) { this.additionalCosts = c; }
    public int getPersonId()                        { return personId; }
    public void setPersonId(int personId)           { this.personId = personId; }
    public int getEstateId()                     { return apartmentId; }
    public void setEstateId(int apartmentId)     { this.apartmentId = apartmentId; }
    @Override public String toString() {
        return "TenancyContract{no=%s start=%s person=%d estate=%d}".formatted(
            getContractNo(), startDate, getPersonId(), getEstateId());
    }
}
