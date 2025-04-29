package com.example.estate.model;

import java.time.LocalDate;

public class PurchaseContract extends Contract {
    private int installments;
    private double interestRate;

    public PurchaseContract() {}
    public PurchaseContract(int id, int contractNo, LocalDate date, String place,
                            int personId, int estateId, int installments, double interestRate) {
        super(id, contractNo, date, place, personId, estateId);
        this.installments = installments; this.interestRate = interestRate;
    }
    public PurchaseContract(int contractNo, LocalDate date, String place,
                            int personId, int estateId, int installments, double interestRate) {
        this(0, contractNo, date, place, personId, estateId, installments, interestRate);
    }

    public int getInstallments() { return installments; }
    public void setInstallments(int i) { this.installments = i; }
    public double getInterestRate() { return interestRate; }
    public void setInterestRate(double ir) { this.interestRate = ir; }

    @Override public String toString() {
        return "PurchaseContract{no=%s installments=%d rate=%.2f%%}".formatted(
            getContractNo(), installments, interestRate);
    }
}
