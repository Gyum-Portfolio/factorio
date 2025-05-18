interface Animal {
    void makeSound();
    void eat();
    void move();
    void sleep();
    void grow();
    void changeColor(String newColor);
}

class Dog implements Animal {
    private String sound;
    private String diet;
    private int numberOfLegs;
    private boolean canSwim;
    private double weight;
    private String color;
    private int age;

    public Dog(String sound, String diet, int numberOfLegs, boolean canSwim, double weight, String color, int age) {
        this.sound = sound;
        this.diet = diet;
        this.numberOfLegs = numberOfLegs;
        this.canSwim = canSwim;
        this.weight = weight;
        this.color = color;
        this.age = age;
    }

    // Implement methods from the Animal interface
    public void makeSound() {
        System.out.println(sound);
    }

    public void eat() {
        System.out.println("Eating " + diet);
    }

    public void move() {
        System.out.println("Walking with " + numberOfLegs + " legs");
    }

    public void sleep() {
        System.out.println("Sleeping on the floor");
    }

    public void grow() {
        age++;
        weight += 0.1;
    }

    public void changeColor(String newColor) {
        this.color = newColor;
    }
}

class AnimalFactory {
    public static Animal createAnimal(String type, String sound, String diet, int numberOfLegs,
                                      boolean canSwim, double weight, String color, int age) {
        if (type.equalsIgnoreCase("dog")) {
            return new Dog(sound, diet, numberOfLegs, canSwim, weight, color, age);
        }
        // Add more cases for other animal types

        return null;
    }
}
