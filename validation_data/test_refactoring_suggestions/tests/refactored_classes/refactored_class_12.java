interface Notification {
    void setMessage(String message);
    void setRecipient(String recipient);
    // Add other common methods
}

class EmailNotification implements Notification {
    private String emailSubject;
    private String emailBody;
    private String recipient;

    public void setMessage(String message) {
        this.emailSubject = message;
        this.emailBody = "Default email body";
    }

    public void setRecipient(String recipient) {
        this.recipient = recipient;
    }

    // Add other methods specific to EmailNotification
}

class SmsNotification implements Notification {
    private String smsText;
    private String recipient;

    public void setMessage(String message) {
        this.smsText = message;
    }

    public void setRecipient(String recipient) {
        this.recipient = recipient;
    }

    // Add other methods specific to SmsNotification
}

class PushNotification implements Notification {
    private String pushTitle;
    private String pushBody;
    private String recipient;

    public void setMessage(String message) {
        this.pushTitle = "Push Notification";
        this.pushBody = message;
    }

    public void setRecipient(String recipient) {
        this.recipient = recipient;
    }

    // Add other methods specific to PushNotification
}

class SlackNotification implements Notification {
    private String htmlContent;
    private String recipient;

    public void setMessage(String message) {
        this.htmlContent = "<p>" + message + "</p>";
    }

    public void setRecipient(String recipient) {
        this.recipient = recipient;
    }

    // Add other methods specific to SlackNotification
}

class NotificationFactory {
    public static Notification createNotification(String type, String message) {
        Notification notification = null;

        if (type.equals("EMAIL")) {
            notification = new EmailNotification();
        } else if (type.equals("SMS")) {
            notification = new SmsNotification();
        } else if (type.equals("PUSH")) {
            notification = new PushNotification();
        } else if (type.equals("SLACK")) {
            notification = new SlackNotification();
        }

        if (notification != null) {
            notification.setMessage(message);
        }

        return notification;
    }
}
