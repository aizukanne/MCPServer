"""
Text Processing Utilities
========================

This module contains utilities for text processing, NLP operations,
and content extraction from web pages.
"""

import re
import json
from typing import Set, Dict, Any
from decimal import Decimal

try:
    from nltk.tokenize import sent_tokenize, word_tokenize
except ImportError:
    # Fallback implementations if NLTK is not available
    def sent_tokenize(text: str) -> list:
        """Simple sentence tokenizer fallback."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def word_tokenize(text: str) -> list:
        """Simple word tokenizer fallback."""
        return re.findall(r'\b\w+\b', text.lower())


def decimal_default(obj: Any) -> Any:
    """JSON serializer for Decimal objects."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def load_stopwords(file_path: str = 'english') -> Set[str]:
    """
    Load stopwords from a given file or use default English stopwords.

    Args:
        file_path: Path to the stopwords file or 'english' for default

    Returns:
        Set of stopwords
    """
    # Default English stopwords if file not found
    default_stopwords = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
        'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 
        'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
        'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
        'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
        'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
        'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
        'with', 'through', 'during', 'before', 'after', 'above', 'below',
        'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
        'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
        'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
        'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
        'should', 'now'
    }
    
    if file_path == 'english':
        return default_stopwords
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            stopwords = set(line.strip().lower() for line in file if line.strip())
        return stopwords
    except FileNotFoundError:
        # Return default stopwords if file not found
        return default_stopwords


def has_proper_sentences(text: str) -> bool:
    """
    Check if text contains proper sentences (with punctuation).
    
    Args:
        text: Text to check
        
    Returns:
        Boolean indicating if text has proper sentences
    """
    # Check if text has sentence-ending punctuation
    sentence_endings = ['.', '!', '?']
    sentences = sent_tokenize(text)
    
    if len(sentences) < 2:
        # If there's only one sentence or less, check if it ends properly
        return any(text.strip().endswith(ending) for ending in sentence_endings)
    
    # If there are multiple sentences, it likely has proper structure
    return True


def clean_website_data(raw_text: str) -> str:
    """
    Clean up raw website text data, removing common HTML artifacts and excess whitespace.
    
    Args:
        raw_text: Raw text extracted from HTML
        
    Returns:
        Cleaned text
    """
    try:
        # Remove HTML tags (basic HTML tag removal)
        cleaned_text = re.sub(r'<[^<]+?>', '', raw_text)

        # Remove multiple spaces and newlines, and then trim
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
        # Remove non-printing characters
        cleaned_text = ''.join(c for c in cleaned_text if c.isprintable())
        
        return cleaned_text

    except Exception as e:
        return json.dumps({"error": f"Error processing text: {str(e)}"})


def rank_sentences(text: str, stopwords: Set[str], max_sentences: int = 10) -> str:
    """
    Rank sentences in the text based on word frequency, returning top 'max_sentences' sentences.
    
    Args:
        text: Input text to process
        stopwords: Set of stopwords to ignore
        max_keywords: Maximum number of keywords to return
        
    Returns:
        List of keywords sorted by frequency
    """
    try:
        word_frequencies = {}
        words = word_tokenize(text.lower())
        
        for word in words:
            if (word.isalpha() and 
                len(word) > 2 and 
                word not in stopwords):
                word_frequencies[word] = word_frequencies.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_keywords]]
        
    except Exception:
        return []


def truncate_text(text: str, max_length: int = 1000, ellipsis: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        ellipsis: String to append if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(ellipsis)] + ellipsis


def extract_urls_from_text(text: str) -> list:
    """
    Extract URLs from text.
    
    Args:
        text: Input text
        
    Returns:
        List of URLs found in the text
    """
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return url_pattern.findall(text)


def clean_html_tags(text: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        text: Text containing HTML tags
        
    Returns:
        Text with HTML tags removed
    """
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    
    # Remove HTML entities
    clean_text = re.sub(r'&[a-zA-Z0-9#]+;', ' ', clean_text)
    
    # Clean up whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    return clean_text


def extract_emails_from_text(text: str) -> list:
    """
    Extract email addresses from text.
    
    Args:
        text: Input text
        
    Returns:
        List of email addresses found
    """
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return email_pattern.findall(text)


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.
    
    Args:
        text: Input text
        
    Returns:
        Text with normalized whitespace
    """
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of words
    """
    words = word_tokenize(text)
    return len([word for word in words if word.isalpha()])


def count_sentences(text: str) -> int:
    """
    Count sentences in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of sentences
    """
    sentences = sent_tokenize(text)
    return len(sentences)


def get_text_stats(text: str) -> Dict[str, Any]:
    """
    Get comprehensive statistics about text.
    
    Args:
        text: Input text
        
    Returns:
        Dictionary with text statistics
    """
    return {
        'character_count': len(text),
        'character_count_no_spaces': len(text.replace(' ', '')),
        'word_count': count_words(text),
        'sentence_count': count_sentences(text),
        'paragraph_count': len([p for p in text.split('\n\n') if p.strip()]),
        'average_words_per_sentence': count_words(text) / max(count_sentences(text), 1),
        'urls_found': len(extract_urls_from_text(text)),
        'emails_found': len(extract_emails_from_text(text))
    }


def is_serializable(value: Any) -> bool:
    """
    Helper function to check if a value is JSON serializable.
    
    Args:
        value: Value to check
        
    Returns:
        True if serializable, False otherwise
    """
    try:
        json.dumps(value, default=decimal_default)
        return True
    except (TypeError, OverflowError):
        return False


def smart_truncate(text: str, max_length: int = 500, prefer_sentences: bool = True) -> str:
    """
    Intelligently truncate text, preferring to break at sentence boundaries.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        prefer_sentences: Whether to prefer breaking at sentence boundaries
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    if prefer_sentences:
        sentences = sent_tokenize(text)
        result = ""
        
        for sentence in sentences:
            if len(result) + len(sentence) + 1 <= max_length - 3:  # Reserve space for "..."
                result += sentence + " "
            else:
                break
        
        if result:
            return result.strip() + "..."
    
    # Fallback to simple truncation
    return text[:max_length - 3] + "..."
        max_sentences: Maximum number of sentences to return
        
    Returns:
        Summary text with top-ranked sentences
    """
    try:
        # Calculate word frequencies
        word_frequencies = {}
        for word in word_tokenize(text.lower()):
            if word.isalpha() and word not in stopwords:  # Consider only alphabetic words
                word_frequencies[word] = word_frequencies.get(word, 0) + 1

        # Score sentences based on word frequencies
        sentence_scores = {}
        sentences = sent_tokenize(text)
        
        for sent in sentences:
            sentence_words = word_tokenize(sent.lower())
            # Only consider sentences with reasonable length
            if len(sent.split(' ')) < 30:
                score = 0
                for word in sentence_words:
                    if word in word_frequencies:
                        score += word_frequencies[word]
                
                if score > 0:  # Only include sentences with meaningful words
                    sentence_scores[sent] = score

        # Get top sentences
        if not sentence_scores:
            return text[:1000] + "..." if len(text) > 1000 else text
        
        sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        summary_sentences = [sent for sent, score in sorted_sentences[:max_sentences]]
        
        # Add a full stop at the end of each sentence if it doesn't already end with one
        summary = ' '.join([s if s.endswith(('.', '!', '?')) else f'{s}.' for s in summary_sentences])

        return summary
        
    except Exception as e:
        # Fallback to simple truncation
        return text[:2000] + "..." if len(text) > 2000 else text


def replace_problematic_chars(text: str) -> str:
    """
    Replace problematic characters for PDF generation.
    
    Args:
        text: Input text
        
    Returns:
        Text with replaced characters
    """
    replacements = {
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u201C': '"',  # Left double quotation mark
        '\u201D': '"',  # Right double quotation mark
        '\u2013': '-',  # En dash
        '\u2014': '--', # Em dash
        '\u2026': '...', # Horizontal ellipsis
        '\u00A0': ' ',  # Non-breaking space
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def extract_keywords(text: str, stopwords: Set[str], max_keywords: int = 10) -> list:
    """
    Extract keywords from text based on frequency.
    
    Args:
        text: Input text
        stopwords: Set of stopwords to ignore