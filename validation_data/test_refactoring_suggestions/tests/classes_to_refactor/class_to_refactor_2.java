public class Vehicle {
    private String type;
    private int wheels;
    private String color;
    private double price;
    private int seats;
    private String engine;
    private String fuel;
    private String manufacturer;
    private boolean isRunning;
    private int speed;
    
    public Vehicle(String type, int wheels, String color, double price, int seats, String engine, String fuel, String manufacturer) {
        this.type = type;
        this.wheels = wheels;
        this.color = color;
        this.price = price;
        this.seats = seats;
        this.engine = engine;
        this.fuel = fuel;
        this.manufacturer = manufacturer;
        this.isRunning = false;
        this.speed = 0;
    }
    
    public void startEngine() {
        isRunning = true;
        System.out.println("Engine started");
    }
    
    public void stopEngine() {
        isRunning = false;
        speed = 0;
        System.out.println("Engine stopped");
    }
    
    public void accelerate() {
        if(isRunning) {
            speed += 10;
            calculateFuelConsumption();
            System.out.println("Speed: " + speed);
        }
    }
    
    public void brake() {
        if(speed > 0) {
            speed -= 10;
            System.out.println("Speed: " + speed);
        }
    }
    
    private void calculateFuelConsumption() {
        if(fuel.equals("Petrol")) {
            System.out.println("Consuming petrol");
        } else if(fuel.equals("Diesel")) {
            System.out.println("Consuming diesel");
        } else if(fuel.equals("Electric")) {
            System.out.println("Using electricity");
        }
    }
}