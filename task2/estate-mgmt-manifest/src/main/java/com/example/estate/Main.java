package com.example.estate;

import com.example.estate.dao.*;
import com.example.estate.model.*;

import java.sql.SQLException;
import java.time.LocalDate;
import java.util.Scanner;

/**
 * Minimal CLI fulfilling required functionality.
 */
public class Main {

    private static final String ADMIN_PW = "admin123";

    private final EstateAgentDAO agentDAO = new EstateAgentDAO();
    private final ApartmentDAO apartmentDAO = new ApartmentDAO();
    private final HouseDAO houseDAO = new HouseDAO();
    private final PersonDAO personDAO = new PersonDAO();
    private final ContractDAO contractDAO = new ContractDAO();
    private final Scanner sc = new Scanner(System.in);

    public static void main(String[] args) throws SQLException {
        new Main().run();
    }

    private void run() throws SQLException {
        while (true) {
            System.out.println("\n=== Main ===\n1) Agent management (admin)\n2) Login as estate agent\n0) Exit");
            switch (sc.nextLine()) {
                case "1" -> adminMenu();
                case "2" -> agentLogin();
                case "0" -> { return; }
                default -> System.out.println("Unknown option!");
            }
        }
    }

    /* Admin mode */
    private void adminMenu() throws SQLException {
        System.out.print("Enter admin password: ");
        if (!sc.nextLine().equals(ADMIN_PW)) { System.out.println("Wrong!"); return; }
        while (true) {
            System.out.println("\n--- Agent Management ---\n1) List\n2) Create\n3) Update\n4) Delete\n0) Back");
            switch (sc.nextLine()) {
                case "1" -> agentDAO.findAll().forEach(System.out::println);
                case "2" -> {
                    System.out.print("Name: "); String n = sc.nextLine();
                    System.out.print("Address: "); String addr = sc.nextLine();
                    System.out.print("Login: "); String login = sc.nextLine();
                    System.out.print("Password: "); String pw = sc.nextLine();
                    try {
                        agentDAO.create(new EstateAgent(n, addr, login, pw));
                        System.out.println("Agent created.");
                    } catch (IllegalArgumentException dup) {
                        System.out.println(dup.getMessage());
                    }
                    
                    
                }
                case "3" -> {
                    System.out.print("Agent id: "); int id = Integer.parseInt(sc.nextLine());
                    EstateAgent a = agentDAO.findAll().stream().filter(e -> e.getId()==id).findFirst().orElse(null);
                    if (a == null) { System.out.println("Not found."); continue; }
                    System.out.print("New name ["+a.getName()+"]: "); String n = sc.nextLine();
                    if (!n.isBlank()) a.setName(n);
                    System.out.print("New address ["+a.getAddress()+"]: "); String ad = sc.nextLine();
                    if (!ad.isBlank()) a.setAddress(ad);
                    System.out.print("New password (blank keep): "); String pw = sc.nextLine();
                    if (!pw.isBlank()) a.setPassword(pw);
                    agentDAO.update(a);
                    System.out.println("Agent updated.");
                }
                case "4" -> {
                    System.out.print("Agent id: "); int id = Integer.parseInt(sc.nextLine());
                    agentDAO.delete(id);
                    System.out.print("Agent deleted.");
                }
                case "0" -> { return; }
                default -> System.out.println("Unknown"); }
        }
    }

    /* Agent login */
    private void agentLogin() throws SQLException {
        System.out.print("Login: "); String login = sc.nextLine();
        System.out.print("Password: "); String pw = sc.nextLine();
        EstateAgent agent = agentDAO.findByLogin(login);
        if (agent == null || !agent.getPassword().equals(pw)) { System.out.println("Wrong credentials!"); return; }
        while (true) {
            System.out.println("\n--- Agent Menu ---\n1) Manage estates\n2) Contracts\n0) Logout");
            switch (sc.nextLine()) {
                case "1" -> estatesMenu(agent);
                case "2" -> contractsMenu();
                case "0" -> { return; }
                default -> System.out.println("Unknown");
            }
        }
    }

    /* Estates */
    private void estatesMenu(EstateAgent agent) throws SQLException {
        while (true) {
            System.out.println("\n-- Estates --\n1) List\n2) Create apartment\n3) Create house\n4) Delete\n0) Back");
            String opt = sc.nextLine();
            switch (opt) {
                case "1" -> {
                    apartmentDAO.findByAgent(agent.getId()).forEach(System.out::println);
                    houseDAO.findByAgent(agent.getId()).forEach(System.out::println);
                }
                case "2" -> createApartment(agent);
                case "3" -> createHouse(agent);
                case "4" -> {
                    System.out.print("Estate id: "); int id = Integer.parseInt(sc.nextLine());
                    apartmentDAO.delete(id);
                    System.out.println("Estate deleted.");
                }
                case "0" -> { return; }
                default -> System.out.println("Unknown");
            }
        }
    }

    private void createApartment(EstateAgent agent) throws SQLException {
        System.out.print("City: "); String city = sc.nextLine();
        System.out.print("Postal: "); String pc = sc.nextLine();
        System.out.print("Street: "); String street = sc.nextLine();
        System.out.print("Number: "); String nr = sc.nextLine();
        System.out.print("Area: "); double area = Double.parseDouble(sc.nextLine());
        System.out.print("Floor: "); int floor = Integer.parseInt(sc.nextLine());
        System.out.print("Rent: "); double rent = Double.parseDouble(sc.nextLine());
        System.out.print("Rooms: "); int rooms = Integer.parseInt(sc.nextLine());
        System.out.print("Balcony y/n: "); boolean bal = sc.nextLine().equalsIgnoreCase("y");
        System.out.print("Built-in kitchen y/n: "); boolean bik = sc.nextLine().equalsIgnoreCase("y");
        apartmentDAO.create(new Apartment(city, pc, street, nr, area, agent.getId(),
                floor, rent, rooms, bal, bik));
    }

    private void createHouse(EstateAgent agent) throws SQLException {
        System.out.print("City: "); String city = sc.nextLine();
        System.out.print("Postal: "); String pc = sc.nextLine();
        System.out.print("Street: "); String street = sc.nextLine();
        System.out.print("Number: "); String nr = sc.nextLine();
        System.out.print("Area: "); double area = Double.parseDouble(sc.nextLine());
        System.out.print("Floors: "); int floors = Integer.parseInt(sc.nextLine());
        System.out.print("Price: "); double price = Double.parseDouble(sc.nextLine());
        System.out.print("Garden y/n: "); boolean garden = sc.nextLine().equalsIgnoreCase("y");
        houseDAO.create(new House(city, pc, street, nr, area, agent.getId(), floors, price, garden));
    }

    /* Contracts */
    private void contractsMenu() throws SQLException {
        while (true) {
            System.out.println("\n-- Contracts --\n1) Insert person\n2) Tenancy contract\n3) Purchase contract\n4) Overview\n0) Back");
            switch (sc.nextLine()) {
                case "1" -> {
                    System.out.print("First name: "); String fn = sc.nextLine();
                    System.out.print("Last name: "); String ln = sc.nextLine();
                    System.out.print("Address: "); String addr = sc.nextLine();
                    personDAO.create(new Person(fn, ln, addr));
                }
                case "2" -> signTenancy();
                case "3" -> signPurchase();
                case "4" -> contractDAO.overview().forEach(System.out::println);
                case "0" -> { return; }
                default -> System.out.println("Unknown");
            }
        }
    }

    private void signTenancy() throws SQLException {
        System.out.print("Contract no: "); int no = Integer.parseInt(sc.nextLine());
        System.out.print("Person id: "); int pid = Integer.parseInt(sc.nextLine());
        System.out.print("Apartment estate id: "); int eid = Integer.parseInt(sc.nextLine());
        System.out.print("Start date (YYYY-MM-DD): "); LocalDate start = LocalDate.parse(sc.nextLine());
        System.out.print("Duration months: "); int dur = Integer.parseInt(sc.nextLine());
        System.out.print("Add. costs: "); double costs = Double.parseDouble(sc.nextLine());
        TenancyContract tc = new TenancyContract(no, LocalDate.now(), "Online", pid, eid, start, dur, costs);
        contractDAO.createTenancy(tc);
    }

    private void signPurchase() throws SQLException {
        System.out.print("Contract no: "); int no = Integer.parseInt(sc.nextLine());
        System.out.print("Person id: "); int pid = Integer.parseInt(sc.nextLine());
        System.out.print("House estate id: "); int eid = Integer.parseInt(sc.nextLine());
        System.out.print("Installments: "); int inst = Integer.parseInt(sc.nextLine());
        System.out.print("Interest rate %: "); double rate = Double.parseDouble(sc.nextLine());
        PurchaseContract pc = new PurchaseContract(no, LocalDate.now(), "Online", pid, eid, inst, rate);
        contractDAO.createPurchase(pc);
    }
}
