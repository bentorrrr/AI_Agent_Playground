"""
Utility functions for the tech stock scraper.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any
import time


def save_to_json(data: List[Dict[str, Any]], filepath: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: List of dictionaries to save
        filepath: Path to the output file
    """
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Data saved to {filepath}")


def load_from_json(filepath: str) -> List[Dict[str, Any]]:
    """
    Load data from a JSON file.
    
    Args:
        filepath: Path to the input file
        
    Returns:
        List of dictionaries loaded from file
    """
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def merge_and_deduplicate(existing_data: List[Dict[str, Any]], 
                          new_data: List[Dict[str, Any]], 
                          key: str = 'url') -> List[Dict[str, Any]]:
    """
    Merge new data with existing data and remove duplicates.
    
    Args:
        existing_data: Existing data list
        new_data: New data to merge
        key: Key to use for deduplication
        
    Returns:
        Merged and deduplicated data
    """
    # Create a set of existing keys
    existing_keys = {item.get(key) for item in existing_data if item.get(key)}
    
    # Add only new items
    for item in new_data:
        if item.get(key) not in existing_keys:
            existing_data.append(item)
            existing_keys.add(item.get(key))
    
    return existing_data


def rate_limit(delay: float = 1.0):
    """
    Decorator to add rate limiting to functions.
    
    Args:
        delay: Delay in seconds between function calls
    """
    def decorator(func):
        last_called = [0.0]
        
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < delay:
                time.sleep(delay - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        
        return wrapper
    return decorator


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


def filter_by_date(data: List[Dict[str, Any]], 
                   date_field: str = 'published_date',
                   days: int = 7) -> List[Dict[str, Any]]:
    """
    Filter data to only include items from the last N days.
    
    Args:
        data: List of data items
        date_field: Field name containing the date
        days: Number of days to include
        
    Returns:
        Filtered data list
    """
    from datetime import timedelta
    
    cutoff_date = datetime.now() - timedelta(days=days)
    filtered_data = []
    
    for item in data:
        if date_field in item:
            try:
                item_date = datetime.fromisoformat(item[date_field].replace('Z', '+00:00'))
                if item_date >= cutoff_date:
                    filtered_data.append(item)
            except (ValueError, AttributeError):
                # If date parsing fails, include the item
                filtered_data.append(item)
    
    return filtered_data


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and special characters.
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()
