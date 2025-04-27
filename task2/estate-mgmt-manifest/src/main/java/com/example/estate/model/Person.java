package com.example.estate.model;

public class Person {
    private int id;
    private String firstName;
    private String name;
    private String address;

    public Person() {}
    public Person(int id, String firstName, String name, String address) {
        this.id = id; this.firstName = firstName; this.name = name; this.address = address;
    }
    public Person(String firstName, String name, String address) {
        this(0, firstName, name, address);
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getFirstName() { return firstName; }
    public void setFirstName(String first) { this.firstName = first; }
    public String getName() { return name; }
    public void setName(String n) { this.name = n; }
    public String getAddress() { return address; }
    public void setAddress(String a) { this.address = a; }

    @Override public String toString() {
        return "Person{id=%d, name=%s %s}".formatted(id, firstName, name);
    }
}
