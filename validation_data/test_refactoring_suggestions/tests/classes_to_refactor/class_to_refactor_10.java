public class Messages {
    private String type;
    private String content;
    private String sender;
    private String recipient;
    private String priority;
    private boolean isEncrypted;
    private boolean isRead;
    private String attachmentPath;
    private int messageSize;
    private String encoding;
    
    public Messages(String type, String content, String sender, String recipient, String priority, boolean isEncrypted, String attachmentPath, String encoding) {
        this.type = type;
        this.content = content;
        this.sender = sender;
        this.recipient = recipient;
        this.priority = priority;
        this.isEncrypted = isEncrypted;
        this.isRead = false;
        this.attachmentPath = attachmentPath;
        this.messageSize = content.length();
        this.encoding = encoding;
    }

    public void encrypt() {
        if (!isEncrypted) {
            content = "ENCRYPTED:" + content;
            isEncrypted = true;
        }
    }

    public void decrypt() {
        if (isEncrypted) {
            content = content.replace("ENCRYPTED:", "");
            isEncrypted = false;
        }
    }

    public void send() {
        if (isEncrypted) {
            System.out.println("Sending encrypted message to " + recipient);
        } else {
            System.out.println("Sending plain message to " + recipient);
        }
    }

    public void markAsRead() {
        isRead = true;
    }

    public void saveAttachment() {
        if (attachmentPath != null) {
            System.out.println("Saving attachment to " + attachmentPath);
        }
    }
}