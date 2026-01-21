#!/usr/bin/env python3
"""
Generate End of Week (EOW) pillar update for Core Experiences pillar.
Fetches Slack messages, Granola calls, and generates a formatted update.
"""

import os
import sys
import re
from datetime import datetime
from slack_reader import (
    get_slack_client,
    get_messages_in_range,
    send_dm_to_user,
    get_user_id_by_email
)
from granola_reader import get_meetings_in_range, get_last_friday_range, get_week_label
from pillar_eow_template import get_eow_prompt_for_data
from metrics_parser import (
    parse_metrics_from_input,
    validate_metrics,
    format_metrics_for_display
)
from config import SLACK_CHANNELS, SLACK_USER_EMAIL


def filter_pillar_relevant_content(slack_messages, granola_meetings):
    """
    Filter content for Core Experiences pillar relevance.
    
    Args:
        slack_messages: List of Slack message dicts
        granola_meetings: List of Granola meeting dicts
    
    Returns:
        Tuple of (filtered_slack_messages, filtered_granola_meetings)
    """
    # Keywords to identify Core Experiences pillar content
    pillar_keywords = [
        "core experiences",
        "experience launch",
        "quick-end",
        "quick end",
        "component",
        "editor",
        "on-site editor",
        "test creation",
        "experience editing",
        "friction",
        "high volume",
        "reforge"
    ]
    
    filtered_slack = []
    for msg in slack_messages:
        text_lower = msg.get("text", "").lower()
        # Include if any keyword is mentioned
        if any(keyword in text_lower for keyword in pillar_keywords):
            filtered_slack.append(msg)
        # Also include if from pillar channel
        elif "pillar-core-experiences" in msg.get("channel_name", "").lower():
            filtered_slack.append(msg)
    
    filtered_meetings = []
    for meeting in granola_meetings:
        title_lower = meeting.get("title", "").lower()
        notes_lower = meeting.get("notes", "").lower()
        transcript_lower = meeting.get("transcript", "").lower()
        
        # Include if any keyword is in title, notes, or transcript
        combined_text = f"{title_lower} {notes_lower} {transcript_lower}"
        if any(keyword in combined_text for keyword in pillar_keywords):
            filtered_meetings.append(meeting)
    
    return filtered_slack, filtered_meetings


def main():
    """Main execution."""
    print("🔄 Generating Core Experiences pillar EOW update...")
    print()
    
    # Step 1: Parse metrics from user input
    print("📊 Step 1: Parsing KR metrics from input...")
    user_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    
    if not user_input:
        print("❌ Error: No metrics provided in command")
        print("   Usage: python generate_pillar_eow.py 'launch: 77%, quickend: 12%, components: 3.2%, editor: 95'")
        print("   Or provide metrics in natural language")
        sys.exit(1)
    
    metrics = parse_metrics_from_input(user_input)
    is_valid, missing = validate_metrics(metrics)
    
    if not is_valid:
        print(f"⚠️  Warning: Missing metrics: {', '.join(missing)}")
        print("   Continuing with available metrics...")
        print()
    
    formatted_metrics = format_metrics_for_display(metrics)
    print(f"   Parsed {len([m for m in metrics.values() if m is not None])} metrics")
    for key, value in metrics.items():
        if value is not None:
            print(f"   - {formatted_metrics[key]['name']}: {value}{formatted_metrics[key]['unit']}")
    print()
    
    # Step 2: Get date range
    print("📅 Step 2: Getting date range...")
    start, end = get_last_friday_range()
    week_label = get_week_label(start, end)
    print(f"   Week: {week_label}")
    print(f"   Date range: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
    print()
    
    # Step 3: Fetch Slack messages
    print("💬 Step 3: Fetching Slack messages...")
    slack_messages = []
    try:
        client = get_slack_client()
        slack_messages = get_messages_in_range(SLACK_CHANNELS, start, end, client)
        print(f"   Found {len(slack_messages)} total messages")
    except Exception as e:
        print(f"   ⚠️  Warning: Could not fetch Slack messages: {e}")
        print("   Continuing with Granola data only...")
    print()
    
    # Step 4: Fetch Granola calls
    print("📞 Step 4: Fetching Granola calls...")
    try:
        granola_meetings = get_meetings_in_range(start, end)
        print(f"   Found {len(granola_meetings)} meetings")
    except Exception as e:
        print(f"   ❌ Error fetching Granola calls: {e}")
        granola_meetings = []
    print()
    
    # Step 5: Filter for pillar relevance
    print("🔍 Step 5: Filtering content for pillar relevance...")
    filtered_slack, filtered_meetings = filter_pillar_relevant_content(
        slack_messages, granola_meetings
    )
    print(f"   Filtered to {len(filtered_slack)} relevant Slack messages")
    print(f"   Filtered to {len(filtered_meetings)} relevant meetings")
    print()
    
    if len(filtered_slack) == 0 and len(filtered_meetings) == 0:
        print("⚠️  Warning: No relevant content found for this week")
        print("   Generating update with metrics only...")
        print()
    
    # Step 6: Generate prompt
    print("📝 Step 6: Generating AI prompt...")
    prompt = get_eow_prompt_for_data(
        formatted_metrics,
        filtered_slack,
        filtered_meetings,
        week_label
    )
    print(f"   Prompt length: {len(prompt)} characters")
    print()
    
    # Step 7: Save prompt to file for Claude to process
    prompt_file = '/tmp/pillar_eow_prompt.txt'
    with open(prompt_file, 'w') as f:
        f.write(prompt)
    
    print(f"✅ Prompt ready with {len(filtered_slack)} Slack messages and {len(filtered_meetings)} meetings")
    print(f"📄 Saved to: {prompt_file}")
    print()
    
    # Output summary for Claude
    print("📊 Summary:")
    print(f"   Week: {week_label}")
    print(f"   Metrics: {len([m for m in metrics.values() if m is not None])}/4")
    print(f"   Relevant Slack messages: {len(filtered_slack)}")
    print(f"   Relevant meetings: {len(filtered_meetings)}")
    print()
    
    # Return metadata for Claude to use
    return {
        'week_label': week_label,
        'week_start': start,
        'reflection_date': datetime.now(),
        'prompt_file': prompt_file,
        'metrics': formatted_metrics,
        'slack_count': len(filtered_slack),
        'meetings_count': len(filtered_meetings),
        'filtered_slack': filtered_slack,
        'filtered_meetings': filtered_meetings
    }


if __name__ == "__main__":
    result = main()
    if isinstance(result, dict):
        # Success - output metadata for Claude Code
        import json
        print("\n" + "="*60)
        print("METADATA FOR CLAUDE CODE:")
        print(json.dumps({
            'week_label': result['week_label'],
            'week_start': result['week_start'].strftime('%Y-%m-%d'),
            'prompt_file': result['prompt_file'],
            'metrics_count': len([m for m in result['metrics'].values() if m]),
            'slack_count': result['slack_count'],
            'meetings_count': result['meetings_count']
        }, indent=2))
        print("="*60)
    else:
        sys.exit(result if isinstance(result, int) else 1)
