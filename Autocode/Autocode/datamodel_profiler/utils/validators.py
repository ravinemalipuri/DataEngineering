"""
Validators for semantic type detection.
"""

import re
import uuid
from typing import Optional, Pattern
from datetime import datetime
from .types import SemanticType


class BaseValidator:
    """Base class for semantic type validators."""
    
    def __init__(self, pattern: Pattern, semantic_type: SemanticType):
        self.pattern = pattern
        self.semantic_type = semantic_type
    
    def validate(self, value: str) -> bool:
        """Validate if value matches the semantic type."""
        if not isinstance(value, str):
            return False
        return bool(self.pattern.match(value.strip()))


class EmailValidator(BaseValidator):
    """Email address validator."""
    
    def __init__(self):
        pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        super().__init__(pattern, SemanticType.EMAIL)


class UUIDValidator(BaseValidator):
    """UUID validator."""
    
    def __init__(self):
        pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        super().__init__(pattern, SemanticType.UUID)
    
    def validate(self, value: str) -> bool:
        """Validate UUID with both regex and uuid module."""
        if not isinstance(value, str):
            return False
        
        # Try regex first
        if not super().validate(value):
            return False
        
        # Double-check with uuid module
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False


class URLValidator(BaseValidator):
    """URL validator."""
    
    def __init__(self):
        pattern = re.compile(
            r'^https?://[^\s/$.?#].[^\s]*$'
        )
        super().__init__(pattern, SemanticType.URL)


class PhoneValidator(BaseValidator):
    """Phone number validator."""
    
    def __init__(self):
        pattern = re.compile(
            r'^\+?[\d\s\-\(\)]{10,}$'
        )
        super().__init__(pattern, SemanticType.PHONE)


class CurrencyValidator(BaseValidator):
    """Currency amount validator."""
    
    def __init__(self):
        pattern = re.compile(
            r'^\$?[\d,]+\.?\d{0,2}$'
        )
        super().__init__(pattern, SemanticType.CURRENCY)


class PercentageValidator(BaseValidator):
    """Percentage validator."""
    
    def __init__(self):
        pattern = re.compile(
            r'^\d+\.?\d*%?$'
        )
        super().__init__(pattern, SemanticType.PERCENTAGE)


class PostalCodeValidator(BaseValidator):
    """Postal code validator (US format)."""
    
    def __init__(self):
        pattern = re.compile(
            r'^\d{5}(-\d{4})?$'
        )
        super().__init__(pattern, SemanticType.POSTAL_CODE)


class CreditCardValidator(BaseValidator):
    """Credit card validator."""
    
    def __init__(self):
        pattern = re.compile(
            r'^\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}$'
        )
        super().__init__(pattern, SemanticType.CREDIT_CARD)


class IPAddressValidator(BaseValidator):
    """IP address validator."""
    
    def __init__(self):
        pattern = re.compile(
            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        )
        super().__init__(pattern, SemanticType.IP_ADDRESS)


class MACAddressValidator(BaseValidator):
    """MAC address validator."""
    
    def __init__(self):
        pattern = re.compile(
            r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        )
        super().__init__(pattern, SemanticType.MAC_ADDRESS)


class SSNValidator(BaseValidator):
    """Social Security Number validator."""
    
    def __init__(self):
        pattern = re.compile(
            r'^\d{3}-\d{2}-\d{4}$'
        )
        super().__init__(pattern, SemanticType.SSN)


class DateValidator(BaseValidator):
    """Date validator."""
    
    def __init__(self):
        # Common date formats
        patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{2}/\d{2}/\d{4}$',  # MM/DD/YYYY
            r'^\d{2}-\d{2}-\d{4}$',  # MM-DD-YYYY
            r'^\d{4}/\d{2}/\d{2}$',  # YYYY/MM/DD
        ]
        self.patterns = [re.compile(p) for p in patterns]
        self.semantic_type = SemanticType.GENERIC  # Will be set to DATE if valid
    
    def validate(self, value: str) -> bool:
        """Validate date format and try to parse."""
        if not isinstance(value, str):
            return False
        
        # Check format first
        if not any(p.match(value.strip()) for p in self.patterns):
            return False
        
        # Try to parse the date
        try:
            datetime.strptime(value.strip(), '%Y-%m-%d')
            return True
        except ValueError:
            try:
                datetime.strptime(value.strip(), '%m/%d/%Y')
                return True
            except ValueError:
                try:
                    datetime.strptime(value.strip(), '%m-%d-%Y')
                    return True
                except ValueError:
                    try:
                        datetime.strptime(value.strip(), '%Y/%m/%d')
                        return True
                    except ValueError:
                        return False


class SemanticTypeDetector:
    """Detects semantic types for values."""
    
    def __init__(self):
        self.validators = {
            SemanticType.EMAIL: EmailValidator(),
            SemanticType.UUID: UUIDValidator(),
            SemanticType.URL: URLValidator(),
            SemanticType.PHONE: PhoneValidator(),
            SemanticType.CURRENCY: CurrencyValidator(),
            SemanticType.PERCENTAGE: PercentageValidator(),
            SemanticType.POSTAL_CODE: PostalCodeValidator(),
            SemanticType.CREDIT_CARD: CreditCardValidator(),
            SemanticType.IP_ADDRESS: IPAddressValidator(),
            SemanticType.MAC_ADDRESS: MACAddressValidator(),
            SemanticType.SSN: SSNValidator(),
        }
        self.date_validator = DateValidator()
    
    def detect_semantic_type(self, values: list, threshold: float = 0.8) -> SemanticType:
        """
        Detect semantic type for a list of values.
        
        Args:
            values: List of values to analyze
            threshold: Minimum percentage of values that must match for detection
            
        Returns:
            Detected semantic type or GENERIC if no match
        """
        if not values:
            return SemanticType.GENERIC
        
        # Convert to strings and filter out nulls
        str_values = [str(v) for v in values if v is not None and str(v).strip()]
        
        if not str_values:
            return SemanticType.GENERIC
        
        # Test each semantic type
        for semantic_type, validator in self.validators.items():
            matches = sum(1 for v in str_values if validator.validate(v))
            match_rate = matches / len(str_values)
            
            if match_rate >= threshold:
                return semantic_type
        
        # Test date separately
        if self.date_validator.validate(str_values[0]):
            matches = sum(1 for v in str_values if self.date_validator.validate(v))
            match_rate = matches / len(str_values)
            
            if match_rate >= threshold:
                return SemanticType.GENERIC  # Will be handled as date in data type detection
        
        return SemanticType.GENERIC
