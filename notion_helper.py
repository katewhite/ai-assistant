"""
Notion API helper for uploading weekly summaries.
Uses the notion-client package to create/update pages in Notion database.
"""

from notion_client import Client
from datetime import datetime
import time
from config import NOTION_API_KEY, NOTION_DATABASE_ID


def markdown_to_notion_blocks(markdown_text):
    """
    Convert markdown text to Notion blocks.
    Handles headers, bullet lists, and paragraphs.

    Args:
        markdown_text: str - Markdown formatted text

    Returns:
        list: List of Notion block objects
    """
    blocks = []
    lines = markdown_text.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            # Skip empty lines
            i += 1
            continue

        # Headers (###, ##, #)
        if line.startswith('###'):
            header_text = line[3:].strip()
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": header_text}}]
                }
            })
            i += 1

        elif line.startswith('##'):
            header_text = line[2:].strip()
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": header_text}}]
                }
            })
            i += 1

        elif line.startswith('#'):
            header_text = line[1:].strip()
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": header_text}}]
                }
            })
            i += 1

        # Bullet points
        elif line.startswith('- '):
            bullet_text = line[2:].strip()
            rich_text = parse_markdown_links(bullet_text)

            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": rich_text
                }
            })
            i += 1

        # Regular paragraph
        else:
            rich_text = parse_markdown_links(line)

            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": rich_text
                }
            })
            i += 1

    return blocks


def parse_markdown_links(text):
    """
    Parse markdown links in text and convert to Notion rich text format.

    Handles formats like:
    - [link text](https://url)
    - **bold text**

    Args:
        text: str - Text with markdown formatting

    Returns:
        list: List of Notion rich_text objects
    """
    import re

    rich_text = []
    pos = 0

    # Pattern for markdown links: [text](url)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    for match in re.finditer(link_pattern, text):
        # Add text before the link
        if match.start() > pos:
            before_text = text[pos:match.start()]
            if before_text:
                rich_text.extend(parse_bold(before_text))

        # Add the link
        link_text = match.group(1)
        link_url = match.group(2)

        rich_text.append({
            "type": "text",
            "text": {
                "content": link_text,
                "link": {"url": link_url}
            }
        })

        pos = match.end()

    # Add remaining text after last link
    if pos < len(text):
        remaining = text[pos:]
        if remaining:
            rich_text.extend(parse_bold(remaining))

    # If no links found, parse the whole text
    if not rich_text:
        rich_text = parse_bold(text)

    return rich_text


def parse_bold(text):
    """
    Parse bold markdown (**text**) and convert to Notion rich text.

    Args:
        text: str - Text with possible bold markdown

    Returns:
        list: List of Notion rich_text objects
    """
    import re

    rich_text = []
    pos = 0

    # Pattern for bold: **text**
    bold_pattern = r'\*\*([^*]+)\*\*'

    for match in re.finditer(bold_pattern, text):
        # Add text before the bold
        if match.start() > pos:
            before_text = text[pos:match.start()]
            if before_text:
                rich_text.append({
                    "type": "text",
                    "text": {"content": before_text}
                })

        # Add the bold text
        bold_text = match.group(1)
        rich_text.append({
            "type": "text",
            "text": {"content": bold_text},
            "annotations": {"bold": True}
        })

        pos = match.end()

    # Add remaining text after last bold
    if pos < len(text):
        remaining = text[pos:]
        if remaining:
            rich_text.append({
                "type": "text",
                "text": {"content": remaining}
            })

    # If no bold found, return plain text
    if not rich_text:
        rich_text = [{"type": "text", "text": {"content": text}}]

    return rich_text


def get_existing_features(notion, database_id):
    """
    Get existing Features multi-select options from the database.

    Args:
        notion: Notion client object
        database_id: str - Notion database ID

    Returns:
        list: List of existing feature option names
    """
    try:
        database = notion.databases.retrieve(database_id=database_id)
        properties = database.get("properties", {})
        features_property = properties.get("Features", {})

        if features_property.get("type") == "multi_select":
            options = features_property.get("multi_select", {}).get("options", [])
            return [option["name"] for option in options]

        return []
    except Exception as e:
        print(f"Warning: Could not retrieve existing features: {e}")
        return []


def find_existing_page_for_week(notion, database_id, week_start_date):
    """
    Check if a page already exists for this week in the Notion database.

    Args:
        notion: Notion client object
        database_id: str - Notion database ID
        week_start_date: datetime - The Friday that starts this week

    Returns:
        str or None: Page ID if found, None otherwise
    """
    try:
        # Format date as ISO string for Notion query
        date_str = week_start_date.strftime("%Y-%m-%d")

        # Query the database for pages with this reflection date
        response = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "Reflection Date",
                "date": {
                    "equals": date_str
                }
            }
        )

        results = response.get("results", [])

        if results:
            return results[0]["id"]

        return None

    except Exception as e:
        print(f"Warning: Error checking for existing page: {e}")
        return None


def upload_to_notion(summary_markdown, week_label, week_start_date, reflection_date=None, customer_call_count=0, notes_summary="", features=None, notion_api_key=NOTION_API_KEY, database_id=NOTION_DATABASE_ID):
    """
    Upload weekly summary to Notion database.
    Creates a new page or updates existing page if one already exists for this week.

    Args:
        summary_markdown: str - The markdown formatted summary
        week_label: str - e.g., "Week of Nov 28 - Dec 5"
        week_start_date: datetime - The Friday that starts this week (used for finding existing pages)
        reflection_date: datetime - The date the summary was created (optional, defaults to today)
        customer_call_count: int - Number of customer calls this week
        notes_summary: str - 2-3 sentence high-level summary of the week
        features: list - List of feature names to tag (only existing options will be used)
        notion_api_key: str - Notion API key (optional, uses config if not provided)
        database_id: str - Notion database ID (optional, uses config if not provided)

    Returns:
        str: URL of the created/updated Notion page

    Raises:
        ValueError: If API key is not set
        Exception: If Notion API call fails
    """
    if reflection_date is None:
        reflection_date = datetime.now()
    if features is None:
        features = []
    if not notion_api_key:
        raise ValueError("NOTION_API_KEY not set. Please set it in config.py or environment variable.")

    # Initialize Notion client
    notion = Client(auth=notion_api_key)

    # Convert markdown to Notion blocks
    blocks = markdown_to_notion_blocks(summary_markdown)

    # Get existing features from database and filter provided features
    existing_features = get_existing_features(notion, database_id)
    valid_features = [f for f in features if f in existing_features]

    if len(valid_features) < len(features):
        excluded = [f for f in features if f not in existing_features]
        print(f"Note: Excluded non-existent features: {excluded}")

    # Check if page already exists for this week
    existing_page_id = find_existing_page_for_week(notion, database_id, week_start_date)

    try:
        if existing_page_id:
            # Update existing page
            print(f"Updating existing page: {existing_page_id}")

            # Update page properties (title, reflection date, customer calls, notes)
            reflection_date_str = reflection_date.strftime("%Y-%m-%d")

            properties = {
                "Name": {
                    "title": [{"text": {"content": week_label}}]
                },
                "Reflection Date": {
                    "date": {"start": reflection_date_str}
                }
            }

            # Add customer call count if provided
            if customer_call_count > 0:
                properties["Customer Calls"] = {"number": customer_call_count}

            # Add notes summary if provided
            if notes_summary:
                properties["Notes"] = {"rich_text": [{"text": {"content": notes_summary}}]}

            # Add features if provided
            if valid_features:
                properties["Features"] = {
                    "multi_select": [{"name": feature} for feature in valid_features]
                }

            notion.pages.update(page_id=existing_page_id, properties=properties)

            # Delete all existing blocks first
            print("Clearing old content...")
            try:
                existing_blocks = notion.blocks.children.list(block_id=existing_page_id)
                for block in existing_blocks.get("results", []):
                    notion.blocks.delete(block_id=block["id"])
                    time.sleep(0.05)  # Rate limiting
            except Exception as e:
                print(f"Warning: Could not clear old blocks: {e}")

            # Add new blocks
            print("Adding new content...")
            for block in blocks:
                notion.blocks.children.append(
                    block_id=existing_page_id,
                    children=[block]
                )
                time.sleep(0.1)  # Rate limiting

            page_url = f"https://www.notion.so/{existing_page_id.replace('-', '')}"
            print(f"✅ Updated Notion page: {page_url}")
            return page_url

        else:
            # Create new page
            print(f"Creating new page: {week_label}")

            # Format reflection date for Notion
            reflection_date_str = reflection_date.strftime("%Y-%m-%d")

            properties = {
                "Name": {
                    "title": [{"text": {"content": week_label}}]
                },
                "Reflection Date": {
                    "date": {"start": reflection_date_str}
                }
            }

            # Add customer call count if provided
            if customer_call_count > 0:
                properties["Customer Calls"] = {"number": customer_call_count}

            # Add notes summary if provided
            if notes_summary:
                properties["Notes"] = {"rich_text": [{"text": {"content": notes_summary}}]}

            # Add features if provided
            if valid_features:
                properties["Features"] = {
                    "multi_select": [{"name": feature} for feature in valid_features]
                }

            new_page = notion.pages.create(
                parent={"database_id": database_id},
                properties=properties,
                children=blocks[:100]  # Notion API limit: 100 blocks per request
            )

            # If more than 100 blocks, add them in batches
            if len(blocks) > 100:
                page_id = new_page["id"]
                remaining_blocks = blocks[100:]

                for i in range(0, len(remaining_blocks), 100):
                    batch = remaining_blocks[i:i+100]
                    notion.blocks.children.append(
                        block_id=page_id,
                        children=batch
                    )
                    time.sleep(0.3)  # Rate limiting

            page_url = new_page["url"]
            print(f"✅ Created Notion page: {page_url}")
            return page_url

    except Exception as e:
        print(f"❌ Error uploading to Notion: {e}")
        raise


if __name__ == "__main__":
    # Test markdown conversion
    test_markdown = """### Test Header

This is a test paragraph with **bold text**.

- First bullet with [a link](https://example.com)
- Second bullet
- **Name** → description with ([source](https://notes.granola.ai/d/test-id))
"""

    print("Testing markdown to Notion blocks conversion...")
    blocks = markdown_to_notion_blocks(test_markdown)
    print(f"Generated {len(blocks)} blocks")

    for i, block in enumerate(blocks, 1):
        print(f"{i}. {block['type']}")
