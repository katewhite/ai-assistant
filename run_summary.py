#!/usr/bin/env python3
"""
Streamlined script to generate weekly summary - runs everything in one go.
This script is designed to be called directly from Claude Code without approval steps.
"""

import sys
import re
from datetime import datetime
from granola_reader import get_meetings_in_range, get_last_friday_range, get_week_label
from prompt_template import get_summary_prompt_for_meetings, WEEKLY_SUMMARY_INSTRUCTIONS
from notion_helper import upload_to_notion


def extract_features_from_summary(summary_text):
    """Extract feature names from the Product Development Focus section."""
    features = []
    match = re.search(r'### 👩‍💻 Product Development Focus\s*\n\n(.*?)\n\n###', summary_text, re.DOTALL)
    if match:
        section = match.group(1)
        feature_matches = re.findall(r'\*\*([^*]+)\*\*', section)
        features = [f.strip() for f in feature_matches]
    return features


def extract_customer_call_count(summary_text):
    """Extract customer call count from the Customer Calls section."""
    match = re.search(r'\*\*Total customer calls:\*\* (\d+)', summary_text)
    if match:
        return int(match.group(1))
    return 0


def main():
    """Main execution - fetch meetings, output prompt for Claude Code to process."""
    print("🔄 Generating weekly Granola summary...")
    print()

    # Step 1: Get meetings from Granola
    print("📅 Loading meetings from Granola...")
    try:
        start, end = get_last_friday_range()
        meetings = get_meetings_in_range(start, end)
        week_label = get_week_label(start, end)

        print(f"   Week: {week_label}")
        print(f"   Date range: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
        print(f"   Found {len(meetings)} personal meetings")
        print()

        if len(meetings) == 0:
            print("❌ No meetings found for this week.")
            return 1

        # Step 2: Generate the prompt
        prompt = get_summary_prompt_for_meetings(meetings)

        # Output prompt to a temp file for Claude Code to read
        prompt_file = '/tmp/granola_summary_prompt.txt'
        with open(prompt_file, 'w') as f:
            f.write(prompt)

        print(f"✅ Prompt ready with {len(meetings)} meetings")
        print(f"📄 Saved to: {prompt_file}")
        print()

        # Output the meetings metadata for Claude Code to use
        print("📊 Meetings Summary:")
        for i, m in enumerate(meetings, 1):
            external = "✓" if m.get('has_external_attendees') else "○"
            print(f"   {i}. [{external}] {m['title']} ({m['attendee_count']} attendees)")
        print()

        # Return the data Claude Code needs
        return {
            'week_label': week_label,
            'week_start': start,
            'reflection_date': datetime.now(),
            'meetings': meetings,
            'prompt_file': prompt_file
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


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
            'meeting_count': len(result['meetings']),
            'prompt_file': result['prompt_file']
        }, indent=2))
        print("="*60)
    else:
        sys.exit(result if isinstance(result, int) else 1)
