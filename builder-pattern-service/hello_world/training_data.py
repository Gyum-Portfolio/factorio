examples = [
    {
        "original_code": """
public class Converter {{
    private String sourceFormat;
    private String targetFormat;
    public Converter(String sourceFormat, String targetFormat) {{
        this.sourceFormat = sourceFormat;
        this.targetFormat = targetFormat;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Converter {{
    String convert(String input);
    String getTargetFormat();
}}

class ImageConverter implements Converter {{
    private String sourceFormat;
    private String targetFormat;
    public ImageConverter(String targetFormat) {{
        this.sourceFormat = "PNG";
        this.targetFormat = targetFormat;
    }}
    public String convert(String input) {{ return input + "." + targetFormat; }}
    public String getTargetFormat() {{ return targetFormat; }}
}}

class ConverterFactory {{
    public static Converter createConverter(String sourceFormat, String targetFormat) {{
        if (sourceFormat.equals("PNG")) return new ImageConverter(targetFormat);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Encoder {{
    private String algorithm;
    private String data;
    public Encoder(String algorithm, String data) {{
        this.algorithm = algorithm;
        this.data = data;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Encoder {{
    String encode(String input);
    String getAlgorithm();
}}

class Base64Encoder implements Encoder {{
    private String algorithm;
    private String data;
    public Base64Encoder(String data) {{
        this.algorithm = "Base64";
        this.data = data;
    }}
    public String encode(String input) {{ return input; }}
    public String getAlgorithm() {{ return algorithm; }}
}}

class EncoderFactory {{
    public static Encoder createEncoder(String algorithm, String data) {{
        if (algorithm.equals("Base64")) return new Base64Encoder(data);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Builder {{
    private String type;
    private String config;
    public Builder(String type, String config) {{
        this.type = type;
        this.config = config;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Builder {{
    Object build();
    String getConfig();
}}

class XMLBuilder implements Builder {{
    private String type;
    private String config;
    public XMLBuilder(String config) {{
        this.type = "XML";
        this.config = config;
    }}
    public Object build() {{ return null; }}
    public String getConfig() {{ return config; }}
}}

class BuilderFactory {{
    public static Builder createBuilder(String type, String config) {{
        if (type.equals("XML")) return new XMLBuilder(config);
        return null;
    }}
}}"""
    },
    {
        "original_code": """
public class Formatter {{
    private String style;
    private String text;
    public Formatter(String style, String text) {{
        this.style = style;
        this.text = text;
    }}
}}""",
        "pattern": "Factory",
        "implemented_code": """
interface Formatter {{
    String format(String input);
    String getStyle();
}}

class HTMLFormatter implements Formatter {{
    private String style;
    private String text;
    public HTMLFormatter(String text) {{
        this.style = "HTML";
        this.text = text;
    }}
    public String format(String input) {{ return "<p>" + input + "</p>"; }}
    public String getStyle() {{ return style; }}
}}

class FormatterFactory {{
    public static Formatter createFormatter(String style, String text) {{
        if (style.equals("HTML")) return new HTMLFormatter(text);
        return null;
    }}
}}"""
    },
 {
        "original_code": """
public class Pizza {{
    private String dough;
    private String sauce;
    private String topping;

    public Pizza(String dough, String sauce, String topping) {{
        this.dough = dough;
        this.sauce = sauce;
        this.topping = topping;
    }}
}}""",
        "pattern": "Builder",
        "implemented_code": """
public class Pizza {{
    private String dough;
    private String sauce;
    private String topping;

    private Pizza() {{}}  // Private constructor

    public static class PizzaBuilder {{
        private Pizza pizza = new Pizza();

        public PizzaBuilder dough(String dough) {{
            pizza.dough = dough;
            return this;
        }}

        public PizzaBuilder sauce(String sauce) {{
            pizza.sauce = sauce;
            return this;
        }}

        public PizzaBuilder topping(String topping) {{
            pizza.topping = topping;
            return this;
        }}

        public Pizza build() {{
            return pizza;
        }}
    }}
}}"""
    }
]