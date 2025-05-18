// Vehicle interface
interface Vehicle {
    void startEngine();
    void stopEngine();
    void accelerate();
    void brake();
}

// Concrete vehicle classes
class Car implements Vehicle {
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

    // Constructor and other methods...

    public void startEngine() {
        // Implementation
    }

    public void stopEngine() {
        // Implementation
    }

    public void accelerate() {
        // Implementation
    }

    public void brake() {
        // Implementation
    }
}

class Truck implements Vehicle {
    // Implementation...
}

class Motorcycle implements Vehicle {
    // Implementation...
}

// VehicleFactory
class VehicleFactory {
    public static Vehicle createVehicle(String type, int wheels, String color, double price, int seats, String engine, String fuel, String manufacturer) {
        if (type.equalsIgnoreCase("car")) {
            return new Car(type, wheels, color, price, seats, engine, fuel, manufacturer);
        } else if (type.equalsIgnoreCase("truck")) {
            return new Truck(type, wheels, color, price, seats, engine, fuel, manufacturer);
        } else if (type.equalsIgnoreCase("motorcycle")) {
            return new Motorcycle(type, wheels, color, price, seats, engine, fuel, manufacturer);
        } else {
            throw new IllegalArgumentException("Invalid vehicle type");
        }
    }
}
