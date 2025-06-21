"""
Input Validation Utilities
==========================

This module provides utilities for validating tool arguments against JSON schemas.
"""

import re
from typing import Any, Dict, List, Union


def validate_tool_arguments(arguments: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate tool arguments against a JSON schema.
    
    Args:
        arguments: The arguments to validate
        schema: The JSON schema to validate against
        
    Returns:
        Dict with 'valid' boolean and 'errors' list
    """
    errors = []
    
    try:
        # Validate required fields
        required = schema.get("required", [])
        for field in required:
            if field not in arguments:
                errors.append(f"Missing required field: '{field}'")
        
        # Validate properties
        properties = schema.get("properties", {})
        for field_name, value in arguments.items():
            if field_name in properties:
                field_schema = properties[field_name]
                field_errors = _validate_field(value, field_schema, field_name)
                errors.extend(field_errors)
            elif not schema.get("additionalProperties", False):
                errors.append(f"Unknown field: '{field_name}'")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
        
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Validation error: {str(e)}"]
        }


def _validate_field(value: Any, field_schema: Dict[str, Any], field_name: str) -> List[str]:
    """Validate a single field against its schema."""
    errors = []
    
    # Handle null values
    if value is None:
        if "null" not in field_schema.get("type", []):
            errors.append(f"Field '{field_name}' cannot be null")
        return errors
    
    # Type validation
    expected_types = field_schema.get("type")
    if expected_types:
        if isinstance(expected_types, str):
            expected_types = [expected_types]
        
        if not _validate_type(value, expected_types):
            errors.append(f"Field '{field_name}' must be of type {expected_types}, got {type(value).__name__}")
            return errors  # Don't continue validation if type is wrong
    
    # String validations
    if isinstance(value, str):
        errors.extend(_validate_string(value, field_schema, field_name))
    
    # Number validations
    elif isinstance(value, (int, float)):
        errors.extend(_validate_number(value, field_schema, field_name))
    
    # Array validations
    elif isinstance(value, list):
        errors.extend(_validate_array(value, field_schema, field_name))
    
    # Object validations
    elif isinstance(value, dict):
        errors.extend(_validate_object(value, field_schema, field_name))
    
    # Enum validation
    if "enum" in field_schema:
        if value not in field_schema["enum"]:
            errors.append(f"Field '{field_name}' must be one of {field_schema['enum']}, got '{value}'")
    
    return errors


def _validate_type(value: Any, expected_types: List[str]) -> bool:
    """Check if value matches any of the expected types."""
    type_mapping = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "array": list,
        "object": dict,
        "null": type(None)
    }
    
    for expected_type in expected_types:
        if expected_type in type_mapping:
            if isinstance(value, type_mapping[expected_type]):
                return True
    
    return False


def _validate_string(value: str, schema: Dict[str, Any], field_name: str) -> List[str]:
    """Validate string-specific constraints."""
    errors = []
    
    # Length constraints
    if "minLength" in schema and len(value) < schema["minLength"]:
        errors.append(f"Field '{field_name}' must be at least {schema['minLength']} characters long")
    
    if "maxLength" in schema and len(value) > schema["maxLength"]:
        errors.append(f"Field '{field_name}' must be at most {schema['maxLength']} characters long")
    
    # Pattern validation
    if "pattern" in schema:
        if not re.match(schema["pattern"], value):
            errors.append(f"Field '{field_name}' does not match required pattern")
    
    # Format validation
    if "format" in schema:
        format_type = schema["format"]
        if format_type == "uri":
            if not _is_valid_uri(value):
                errors.append(f"Field '{field_name}' must be a valid URI")
        elif format_type == "email":
            if not _is_valid_email(value):
                errors.append(f"Field '{field_name}' must be a valid email address")
    
    return errors


def _validate_number(value: Union[int, float], schema: Dict[str, Any], field_name: str) -> List[str]:
    """Validate number-specific constraints."""
    errors = []
    
    # Range constraints
    if "minimum" in schema and value < schema["minimum"]:
        errors.append(f"Field '{field_name}' must be at least {schema['minimum']}")
    
    if "maximum" in schema and value > schema["maximum"]:
        errors.append(f"Field '{field_name}' must be at most {schema['maximum']}")
    
    if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
        errors.append(f"Field '{field_name}' must be greater than {schema['exclusiveMinimum']}")
    
    if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
        errors.append(f"Field '{field_name}' must be less than {schema['exclusiveMaximum']}")
    
    # Multiple constraint
    if "multipleOf" in schema and value % schema["multipleOf"] != 0:
        errors.append(f"Field '{field_name}' must be a multiple of {schema['multipleOf']}")
    
    return errors


def _validate_array(value: List[Any], schema: Dict[str, Any], field_name: str) -> List[str]:
    """Validate array-specific constraints."""
    errors = []
    
    # Length constraints
    if "minItems" in schema and len(value) < schema["minItems"]:
        errors.append(f"Field '{field_name}' must have at least {schema['minItems']} items")
    
    if "maxItems" in schema and len(value) > schema["maxItems"]:
        errors.append(f"Field '{field_name}' must have at most {schema['maxItems']} items")
    
    # Item validation
    if "items" in schema:
        item_schema = schema["items"]
        for i, item in enumerate(value):
            item_errors = _validate_field(item, item_schema, f"{field_name}[{i}]")
            errors.extend(item_errors)
    
    # Uniqueness
    if schema.get("uniqueItems", False):
        if len(value) != len(set(str(item) for item in value)):
            errors.append(f"Field '{field_name}' must contain unique items")
    
    return errors


def _validate_object(value: Dict[str, Any], schema: Dict[str, Any], field_name: str) -> List[str]:
    """Validate object-specific constraints."""
    errors = []
    
    # Property count constraints
    if "minProperties" in schema and len(value) < schema["minProperties"]:
        errors.append(f"Field '{field_name}' must have at least {schema['minProperties']} properties")
    
    if "maxProperties" in schema and len(value) > schema["maxProperties"]:
        errors.append(f"Field '{field_name}' must have at most {schema['maxProperties']} properties")
    
    # Required properties
    required = schema.get("required", [])
    for prop in required:
        if prop not in value:
            errors.append(f"Field '{field_name}' is missing required property '{prop}'")
    
    # Validate properties
    properties = schema.get("properties", {})
    for prop_name, prop_value in value.items():
        if prop_name in properties:
            prop_schema = properties[prop_name]
            prop_errors = _validate_field(prop_value, prop_schema, f"{field_name}.{prop_name}")
            errors.extend(prop_errors)
        elif not schema.get("additionalProperties", True):
            errors.append(f"Field '{field_name}' has unexpected property '{prop_name}'")
    
    return errors


def _is_valid_uri(value: str) -> bool:
    """Check if string is a valid URI."""
    uri_pattern = re.compile(
        r'^[a-zA-Z][a-zA-Z\d+\-\.]*:'  # scheme
        r'//(?:[^\s/?#]*)/?'           # authority and path start
        r'(?:[^\s]*)?$'                # rest of URI
    )
    return bool(uri_pattern.match(value))


def _is_valid_email(value: str) -> bool:
    """Check if string is a valid email address."""
    email_pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    return bool(email_pattern.match(value))


def sanitize_input(value: Any) -> Any:
    """
    Sanitize input values to prevent injection attacks.
    
    Args:
        value: The value to sanitize
        
    Returns:
        Sanitized value
    """
    if isinstance(value, str):
        # Remove dangerous characters for SQL injection prevention
        dangerous_chars = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_']
        sanitized = value
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # Limit length to prevent buffer overflow
        if len(sanitized) > 10000:
            sanitized = sanitized[:10000]
        
        return sanitized.strip()
    
    elif isinstance(value, list):
        return [sanitize_input(item) for item in value]
    
    elif isinstance(value, dict):
        return {key: sanitize_input(val) for key, val in value.items()}
    
    else:
        return value


def validate_file_path(file_path: str) -> Dict[str, Any]:
    """
    Validate file path for security.
    
    Args:
        file_path: The file path to validate
        
    Returns:
        Dict with 'valid' boolean and 'errors' list
    """
    errors = []
    
    # Check for path traversal attempts
    if '..' in file_path:
        errors.append("File path cannot contain '..' (path traversal)")
    
    # Check for absolute paths that might access system files
    if file_path.startswith('/etc/') or file_path.startswith('/proc/') or file_path.startswith('/sys/'):
        errors.append("Access to system directories is not allowed")
    
    # Check for suspicious characters
    suspicious_chars = ['|', '&', ';', '$', '`', '<', '>']
    for char in suspicious_chars:
        if char in file_path:
            errors.append(f"File path cannot contain '{char}'")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }