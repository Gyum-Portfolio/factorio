interface Shape {
    double calculateArea();
    double calculatePerimeter();
    void draw();
}

class Rectangle implements Shape {
    private double width;
    private double height;
    private String color;
    private boolean isFilled;

    public Rectangle(double width, double height, String color, boolean isFilled) {
        this.width = width;
        this.height = height;
        this.color = color;
        this.isFilled = isFilled;
    }

    public double calculateArea() {
        return width * height;
    }

    public double calculatePerimeter() {
        return 2 * (width + height);
    }

    public void draw() {
        System.out.println("Drawing a Rectangle");
        System.out.println("Color: " + color);
        System.out.println("Filled: " + isFilled);
        System.out.println("Area: " + calculateArea());
        System.out.println("Perimeter: " + calculatePerimeter());
    }
}

// Implement other shape classes (Circle, Triangle, Square) similarly

class ShapeFactory {
    public static Shape createShape(String type, double... params) {
        if (type.equalsIgnoreCase("Rectangle")) {
            return new Rectangle(params[0], params[1], params[2].toString(), (boolean) params[3]);
        } else if (type.equalsIgnoreCase("Circle")) {
            // Create and return Circle instance
        } else if (type.equalsIgnoreCase("Triangle")) {
            // Create and return Triangle instance
        } else if (type.equalsIgnoreCase("Square")) {
            // Create and return Square instance
        }
        return null;
    }
}
