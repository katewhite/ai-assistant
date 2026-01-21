"""
Module for parsing KR metrics from user command input.
"""

import re
from typing import Dict, Optional, Tuple, List


# KR definitions with targets and baselines
KR_DEFINITIONS = {
    "experience_launch": {
        "name": "Experience launch success rate",
        "target": 80.0,
        "baseline": 75.0,
        "unit": "%",
        "keywords": ["experience launch", "launch success", "launch rate", "experience launch success"]
    },
    "quick_end": {
        "name": "Quick-End rate",
        "target": 10.0,
        "baseline": 14.0,
        "unit": "%",
        "keywords": ["quick-end", "quick end", "quickend", "quick end rate"]
    },
    "components": {
        "name": "% accounts with live components",
        "target": 5.0,
        "baseline": 2.42,
        "unit": "%",
        "keywords": ["components", "component adoption", "live components", "accounts with components"]
    },
    "editor_problems": {
        "name": "On-site editor problems",
        "target": 60.0,
        "baseline": 120.0,
        "unit": "mentions/month",
        "keywords": ["editor problems", "editor issues", "on-site editor", "reforge mentions"]
    }
}


def parse_metrics_from_input(user_input: str) -> Dict[str, Optional[float]]:
    """
    Extract metric values from user's command message.
    
    Args:
        user_input: User's command message containing metrics
    
    Returns:
        Dict with keys: experience_launch, quick_end, components, editor_problems
        Values are floats or None if not found
    """
    user_input_lower = user_input.lower()
    metrics = {
        "experience_launch": None,
        "quick_end": None,
        "components": None,
        "editor_problems": None
    }
    
    # Try to find each metric using various patterns
    for metric_key, metric_info in KR_DEFINITIONS.items():
        # Pattern 1: Look for structured format like "launch: 77%" or "launch=77%"
        for keyword in metric_info["keywords"]:
            # Pattern: keyword: number or keyword=number
            pattern1 = rf"{re.escape(keyword)}\s*[:=]\s*([\d.]+)"
            match = re.search(pattern1, user_input_lower, re.IGNORECASE)
            if match:
                try:
                    value = float(match.group(1))
                    metrics[metric_key] = value
                    break
                except ValueError:
                    continue
            
            # Pattern 2: Look for "keyword is number" or "keyword number"
            pattern2 = rf"{re.escape(keyword)}\s+(?:is\s+)?([\d.]+)"
            match = re.search(pattern2, user_input_lower, re.IGNORECASE)
            if match:
                try:
                    value = float(match.group(1))
                    metrics[metric_key] = value
                    break
                except ValueError:
                    continue
            
            # Pattern 3: Look for number followed by keyword (e.g., "77% experience launch")
            pattern3 = rf"([\d.]+)\s*%?\s*{re.escape(keyword)}"
            match = re.search(pattern3, user_input_lower, re.IGNORECASE)
            if match:
                try:
                    value = float(match.group(1))
                    metrics[metric_key] = value
                    break
                except ValueError:
                    continue
    
    return metrics


def validate_metrics(metrics_dict: Dict[str, Optional[float]]) -> Tuple[bool, List[str]]:
    """
    Validate that all 4 KRs are provided.
    
    Args:
        metrics_dict: Dictionary of parsed metrics
    
    Returns:
        Tuple of (is_valid, list_of_missing_metrics)
    """
    missing = []
    for key, value in metrics_dict.items():
        if value is None:
            missing.append(KR_DEFINITIONS[key]["name"])
    
    return len(missing) == 0, missing


def format_metrics_for_display(metrics_dict: Dict[str, Optional[float]]) -> Dict[str, Dict]:
    """
    Format metrics with targets, baselines, and progress indicators.
    
    Args:
        metrics_dict: Dictionary of parsed metrics
    
    Returns:
        Dictionary with formatted metric information including progress
    """
    formatted = {}
    
    for key, current_value in metrics_dict.items():
        if current_value is None:
            continue
            
        metric_info = KR_DEFINITIONS[key]
        target = metric_info["target"]
        baseline = metric_info["baseline"]
        
        # Calculate progress
        if key == "editor_problems":
            # For editor problems, lower is better (inverse progress)
            progress_pct = ((baseline - current_value) / (baseline - target)) * 100 if baseline != target else 0
            trending = "down" if current_value < baseline else "up"
        else:
            # For other metrics, higher is better
            progress_pct = ((current_value - baseline) / (target - baseline)) * 100 if target != baseline else 0
            trending = "up" if current_value > baseline else "down"
        
        formatted[key] = {
            "name": metric_info["name"],
            "current": current_value,
            "target": target,
            "baseline": baseline,
            "unit": metric_info["unit"],
            "progress_pct": max(0, min(100, progress_pct)),
            "trending": trending,
            "to_target": current_value - target if key != "editor_problems" else target - current_value
        }
    
    return formatted
