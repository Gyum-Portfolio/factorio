interface Payment {
    void processPayment();
    void refundPayment(String reason);
    void convertCurrency(String newCurrency, double conversionRate);
}

class CardPayment implements Payment {
    private double amount;
    private String cardNumber;
    private String transactionId;
    private boolean isRefunded;
    private String refundReason;
    private String currency;
    private double conversionRate;

    public CardPayment(double amount, String cardNumber) {
        this.amount = amount;
        this.cardNumber = cardNumber;
        this.transactionId = "CARD-" + System.currentTimeMillis();
    }

    public void processPayment() {
        // Process card payment
    }

    public void refundPayment(String reason) {
        this.isRefunded = true;
        this.refundReason = reason;
    }

    public void convertCurrency(String newCurrency, double conversionRate) {
        this.currency = newCurrency;
        this.conversionRate = conversionRate;
        this.amount = amount * conversionRate;
    }
}

// Other payment types: BankPayment, PaypalPayment, CryptoPayment

class PaymentFactory {
    public static Payment createPayment(String method, double amount, String paymentInfo) {
        switch (method) {
            case "card":
                return new CardPayment(amount, paymentInfo);
            case "bank":
                return new BankPayment(amount, paymentInfo);
            case "paypal":
                return new PaypalPayment(amount, paymentInfo);
            case "crypto":
                return new CryptoPayment(amount, paymentInfo);
            default:
                throw new IllegalArgumentException("Invalid payment method: " + method);
        }
    }
}
