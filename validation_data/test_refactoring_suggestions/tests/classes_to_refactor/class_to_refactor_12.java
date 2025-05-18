public class Notification {
    private String type;
    private String message;
    private String priority;
    private String channel;
    private String recipient;
    private boolean isRead;
    private boolean isDelivered;
    private String sender;
    private String timestamp;
    private String htmlContent;
    private String smsText;
    private String emailSubject;
    private String emailBody;
    private String pushTitle;
    private String pushBody;
    
    public Notification(String type, String message) {
        this.type = type;
        this.message = message;
        
        if (type.equals("EMAIL")) {
            this.emailSubject = message;
            this.emailBody = "Default email body";
            this.channel = "EMAIL";
        } else if (type.equals("SMS")) {
            this.smsText = message;
            this.channel = "SMS";
        } else if (type.equals("PUSH")) {
            this.pushTitle = "Push Notification";
            this.pushBody = message;
            this.channel = "PUSH";
        } else if (type.equals("SLACK")) {
            this.htmlContent = "<p>" + message + "</p>";
            this.channel = "SLACK";
        }
    }
}