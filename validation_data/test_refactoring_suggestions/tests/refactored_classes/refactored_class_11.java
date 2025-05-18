interface Report {
    void generateReport();
    void send();
}

class PDFReport implements Report {
    private String data;
    private String title;
    private String author;
    private String[] recipients;
    // Additional fields specific to PDF reports

    public PDFReport(String data, String title, String author, String[] recipients) {
        this.data = data;
        this.title = title;
        this.author = author;
        this.recipients = recipients;
    }

    public void generateReport() {
        // PDF report generation logic
    }

    public void send() {
        // Sending logic for PDF reports
    }
}

class ExcelReport implements Report {
    private String data;
    private String title;
    private String author;
    private String[] recipients;
    // Additional fields specific to Excel reports

    public ExcelReport(String data, String title, String author, String[] recipients) {
        this.data = data;
        this.title = title;
        this.author = author;
        this.recipients = recipients;
    }

    public void generateReport() {
        // Excel report generation logic
    }

    public void send() {
        // Sending logic for Excel reports
    }
}

class ReportFactory {
    public static Report createReport(String format, String data, String title, String author, String[] recipients) {
        if (format.equalsIgnoreCase("PDF")) {
            return new PDFReport(data, title, author, recipients);
        } else if (format.equalsIgnoreCase("EXCEL")) {
            return new ExcelReport(data, title, author, recipients);
        }
        // Add more report types as needed
        return null;
    }
}
