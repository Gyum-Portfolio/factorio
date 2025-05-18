public class Animal {
    private String species;
    private String sound;
    private String habitat;
    private String diet;
    private int numberOfLegs;
    private boolean canFly;
    private boolean canSwim;
    private double weight;
    private String color;
    private int age;

    public Animal(String species, String sound, String habitat, String diet, int numberOfLegs,
                 boolean canFly, boolean canSwim, double weight, String color, int age) {
        this.species = species;
        this.sound = sound;
        this.habitat = habitat;
        this.diet = diet;
        this.numberOfLegs = numberOfLegs;
        this.canFly = canFly;
        this.canSwim = canSwim;
        this.weight = weight;
        this.color = color;
        this.age = age;
    }

    public void makeSound() {
        System.out.println(sound);
    }

    public void eat() {
        System.out.println("Eating " + diet);
    }

    public void move() {
        if (canFly) {
            System.out.println("Flying");
        } else if (canSwim) {
            System.out.println("Swimming");
        } else {
            System.out.println("Walking with " + numberOfLegs + " legs");
        }
    }

    public void sleep() {
        System.out.println("Sleeping in " + habitat);
    }

    public void grow() {
        age++;
        weight += 0.1;
    }

    public void changeColor(String newColor) {
        this.color = newColor;
    }
}