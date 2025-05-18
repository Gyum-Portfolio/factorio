public class Computer {
    private String ram;
    private String cpu;
    private String type;
    private String graphicsCard;
    private String storage;
    private String motherboard;
    private String powerSupply;
    private String case_;
    private boolean isLaptop;
    private boolean isDesktop;
    private boolean isServer;
    private boolean isGaming;
    private boolean isWorkstation;
    
    public Computer(String ram, String cpu, String type, String graphicsCard, String storage, 
                   String motherboard, String powerSupply, String case_) {
        this.ram = ram;
        this.cpu = cpu;
        this.type = type;
        this.graphicsCard = graphicsCard;
        this.storage = storage;
        this.motherboard = motherboard;
        this.powerSupply = powerSupply;
        this.case_ = case_;
        
        if(type.equals("laptop")) {
            this.isLaptop = true;
        } else if(type.equals("desktop")) {
            this.isDesktop = true;
        } else if(type.equals("server")) {
            this.isServer = true;
        } else if(type.equals("gaming")) {
            this.isGaming = true;
        } else if(type.equals("workstation")) {
            this.isWorkstation = true;
        }
    }
}