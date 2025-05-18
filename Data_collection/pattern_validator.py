import re

class PatternValidator:
    """
    A validator specifically designed to detect Factory patterns in Java code.
    Focuses on both Factory Method and Abstract Factory patterns with careful
    consideration of Java-specific implementations.
    """
    def __init__(self):
        # Core pattern detection components
        self.compiled_patterns = None
        self.compiled_indicators = None
        self.compiled_context = None
        self.pattern_patterns = None
        self.implementation_indicators = None
        self.context_patterns = None

        # Define Java-specific factory pattern matching rules
        self.patterns = {
            "factory": {
                "raw_patterns": [
                    # Factory Method Patterns
                    r"(public|protected|private)\s+\w+\s+(create\w*|make\w*|get\w*Instance)\s*\([^)]*\)",
                    r"(public|protected|private)\s+static\s+\w+\s+\w+\s*\([^)]*\)\s*\{[^}]*\breturn\s+new\b",
                    
                    # Factory Class Patterns
                    r"(public|protected|private)?\s*(abstract\s+)?class\s+\w*Factory\b",
                    r"(public|protected|private)?\s*interface\s+\w*Factory\b",
                    r"implements\s+\w*Factory\b",
                    r"extends\s+\w*Factory\b",
                    
                    # Abstract Factory Patterns
                    r"abstract\s+\w+\s+create\w+\([^)]*\)",
                    r"abstract\s+class\s+Abstract\w*Factory\b",
                    
                    # Factory Instance Creation
                    r"getInstance\(\s*\)",
                    r"newInstance\(\s*\)",
                    r"createInstance\(\s*\)",
                ],
                "raw_indicators": {
                    'creation_methods': [
                        r"new\s+\w+\s*\([^)]*\)",
                        r"return\s+new\s+\w+",
                    ],
                    'factory_methods': [
                        r"create\w+\([^)]*\)",
                        r"make\w+\([^)]*\)",
                        r"get\w+Instance\([^)]*\)",
                    ]
                },
                "context_indicators": [
                    r"package.*\.factory",
                    r"package.*\.factories",
                    r"import.*\.factory\.",
                    r"/\*\*.*[Ff]actory.*\*/",
                    r"@see.*Factory",
                    r"implements.*Creator",
                    r"extends.*Creator"
                ]
            }
        }

    def set_pattern(self, pattern_type):
        """
        Configure the validator for factory pattern detection.
        
        Args:
            pattern_type (str): Should be 'factory' for this implementation
            
        Raises:
            ValueError: If pattern_type isn't 'factory'
        """
        if pattern_type not in self.patterns:
            raise ValueError(f"Pattern type '{pattern_type}' is not defined.")
        
        self.pattern_patterns = self.patterns[pattern_type]["raw_patterns"]
        self.implementation_indicators = self.patterns[pattern_type]["raw_indicators"]
        self.context_patterns = self.patterns[pattern_type]["context_indicators"]
        self.compile_patterns()

    def compile_patterns(self):
        """
        Compile all regex patterns for improved performance.
        """
        self.compiled_patterns = [re.compile(pattern, re.MULTILINE) for pattern in self.pattern_patterns]
        self.compiled_indicators = {
            key: [re.compile(pattern, re.MULTILINE) for pattern in patterns]
            for key, patterns in self.implementation_indicators.items()
        }
        self.compiled_context = [re.compile(pattern, re.MULTILINE) for pattern in self.context_patterns]

    def has_pattern_implemented(self, code):
        """
        Check for implementation indicators of the factory pattern.
        
        Args:
            code (str): Source code to analyze
            
        Returns:
            bool: True if factory implementation indicators are found
        """
        return any(
            any(pattern.search(code) for pattern in patterns)
            for patterns in self.compiled_indicators.values()
        )

    def has_relevant_context(self, code):
        """
        Check for contextual indicators suggesting factory pattern usage.
        
        Args:
            code (str): Source code to analyze
            
        Returns:
            bool: True if factory context indicators are found
        """
        return any(pattern.search(code) for pattern in self.compiled_context)

    def calculate_confidence_score(self, code):
        """
        Calculate confidence score for factory pattern implementation.
        
        Args:
            code (str): Source code to analyze
            
        Returns:
            float: Confidence score between 0 and 1
        """
        score = 0
        pattern_matches = 0
        
        # Check for explicit factory patterns
        for pattern in self.compiled_patterns:
            if pattern.search(code):
                pattern_matches += 1
                if any(key in pattern.pattern for key in ['Factory', 'factory']):
                    score += 3  # Higher weight for explicit factory patterns
                else:
                    score += 2
        
        # Bonus for multiple pattern matches
        if pattern_matches > 1:
            score += 2
        
        # Check implementation indicators
        for patterns in self.compiled_indicators.values():
            if any(pattern.search(code) for pattern in patterns):
                score += 1
        
        # Consider context
        if self.has_relevant_context(code):
            score += 2
        
        return min(score / 12.0, 1.0)  # Normalized score

    def is_pattern_absent(self, code, threshold=0.25):
        """
        Check if factory pattern is absent from the code.
        
        Args:
            code (str): Source code to analyze
            threshold (float): Confidence threshold for absence determination
            
        Returns:
            bool: True if factory pattern is confidently absent
        """
        if not code:
            return True
            
        confidence = self.calculate_confidence_score(code)
        has_factory_indicators = self.has_pattern_implemented(code)
        
        return confidence < threshold and not has_factory_indicators

    def __call__(self, code, before_code=None, threshold=0.3):
        """
        Validate factory pattern implementation.
        
        Args:
            code (str): Current code to analyze
            before_code (str, optional): Previous code version for comparison
            threshold (float): Confidence threshold for pattern detection
            
        Returns:
            bool: True if factory pattern is confidently found
        """
        confidence = self.calculate_confidence_score(code)
        current_has_pattern = confidence >= threshold and self.has_pattern_implemented(code)
        
        if before_code is not None:
            return current_has_pattern and self.is_pattern_absent(before_code)
            
        return current_has_pattern
