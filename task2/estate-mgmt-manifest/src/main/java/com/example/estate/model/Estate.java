package com.example.estate.model;

public abstract class Estate {
    private int id;
    private String city;
    private String postalCode;
    private String street;
    private String streetNumber;
    private double squareArea;
    private int agentId;

    public Estate() {}
    public Estate(int id, String city, String postalCode, String street, String streetNumber,
                  double squareArea, int agentId) {
        this.id = id; this.city = city; this.postalCode = postalCode; this.street = street;
        this.streetNumber = streetNumber; this.squareArea = squareArea; this.agentId = agentId;
    }
    public Estate(String city, String postalCode, String street, String streetNumber,
                  double squareArea, int agentId) {
        this(0, city, postalCode, street, streetNumber, squareArea, agentId);
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }
    public String getPostalCode() { return postalCode; }
    public void setPostalCode(String postal) { this.postalCode = postal; }
    public String getStreet() { return street; }
    public void setStreet(String street) { this.street = street; }
    public String getStreetNumber() { return streetNumber; }
    public void setStreetNumber(String nr) { this.streetNumber = nr; }
    public double getSquareArea() { return squareArea; }
    public void setSquareArea(double area) { this.squareArea = area; }
    public int getAgentId() { return agentId; }
    public void setAgentId(int agentId) { this.agentId = agentId; }
}
