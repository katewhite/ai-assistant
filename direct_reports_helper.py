"""
Helper module for managing direct reports feedback pages in Notion.
Parses AI-generated direct reports notes and updates individual Notion pages
for each direct report with reverse chronological entries grouped by month/quarter.
"""

import re
from datetime import datetime
from notion_client import Client
from config import NOTION_API_KEY, DIRECT_REPORTS_PARENT_PAGE_ID
from notion_helper import markdown_to_notion_blocks, parse_markdown_links
import time


# Valid tags for direct report entries
VALID_TAGS = ['Win', 'Coaching', 'Growth', 'Challenge', 'Initiative']
# Direct report names (case-insensitive matching)
DIRECT_REPORTS = ['Hannah', 'Jerica']


def parse_direct_reports_entries(markdown_text, week_date):
    """
    Parse AI-generated direct reports markdown and extract entries.
    
    Args:
        markdown_text: str - Markdown text from AI with direct report entries
        week_date: datetime - Date for the week (used for entry timestamps)
    
    Returns:
        dict: {person_name: [list of entry dicts]}
              Each entry dict has: tag, topic, description, meeting_link, date
    """
    entries_by_person = {}
    
    # Check if there are no entries
    if "No notable direct report moments this week" in markdown_text:
        return entries_by_person
    
    lines = markdown_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line or not line.startswith('-'):
            continue
        
        # Try to extract tag, name, topic, description, and link
        # Format: - **[Tag] [Name - Topic]** → Description ([Meeting](link))
        # Pattern: - **[TAG] [NAME - TOPIC]** → DESCRIPTION (LINK)
        match = re.match(r'- \*\*\[([^\]]+)\]\s+\[([^\]]+)\s+-\s+([^\]]+)\]\*\*\s+→\s+(.+?)(?:\s+\(([^)]+)\))?$', line)
        if not match:
            # Try alternative format: - **[TAG] NAME - TOPIC** → DESCRIPTION (LINK)
            match = re.match(r'- \*\*\[([^\]]+)\]\s+([^\]]+)\s+-\s+([^\]]+)\*\*\s+→\s+(.+?)(?:\s+\(([^)]+)\))?$', line)
        
        if match:
            tag = match.group(1).strip()
            name = match.group(2).strip()
            topic = match.group(3).strip()
            description = match.group(4).strip()
            meeting_link = match.group(5).strip() if len(match.groups()) > 4 and match.group(5) else None
            
            # Normalize tag (remove brackets if present, capitalize first letter)
            tag = tag.strip('[]').strip()
            tag_capitalized = tag.capitalize()
            if tag_capitalized not in VALID_TAGS:
                tag = 'Coaching'  # Default tag
            else:
                tag = tag_capitalized
            
            # Normalize name (case-insensitive matching)
            name_normalized = None
            for dr_name in DIRECT_REPORTS:
                if name.lower() == dr_name.lower():
                    name_normalized = dr_name
                    break
            
            # Only process if it's a known direct report
            if name_normalized:
                if name_normalized not in entries_by_person:
                    entries_by_person[name_normalized] = []
                
                entries_by_person[name_normalized].append({
                    'tag': tag,
                    'topic': topic,
                    'description': description,
                    'meeting_link': meeting_link,
                    'date': week_date
                })
    
    return entries_by_person


def find_or_create_direct_report_page(notion, parent_page_id, person_name):
    """
    Find or create a Notion page for a direct report under the parent page.
    
    Args:
        notion: Notion client object
        parent_page_id: str - Parent page ID
        person_name: str - Name of the direct report (Hannah or Jerica)
    
    Returns:
        str: Page ID of the direct report page
    """
    # List all child pages of the parent
    try:
        children = notion.blocks.children.list(block_id=parent_page_id)
        
        # Look for a page with the person's name
        for child in children.get("results", []):
            if child.get("type") == "child_page":
                page_id = child["id"]
                # Get title from child_page block
                child_page_data = child.get("child_page", {})
                title = child_page_data.get("title", "") if child_page_data else ""
                
                if title and title.lower() == person_name.lower():
                    return page_id
        
        # Page not found, create it
        print(f"   Creating new page for {person_name}...")
        new_page = notion.pages.create(
            parent={"page_id": parent_page_id},
            properties={
                "title": {
                    "title": [{"text": {"content": person_name}}]
                }
            }
        )
        return new_page["id"]
        
    except Exception as e:
        print(f"   Error finding/creating page for {person_name}: {e}")
        raise


def get_existing_page_content(notion, page_id):
    """
    Get existing content from a Notion page and parse it into a structure.
    
    Args:
        notion: Notion client object
        page_id: str - Page ID
    
    Returns:
        dict: {month_key: [list of entry strings]} where month_key is "YYYY-MM"
    """
    entries_by_month = {}
    
    try:
        blocks = notion.blocks.children.list(block_id=page_id)
        current_month = None
        
        for block in blocks.get("results", []):
            block_type = block.get("type")
            
            if block_type == "heading_3":
                # This is a month header
                heading = block.get("heading_3", {}).get("rich_text", [])
                if heading:
                    month_text = heading[0].get("text", {}).get("content", "")
                    # Extract month from text like "January 2026"
                    # Try to parse it
                    try:
                        # Try common formats
                        if " " in month_text:
                            parts = month_text.split()
                            if len(parts) >= 2:
                                month_name = parts[0]
                                year = parts[1]
                                # Convert month name to number
                                month_map = {
                                    "January": "01", "February": "02", "March": "03",
                                    "April": "04", "May": "05", "June": "06",
                                    "July": "07", "August": "08", "September": "09",
                                    "October": "10", "November": "11", "December": "12"
                                }
                                month_num = month_map.get(month_name, "01")
                                current_month = f"{year}-{month_num}"
                    except:
                        pass
                    
                    if current_month and current_month not in entries_by_month:
                        entries_by_month[current_month] = []
            
            elif block_type == "bulleted_list_item" and current_month:
                # This is an entry - store the rich_text array directly
                item = block.get("bulleted_list_item", {}).get("rich_text", [])
                if item:
                    # Store the rich_text array so we can preserve formatting
                    entries_by_month[current_month].append(item)
        
        return entries_by_month
        
    except Exception as e:
        print(f"   Warning: Could not read existing page content: {e}")
        return {}


def format_entry_for_notion(entry, week_date):
    """
    Format an entry dict into a Notion bullet list item block.
    
    Args:
        entry: dict with keys: tag, topic, description, meeting_link, date
        week_date: datetime - Date for the entry
    
    Returns:
        dict: Notion block object
    """
    # Format: **[Tag]** [YYYY-MM-DD] Name - Topic → Description ([Meeting](link))
    date_str = week_date.strftime("%Y-%m-%d")
    
    # Build the text content
    text_parts = []
    
    # Tag in bold
    text_parts.append({
        "type": "text",
        "text": {"content": f"[{entry['tag']}] "},
        "annotations": {"bold": True}
    })
    
    # Date
    text_parts.append({
        "type": "text",
        "text": {"content": f"[{date_str}] "}
    })
    
    # Topic and description
    content = f"{entry['topic']} → {entry['description']}"
    
    # Add meeting link if present
    if entry.get('meeting_link'):
        # Extract link text and URL from markdown link format
        link_match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', entry['meeting_link'])
        if link_match:
            link_text = link_match.group(1)
            link_url = link_match.group(2)
            content += f" ([{link_text}]({link_url}))"
        else:
            content += f" ({entry['meeting_link']})"
    
    # Parse the content for any remaining markdown links
    rich_text = parse_markdown_links(content)
    
    # Combine all text parts
    all_text = text_parts + rich_text
    
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": all_text
        }
    }


def update_direct_report_page(notion, page_id, new_entries, week_date):
    """
    Update a direct report's Notion page with new entries.
    Adds entries at the top, grouped by month/quarter.
    
    Args:
        notion: Notion client object
        page_id: str - Page ID
        new_entries: list - List of entry dicts
        week_date: datetime - Date for the week
    """
    if not new_entries:
        return
    
    # Get existing content
    existing_by_month = get_existing_page_content(notion, page_id)
    
    # Group new entries by month
    new_entries_by_month = {}
    for entry in new_entries:
        month_key = week_date.strftime("%Y-%m")
        if month_key not in new_entries_by_month:
            new_entries_by_month[month_key] = []
        new_entries_by_month[month_key].append(entry)
    
    # Build blocks to add (reverse chronological by month)
    blocks_to_add = []
    
    # Get all months (existing + new), sorted reverse chronologically
    all_months = set(existing_by_month.keys()) | set(new_entries_by_month.keys())
    sorted_months = sorted(all_months, reverse=True)
    
    for month_key in sorted_months:
        # Add month header
        month_date = datetime.strptime(f"{month_key}-01", "%Y-%m-%d")
        month_name = month_date.strftime("%B %Y")
        
        blocks_to_add.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": month_name}}]
            }
        })
        
        # Add new entries for this month (if any)
        if month_key in new_entries_by_month:
            for entry in new_entries_by_month[month_key]:
                blocks_to_add.append(format_entry_for_notion(entry, week_date))
        
        # Add existing entries for this month (if any)
        if month_key in existing_by_month:
            for entry_rich_text in existing_by_month[month_key]:
                # entry_rich_text is already a list of rich_text objects from Notion
                blocks_to_add.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": entry_rich_text
                    }
                })
    
    # Clear existing page content
    try:
        existing_blocks = notion.blocks.children.list(block_id=page_id)
        for block in existing_blocks.get("results", []):
            notion.blocks.delete(block_id=block["id"])
            time.sleep(0.05)  # Rate limiting
    except Exception as e:
        print(f"   Warning: Could not clear old blocks: {e}")
    
    # Add new blocks
    if blocks_to_add:
        # Notion API limit: 100 blocks per request
        for i in range(0, len(blocks_to_add), 100):
            batch = blocks_to_add[i:i+100]
            notion.blocks.children.append(
                block_id=page_id,
                children=batch
            )
            time.sleep(0.1)  # Rate limiting


def update_direct_reports_pages(direct_reports_markdown, week_date, notion_api_key=NOTION_API_KEY, parent_page_id=DIRECT_REPORTS_PARENT_PAGE_ID):
    """
    Main function to parse direct reports notes and update Notion pages.
    
    Args:
        direct_reports_markdown: str - AI-generated markdown with direct report entries
        week_date: datetime - Date for the week
        notion_api_key: str - Notion API key (optional)
        parent_page_id: str - Parent page ID (optional)
    
    Returns:
        dict: {person_name: page_url} for updated pages
    """
    if not notion_api_key:
        raise ValueError("NOTION_API_KEY not set. Please set it in config.py or environment variable.")
    
    # Parse entries
    entries_by_person = parse_direct_reports_entries(direct_reports_markdown, week_date)
    
    if not entries_by_person:
        print("   No direct report entries to update")
        return {}
    
    # Initialize Notion client
    notion = Client(auth=notion_api_key)
    
    updated_pages = {}
    
    # Update each person's page
    for person_name, entries in entries_by_person.items():
        print(f"   Updating page for {person_name} ({len(entries)} entries)...")
        
        try:
            # Find or create page
            page_id = find_or_create_direct_report_page(notion, parent_page_id, person_name)
            
            # Update page with new entries
            update_direct_report_page(notion, page_id, entries, week_date)
            
            page_url = f"https://www.notion.so/{page_id.replace('-', '')}"
            updated_pages[person_name] = page_url
            print(f"   ✅ Updated {person_name}'s page")
            
        except Exception as e:
            print(f"   ❌ Error updating {person_name}'s page: {e}")
            import traceback
            traceback.print_exc()
    
    return updated_pages
