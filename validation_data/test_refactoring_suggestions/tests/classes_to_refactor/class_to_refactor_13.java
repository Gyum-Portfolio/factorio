public class Product {
    private String category;
    private double price;
    private String name;
    private String description;
    private int quantity;
    private String manufacturer;
    private String type;
    private boolean isDiscounted;
    private double discountPercentage;
    private String shippingMethod;
    private double weight;
    private boolean isInStock;
    private String warehouse;
    
    public Product(String category, double price, String type) {
        this.category = category;
        this.price = price;
        this.type = type;
    }
    
    public void processOrder() {
        calculateDiscount();
        updateInventory();
        handleShipping();
        generateInvoice();
    }
    
    private void calculateDiscount() {
        if(isDiscounted) {
            price = price * (1 - discountPercentage);
        }
    }
    
    private void updateInventory() {
        if(quantity > 0) {
            quantity--;
            isInStock = quantity > 0;
        }
    }
    
    private void handleShipping() {
        if(shippingMethod.equals("express")) {
            price += weight * 2;
        } else {
            price += weight;
        }
    }
    
    private void generateInvoice() {
        // Complex invoice generation logic
    }
}