public class Document {
    private String type;
    private String content;
    private String format;
    private int size;
    private String author;
    private String dateCreated;
    private boolean isEncrypted;
    private String[] tags;
    private byte[] rawData;
    private boolean isCompressed;
    
    public Document(String type, String content, String format, int size, String author, 
                   String dateCreated, boolean isEncrypted, String[] tags, byte[] rawData, 
                   boolean isCompressed) {
        this.type = type;
        this.content = content;
        this.format = format;
        this.size = size;
        this.author = author;
        this.dateCreated = dateCreated;
        this.isEncrypted = isEncrypted;
        this.tags = tags;
        this.rawData = rawData;
        this.isCompressed = isCompressed;
    }

    public void encrypt() {
        if (!isEncrypted) {
            // encryption logic
            isEncrypted = true;
        }
    }

    public void compress() {
        if (!isCompressed) {
            // compression logic
            isCompressed = true;
        }
    }

    public void validate() {
        // validation logic
    }

    public void convert(String newFormat) {
        // conversion logic
        this.format = newFormat;
    }

    public void backup() {
        // backup logic
    }

    public void print() {
        // printing logic
    }

    public void share() {
        // sharing logic
    }
}