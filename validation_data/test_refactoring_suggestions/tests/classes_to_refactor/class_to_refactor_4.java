public class Shape {
    private String type;
    private double area;
    private double perimeter;
    private int sides;
    private String color;
    private boolean isFilled;
    private double width;
    private double height;
    private double radius;
    private double diagonal;
    
    public Shape(String type, double area, double perimeter, int sides, String color, boolean isFilled, double width, double height, double radius, double diagonal) {
        this.type = type;
        this.area = area;
        this.perimeter = perimeter;
        this.sides = sides;
        this.color = color;
        this.isFilled = isFilled;
        this.width = width;
        this.height = height;
        this.radius = radius;
        this.diagonal = diagonal;
    }

    public double calculateArea() {
        if(type.equals("Rectangle")) {
            return width * height;
        } else if(type.equals("Circle")) {
            return Math.PI * radius * radius;
        } else if(type.equals("Triangle")) {
            return (width * height) / 2;
        } else if(type.equals("Square")) {
            return width * width;
        }
        return 0;
    }

    public double calculatePerimeter() {
        if(type.equals("Rectangle")) {
            return 2 * (width + height);
        } else if(type.equals("Circle")) {
            return 2 * Math.PI * radius;
        } else if(type.equals("Triangle")) {
            return 3 * width;
        } else if(type.equals("Square")) {
            return 4 * width;
        }
        return 0;
    }

    public void draw() {
        System.out.println("Drawing a " + type);
        System.out.println("Color: " + color);
        System.out.println("Filled: " + isFilled);
        System.out.println("Area: " + calculateArea());
        System.out.println("Perimeter: " + calculatePerimeter());
    }
}