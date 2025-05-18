public class Payment {
    private String method;
    private double amount;
    private String cardNumber;
    private String bankAccount;
    private String paypalEmail;
    private String cryptoWallet;
    private boolean isProcessed;
    private String currency;
    private double conversionRate;
    private String transactionId;
    private boolean isRefunded;
    private String refundReason;
    
    public Payment(String method, double amount) {
        this.method = method;
        this.amount = amount;
        this.isProcessed = false;
        this.isRefunded = false;
    }

    public void processCardPayment(String cardNumber) {
        this.cardNumber = cardNumber;
        this.isProcessed = true;
        this.transactionId = "CARD-" + System.currentTimeMillis();
    }

    public void processBankPayment(String bankAccount) {
        this.bankAccount = bankAccount;
        this.isProcessed = true;
        this.transactionId = "BANK-" + System.currentTimeMillis();
    }

    public void processPaypalPayment(String paypalEmail) {
        this.paypalEmail = paypalEmail;
        this.isProcessed = true;
        this.transactionId = "PP-" + System.currentTimeMillis();
    }

    public void processCryptoPayment(String cryptoWallet) {
        this.cryptoWallet = cryptoWallet;
        this.isProcessed = true;
        this.transactionId = "CRYPTO-" + System.currentTimeMillis();
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