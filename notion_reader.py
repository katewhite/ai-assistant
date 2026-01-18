"""
Notion API helper for reading context files from Notion database.
Converts Notion blocks to markdown format.
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from dateutil.parser import parse as parse_date
from notion_client import Client
from config import NOTION_API_KEY, NOTION_CONTEXT_DATABASE_ID


def rich_text_to_markdown(rich_text_array):
    """
    Convert Notion rich_text array to markdown string.
    
    Args:
        rich_text_array: List of rich_text objects from Notion
        
    Returns:
        str: Markdown formatted text
    """
    if not rich_text_array:
        return ""
    
    result = []
    for item in rich_text_array:
        if item.get("type") == "text":
            text = item.get("text", {}).get("content", "")
            annotations = item.get("annotations", {})
            
            # Apply formatting
            if annotations.get("bold"):
                text = f"**{text}**"
            if annotations.get("italic"):
                text = f"*{text}*"
            if annotations.get("code"):
                text = f"`{text}`"
            
            # Handle links
            link = item.get("text", {}).get("link")
            if link:
                url = link.get("url", "")
                text = f"[{text}]({url})"
            
            result.append(text)
        elif item.get("type") == "mention":
            # Handle mentions (users, pages, etc.)
            mention = item.get("mention", {})
            if mention.get("type") == "page":
                page_id = mention.get("page", {}).get("id", "")
                result.append(f"[Page](https://www.notion.so/{page_id.replace('-', '')})")
            else:
                result.append(item.get("plain_text", ""))
        else:
            # Fallback to plain_text
            result.append(item.get("plain_text", ""))
    
    return "".join(result)


def notion_blocks_to_markdown(blocks):
    """
    Convert Notion blocks to markdown format.
    
    Args:
        blocks: List of Notion block objects
        
    Returns:
        str: Markdown formatted text
    """
    if not blocks:
        return ""
    
    markdown_lines = []
    
    for block in blocks:
        block_type = block.get("type", "")
        
        if block_type == "heading_1":
            rich_text = block.get("heading_1", {}).get("rich_text", [])
            text = rich_text_to_markdown(rich_text)
            if text:
                markdown_lines.append(f"# {text}")
        
        elif block_type == "heading_2":
            rich_text = block.get("heading_2", {}).get("rich_text", [])
            text = rich_text_to_markdown(rich_text)
            if text:
                markdown_lines.append(f"## {text}")
        
        elif block_type == "heading_3":
            rich_text = block.get("heading_3", {}).get("rich_text", [])
            text = rich_text_to_markdown(rich_text)
            if text:
                markdown_lines.append(f"### {text}")
        
        elif block_type == "paragraph":
            rich_text = block.get("paragraph", {}).get("rich_text", [])
            text = rich_text_to_markdown(rich_text)
            if text:
                markdown_lines.append(text)
            else:
                # Empty paragraph - add blank line
                markdown_lines.append("")
        
        elif block_type == "bulleted_list_item":
            rich_text = block.get("bulleted_list_item", {}).get("rich_text", [])
            text = rich_text_to_markdown(rich_text)
            if text:
                markdown_lines.append(f"- {text}")
        
        elif block_type == "numbered_list_item":
            rich_text = block.get("numbered_list_item", {}).get("rich_text", [])
            text = rich_text_to_markdown(rich_text)
            if text:
                markdown_lines.append(f"1. {text}")
        
        elif block_type == "code":
            code_obj = block.get("code", {})
            language = code_obj.get("language", "")
            rich_text = code_obj.get("rich_text", [])
            text = rich_text_to_markdown(rich_text)
            if text:
                markdown_lines.append(f"```{language}")
                markdown_lines.append(text)
                markdown_lines.append("```")
        
        elif block_type == "quote":
            rich_text = block.get("quote", {}).get("rich_text", [])
            text = rich_text_to_markdown(rich_text)
            if text:
                # Quote each line
                for line in text.split("\n"):
                    markdown_lines.append(f"> {line}")
        
        elif block_type == "divider":
            markdown_lines.append("---")
        
        elif block_type == "to_do":
            to_do_obj = block.get("to_do", {})
            checked = to_do_obj.get("checked", False)
            rich_text = to_do_obj.get("rich_text", [])
            text = rich_text_to_markdown(rich_text)
            if text:
                checkbox = "- [x]" if checked else "- [ ]"
                markdown_lines.append(f"{checkbox} {text}")
        
        elif block_type == "toggle":
            rich_text = block.get("toggle", {}).get("rich_text", [])
            text = rich_text_to_markdown(rich_text)
            if text:
                markdown_lines.append(f"<details><summary>{text}</summary>")
                # Note: Toggle children would need to be handled separately
                markdown_lines.append("</details>")
        
        # Add blank line after block for readability
        if block_type in ["heading_1", "heading_2", "heading_3", "paragraph", "quote", "divider"]:
            markdown_lines.append("")
    
    return "\n".join(markdown_lines).strip()


def get_page_content(notion, page_id):
    """
    Retrieve all blocks from a Notion page and convert to markdown.
    
    Args:
        notion: Notion client object
        page_id: Notion page ID
        
    Returns:
        str: Markdown content of the page
    """
    all_blocks = []
    cursor = None
    
    while True:
        if cursor:
            response = notion.blocks.children.list(block_id=page_id, start_cursor=cursor)
        else:
            response = notion.blocks.children.list(block_id=page_id)
        
        blocks = response.get("results", [])
        all_blocks.extend(blocks)
        
        has_more = response.get("has_more", False)
        if not has_more:
            break
        
        cursor = response.get("next_cursor")
    
    return notion_blocks_to_markdown(all_blocks)


def get_last_sync_time(sync_state_file):
    """
    Read last sync timestamp from state file.
    
    Args:
        sync_state_file: Path to JSON state file
        
    Returns:
        datetime or None: Last sync time, or None if file doesn't exist
    """
    if not sync_state_file.exists():
        return None
    
    try:
        with open(sync_state_file, "r") as f:
            data = json.load(f)
            last_sync_str = data.get("last_sync")
            if last_sync_str:
                return parse_date(last_sync_str)
    except Exception as e:
        print(f"Warning: Could not read sync state: {e}")
    
    return None


def update_last_sync_time(sync_state_file, sync_time):
    """
    Write last sync timestamp to state file.
    
    Args:
        sync_state_file: Path to JSON state file
        sync_time: datetime object
    """
    sync_state_file.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "last_sync": sync_time.isoformat()
    }
    
    with open(sync_state_file, "w") as f:
        json.dump(data, f, indent=2)


def get_notion_pages_modified_since(database_id, since_date, notion_api_key=None):
    """
    Query Notion database for pages modified since a given date.
    
    Args:
        database_id: Notion database ID
        since_date: datetime object - only get pages modified after this date
        notion_api_key: Notion API key (optional, uses config if not provided)
        
    Returns:
        list: List of page dicts with keys: id, title, filename, last_modified, url, content
    """
    if not notion_api_key:
        notion_api_key = NOTION_API_KEY
    
    if not notion_api_key:
        raise ValueError("NOTION_API_KEY not set")
    
    notion = Client(auth=notion_api_key)
    
    # Convert since_date to ISO format for Notion query
    since_date_str = since_date.isoformat()
    
    # Query database for pages modified since the date
    pages = []
    cursor = None
    
    while True:
        # Use timestamp sort instead of property sort to avoid requiring custom "Last Modified" property
        query_params = {
            "database_id": database_id,
            "sorts": [
                {
                    "timestamp": "last_edited_time",
                    "direction": "descending"
                }
            ]
        }

        if cursor:
            query_params["start_cursor"] = cursor

        # Query without filter - we'll filter by date in Python instead
        # This avoids requiring a custom "Last Modified" property
        response = notion.databases.query(**query_params)
        
        results = response.get("results", [])

        for page in results:
            try:
                # Get last modified time first to filter by date
                last_edited_time = page.get("last_edited_time", "")
                if last_edited_time:
                    last_modified = parse_date(last_edited_time)
                    # Skip pages that haven't been modified since since_date
                    if last_modified < since_date:
                        continue
                else:
                    last_modified = datetime.now(timezone.utc)

                # Extract page properties
                properties = page.get("properties", {})
                
                # Get title (try both "Title" and "Name" properties)
                title_prop = properties.get("Title", {}) or properties.get("Name", {})
                if title_prop.get("type") == "title":
                    title_rich_text = title_prop.get("title", [])
                    title = "".join([rt.get("plain_text", "") for rt in title_rich_text]).strip()
                else:
                    title = "Untitled"

                # Skip if title is empty
                if not title:
                    title = "Untitled"
                
                # Get filename (optional)
                filename_prop = properties.get("Filename", {})
                filename = None
                if filename_prop:
                    if filename_prop.get("type") == "rich_text":
                        filename_rich_text = filename_prop.get("rich_text", [])
                        filename = "".join([rt.get("plain_text", "") for rt in filename_rich_text]).strip()
                    elif filename_prop.get("type") == "title":
                        filename_rich_text = filename_prop.get("title", [])
                        filename = "".join([rt.get("plain_text", "") for rt in filename_rich_text]).strip()
                
                # Get page ID and URL
                page_id = page.get("id", "")
                page_url = page.get("url", "")
                
                # Get page content
                content = get_page_content(notion, page_id)
                
                pages.append({
                    "id": page_id,
                    "title": title,
                    "filename": filename,
                    "last_modified": last_modified,
                    "url": page_url,
                    "content": content
                })
                
            except Exception as e:
                print(f"Warning: Failed to process page {page.get('id', 'unknown')}: {e}")
                continue
        
        has_more = response.get("has_more", False)
        if not has_more:
            break
        
        cursor = response.get("next_cursor")
    
    return pages
