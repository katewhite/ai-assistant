#!/usr/bin/env python3
"""
Complete workflow: Read prompt, generate summary with Claude API, upload to Notion
"""

import os
import re
import sys
from datetime import datetime, timezone
from anthropic import Anthropic
from notion_helper import upload_to_notion
from granola_reader import get_last_friday_range, get_week_label, get_meetings_in_range
from prompt_template import get_direct_reports_prompt_for_meetings
from direct_reports_helper import update_direct_reports_pages
from slack_reader import get_slack_messages_for_week
from config import WEEKLY_JOURNALING_SLACK_CHANNELS, SLACK_USER_EMAIL, SLACK_BOT_TOKEN

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


def generate_summary_with_claude(prompt_text):
    """Generate summary using Claude API."""
    print("🤖 Generating summary with Claude API...")

    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("   Please set it with: export ANTHROPIC_API_KEY='your_key_here'")
        sys.exit(1)

    # Initialize client
    client = Anthropic(api_key=api_key)

    # Call Claude API
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            messages=[
                {"role": "user", "content": prompt_text}
            ]
        )

        summary = message.content[0].text
        print("✅ Summary generated successfully")
        return summary

    except Exception as e:
        print(f"❌ Error calling Claude API: {e}")
        sys.exit(1)


def main():
    print("🔄 Running complete weekly journaling workflow...\n")

    # Step 1: Get week metadata and meetings
    print("📅 Step 1: Getting week metadata and meetings...")
    start, end = get_last_friday_range()
    week_label = get_week_label(start, end)
    meetings = get_meetings_in_range(start, end)
    print(f"   Week: {week_label}")
    print(f"   Date range: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
    print(f"   Found {len(meetings)} personal meetings\n")

    if len(meetings) == 0:
        print("❌ No meetings found for this week.")
        sys.exit(1)

    # Step 2: Fetch Slack messages
    slack_messages = []
    if SLACK_BOT_TOKEN:
        print("📱 Step 2: Fetching Slack messages...")
        try:
            # Ensure dates are timezone-aware for Slack API
            start_tz = start.replace(tzinfo=timezone.utc) if start.tzinfo is None else start
            end_tz = end.replace(tzinfo=timezone.utc) if end.tzinfo is None else end
            slack_messages = get_slack_messages_for_week(
                start_tz,
                end_tz,
                SLACK_USER_EMAIL,
                WEEKLY_JOURNALING_SLACK_CHANNELS
            )
            print(f"   Found {len(slack_messages)} Slack messages\n")
        except Exception as e:
            print(f"   ⚠️  Warning: Error fetching Slack messages: {e}")
            print("   Continuing with meetings only...\n")
    else:
        print("   ⚠️  No SLACK_BOT_TOKEN found, skipping Slack messages...\n")

    # Step 3: Read the weekly summary prompt
    print("📖 Step 3: Reading weekly summary prompt from /tmp/granola_summary_prompt.txt")
    try:
        with open('/tmp/granola_summary_prompt.txt', 'r') as f:
            prompt = f.read()
        print(f"   Loaded {len(prompt)} characters\n")
    except FileNotFoundError:
        print("❌ Prompt file not found. Run run_summary.py first.")
        sys.exit(1)

    # Step 4: Generate weekly summary with Claude
    print("📝 Step 4: Generating weekly summary with Claude API...")
    summary_text = generate_summary_with_claude(prompt)

    # Save the summary
    summary_file = '/tmp/weekly_summary.md'
    with open(summary_file, 'w') as f:
        f.write(summary_text)
    print(f"   Saved summary to {summary_file}\n")

    # Step 5: Generate direct reports notes
    print("👥 Step 5: Generating direct reports notes with Claude API...")
    direct_reports_prompt = get_direct_reports_prompt_for_meetings(meetings, slack_messages)
    direct_reports_text = generate_summary_with_claude(direct_reports_prompt)
    
    # Save direct reports notes
    direct_reports_file = '/tmp/direct_reports_notes.md'
    with open(direct_reports_file, 'w') as f:
        f.write(direct_reports_text)
    print(f"   Saved direct reports notes to {direct_reports_file}\n")

    # Step 6: Update direct reports pages
    print("📝 Step 6: Updating direct reports pages in Notion...")
    updated_pages = {}
    try:
        updated_pages = update_direct_reports_pages(direct_reports_text, start)
        if updated_pages:
            print(f"   Updated {len(updated_pages)} page(s):")
            for person, url in updated_pages.items():
                print(f"   - {person}: {url}")
        else:
            print("   No direct report entries to update")
        print()
    except Exception as e:
        print(f"   ⚠️  Warning: Error updating direct reports pages: {e}")
        import traceback
        traceback.print_exc()
        print()

    # Step 7: Extract metadata
    print("🔍 Step 7: Extracting metadata...")

    # Extract HIGH-LEVEL SUMMARY
    high_level_match = re.search(r'HIGH-LEVEL SUMMARY:\s*\n\n(.*?)\n\n---', summary_text, re.DOTALL)
    if high_level_match:
        notes_summary = high_level_match.group(1).strip()
        # Remove HIGH-LEVEL SUMMARY from main content
        summary_content = re.sub(r'HIGH-LEVEL SUMMARY:.*?\n\n---\n\n', '', summary_text, count=1, flags=re.DOTALL)
    else:
        notes_summary = "Week focused on product development and strategic planning."
        summary_content = summary_text

    # Extract features and customer calls
    features = extract_features_from_summary(summary_text)
    customer_call_count = extract_customer_call_count(summary_text)

    print(f"   Features: {len(features)}")
    if features:
        print(f"   - {', '.join(features[:3])}{'...' if len(features) > 3 else ''}")
    print(f"   Customer Calls: {customer_call_count}")
    print(f"   Notes Summary: {notes_summary[:80]}...\n")

    # Step 8: Upload weekly summary to Notion
    print("☁️  Step 8: Uploading weekly summary to Notion...")
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

        print("\n" + "="*60)
        print("✅ SUCCESS! Your weekly journaling is complete:")
        print(f"   Weekly Summary: {page_url}")
        if updated_pages:
            print("   Direct Reports:")
            for person, url in updated_pages.items():
                print(f"     - {person}: {url}")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Error uploading to Notion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
