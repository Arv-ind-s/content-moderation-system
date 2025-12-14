"""
Text preprocessing utilities for content moderation.
Applies the same cleaning used during training.
"""

import re


def clean_text(text: str) -> str:
    """
    Clean text while preserving toxicity signals.
    
    Args:
        text: Raw input text
        
    Returns:
        Cleaned text ready for model inference
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove newlines and tabs
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    
    # Remove URLs
    url_pattern = r'https?://\S+|www\.\S+'
    text = re.sub(url_pattern, '', text)
    
    # Remove IP addresses
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    text = re.sub(ip_pattern, '', text)
    
    # Remove email addresses
    email_pattern = r'\S+@\S+'
    text = re.sub(email_pattern, '', text)
    
    # Remove Wikipedia markup
    wiki_pattern = r'\[\[.*?\]\]'
    text = re.sub(wiki_pattern, '', text)
    
    # Normalize whitespace (multiple spaces to single space)
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing spaces
    text = text.strip()
    
    return text


def validate_text(text: str, max_length: int = 5000) -> tuple[bool, str]:
    """
    Validate input text.
    
    Args:
        text: Input text to validate
        max_length: Maximum allowed length
        
    Returns:
        (is_valid, error_message)
    """
    if not text:
        return False, "Text cannot be empty"
    
    if not isinstance(text, str):
        return False, "Text must be a string"
    
    if len(text) > max_length:
        return False, f"Text exceeds maximum length of {max_length} characters"
    
    # Check if text becomes empty after cleaning
    cleaned = clean_text(text)
    if not cleaned or len(cleaned.strip()) == 0:
        return False, "Text is empty after preprocessing"
    
    return True, ""