package com.example.estate.model;

public class Apartment extends Estate {
    private int floor;
    private double rent;
    private int rooms;
    private boolean balcony;
    private boolean builtInKitchen;

    public Apartment() {}
    public Apartment(int id, String city, String postalCode, String street, String streetNumber,
                     double squareArea, int agentId,
                     int floor, double rent, int rooms, boolean balcony, boolean builtInKitchen) {
        super(id, city, postalCode, street, streetNumber, squareArea, agentId);
        this.floor = floor; this.rent = rent; this.rooms = rooms;
        this.balcony = balcony; this.builtInKitchen = builtInKitchen;
    }
    public Apartment(String city, String postalCode, String street, String streetNumber,
                     double squareArea, int agentId,
                     int floor, double rent, int rooms, boolean balcony, boolean builtInKitchen) {
        this(0, city, postalCode, street, streetNumber, squareArea, agentId,
            floor, rent, rooms, balcony, builtInKitchen);
    }

    public int getFloor() { return floor; }
    public void setFloor(int floor) { this.floor = floor; }
    public double getRent() { return rent; }
    public void setRent(double rent) { this.rent = rent; }
    public int getRooms() { return rooms; }
    public void setRooms(int rooms) { this.rooms = rooms; }
    public boolean isBalcony() { return balcony; }
    public void setBalcony(boolean balcony) { this.balcony = balcony; }
    public boolean isBuiltInKitchen() { return builtInKitchen; }
    public void setBuiltInKitchen(boolean builtInKitchen) { this.builtInKitchen = builtInKitchen; }

    @Override public String toString() {
        return "Apartment{id=%d, city=%s, rent=%.2f}".formatted(getId(), getCity(), rent);
    }
}
