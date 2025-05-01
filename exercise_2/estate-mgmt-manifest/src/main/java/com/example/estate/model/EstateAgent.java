package com.example.estate.model;

public class EstateAgent {
    private int agent_id;
    private String name;
    private String address;
    private String  username;
    private String password;

    public EstateAgent() {}

    public EstateAgent(int agent_id, String name, String address, String username, String password) {
        this.agent_id = agent_id; this.name = name; this.address = address; this.username = username; this.password = password;
    }
    public EstateAgent(String name, String address, String username, String password) {
        this(0, name, address, username, password);
    }

    public int getId() { return agent_id; }
    public void setId(int agent_id) { this.agent_id = agent_id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }
    public String getLogin() { return username; }
    public void setLogin(String username) { this.username = username; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    @Override public String toString() {
        return "Agent{agent_id=%d, name='%s', username='%s'}".formatted(agent_id, name, username);
    }
}
