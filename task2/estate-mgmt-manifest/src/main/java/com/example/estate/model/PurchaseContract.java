package com.example.estate.model;

import java.time.LocalDate;

public class PurchaseContract extends Contract {
    private int installments;
    private double interestRate;
    private int personId;  
    private int estateId;  

    public PurchaseContract() {}
    public PurchaseContract(int contractNo, LocalDate date, String place,
                            int personId, int estateId, int installments, double interestRate) {
        super( contractNo, date, place);
        this.installments = installments; this.interestRate = interestRate;
        this.personId = personId; this.estateId = estateId;
    }
    public PurchaseContract(LocalDate date, String place,
                            int personId, int estateId, int installments, double interestRate) {
        this(0, date, place, personId, estateId, installments, interestRate);
    }

    public int getInstallments() { return installments; }
    public void setInstallments(int i) { this.installments = i; }
    public double getInterestRate() { return interestRate; }
    public void setInterestRate(double ir) { this.interestRate = ir; }
    public int getPersonId() { return personId; }
    public void setPersonId(int personId) {this.personId = personId; }
    public int getEstateId() { return estateId; }
    public void setEstateID(int estateId) {this.estateId = estateId; }



    @Override public String toString() {
        return "PurchaseContract{no=%s installments=%d rate=%.2f%%}".formatted(
            getContractNo(), installments, interestRate);
    }
}
