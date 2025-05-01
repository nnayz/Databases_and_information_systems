package com.example.estate.model;

public class House extends Estate {
    private int floors;
    private double price;
    private boolean garden;

    public House() {}
    public House(int id, String city, String postalCode, String street, String streetNumber,
                 double squareArea, int agentId,
                 int floors, double price, boolean garden) {
        super(id, city, postalCode, street, streetNumber, squareArea, agentId);
        this.floors = floors; this.price = price; this.garden = garden;
    }
    public House(String city, String postalCode, String street, String streetNumber,
                 double squareArea, int agentId,
                 int floors, double price, boolean garden) {
        this(0, city, postalCode, street, streetNumber, squareArea, agentId, floors, price, garden);
    }

    public int getFloors() { return floors; }
    public void setFloors(int floors) { this.floors = floors; }
    public double getPrice() { return price; }
    public void setPrice(double price) { this.price = price; }
    public boolean isGarden() { return garden; }
    public void setGarden(boolean garden) { this.garden = garden; }

    @Override public String toString() {
        return "House{id=%d, city=%s, price=%.2f}".formatted(getId(), getCity(), price);
    }
}
