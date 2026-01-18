#!/usr/bin/env python3
"""
Main script to generate weekly Granola summary and upload to Notion.
Run with: python generate_summary.py
"""

import json
import re
from datetime import datetime
from granola_reader import get_meetings_in_range, get_last_friday_range, get_week_label
from prompt_template import get_summary_prompt_for_meetings
from notion_helper import upload_to_notion


def extract_features_from_summary(summary_text):
    """Extract feature names from the Product Development Focus section."""
    features = []

    # Find the Product Development Focus section
    match = re.search(r'### 👩‍💻 Product Development Focus\s*\n\n(.*?)\n\n###', summary_text, re.DOTALL)
    if match:
        section = match.group(1)
        # Extract bold feature names (between ** and **)
        feature_matches = re.findall(r'\*\*([^*]+)\*\*', section)
        features = [f.strip() for f in feature_matches]

    return features


def extract_customer_call_count(summary_text):
    """Extract customer call count from the Customer Calls section."""
    match = re.search(r'\*\*Total customer calls:\*\* (\d+)', summary_text)
    if match:
        return int(match.group(1))
    return 0


def generate_summary_with_ai(meetings, week_label):
    """
    Generate summary using AI prompt.
    This is a placeholder - you'll need to implement this with your preferred AI method.
    For now, it returns a template message.
    """
    print("⚠️  AI summary generation not yet implemented in this script.")
    print("Please manually generate the summary using the prompt, or implement AI integration.")
    print()

    # Save meetings to temp file for manual processing
    prompt = get_summary_prompt_for_meetings(meetings)

    temp_file = '/tmp/granola_summary_prompt.txt'
    with open(temp_file, 'w') as f:
        f.write(prompt)

    print(f"📄 Prompt saved to: {temp_file}")
    print("You can use this prompt with Claude or another AI to generate the summary.")
    print()

    return None


def main():
    print("🔄 Generating weekly Granola summary...")
    print()

    # Step 1: Get meetings
    print("📅 Step 1: Loading meetings from Granola...")
    start, end = get_last_friday_range()
    meetings = get_meetings_in_range(start, end)
    week_label = get_week_label(start, end)

    print(f"   Week: {week_label}")
    print(f"   Date range: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
    print(f"   Found {len(meetings)} personal meetings")
    print()

    if len(meetings) == 0:
        print("❌ No meetings found for this week. Exiting.")
        return

    # Step 2: Generate summary (manual for now)
    print("📝 Step 2: Generating summary...")
    summary_text = generate_summary_with_ai(meetings, week_label)

    if summary_text is None:
        print()
        print("💡 Manual process:")
        print("   1. Copy the prompt from /tmp/granola_summary_prompt.txt")
        print("   2. Use it with Claude to generate the summary")
        print("   3. Save the output to /tmp/weekly_summary.md")
        print("   4. Run this script again")
        print()

        # Check if manual summary exists
        try:
            with open('/tmp/weekly_summary.md', 'r') as f:
                summary_text = f.read()
            print("✅ Found existing summary at /tmp/weekly_summary.md")
        except FileNotFoundError:
            print("⏸️  Waiting for manual summary generation...")
            return

    print()

    # Step 3: Extract metadata
    print("🔍 Step 3: Extracting metadata...")

    # Extract HIGH-LEVEL SUMMARY
    high_level_match = re.search(r'HIGH-LEVEL SUMMARY:\s*\n\n(.*?)\n\n---', summary_text, re.DOTALL)
    if high_level_match:
        notes_summary = high_level_match.group(1).strip()
        # Remove HIGH-LEVEL SUMMARY from main content
        summary_content = re.sub(r'HIGH-LEVEL SUMMARY:.*?\n\n---\n\n', '', summary_text, count=1, flags=re.DOTALL)
    else:
        notes_summary = f"Week focused on product development and strategic planning."
        summary_content = summary_text

    # Extract features and customer calls
    features = extract_features_from_summary(summary_text)
    customer_call_count = extract_customer_call_count(summary_text)

    print(f"   Features: {len(features)} - {', '.join(features[:3])}{'...' if len(features) > 3 else ''}")
    print(f"   Customer Calls: {customer_call_count}")
    print(f"   Notes: {notes_summary[:80]}...")
    print()

    # Step 4: Upload to Notion
    print("☁️  Step 4: Uploading to Notion...")

    try:
        page_url = upload_to_notion(
            summary_content,
            week_label,
            week_start_date=start,
            reflection_date=datetime.now(),
            customer_call_count=customer_call_count,
            notes_summary=notes_summary,
            features=features
        )

        print()
        print("✅ Success! Your weekly summary is in Notion:")
        print(f"   {page_url}")
        print()

    except Exception as e:
        print()
        print(f"❌ Error uploading to Notion: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
