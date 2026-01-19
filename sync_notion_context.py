#!/usr/bin/env python3
"""
Sync context files from Notion database to .claude/context/core/
"""

import re
from pathlib import Path
from datetime import datetime, timezone
from notion_reader import (
    get_notion_pages_modified_since,
    get_last_sync_time,
    update_last_sync_time
)
from config import NOTION_API_KEY, NOTION_CONTEXT_DATABASE_ID

# Paths
PROJECT_ROOT = Path(__file__).parent
CORE_DIR = PROJECT_ROOT / ".claude" / "context" / "core"
SYNC_STATE_FILE = PROJECT_ROOT / ".notion_sync_state.json"


def slugify(text):
    """Convert text to a URL-safe filename."""
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Remove all non-alphanumeric characters except hyphens and dots
    text = re.sub(r'[^a-z0-9\-.]', '', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Remove leading/trailing hyphens and dots
    text = text.strip('-.')
    # Limit length
    if len(text) > 100:
        text = text[:100]
    return text


def generate_filename(title, filename_hint=None):
    """Generate a safe filename from title or use provided filename."""
    if filename_hint and filename_hint.strip():
        # Use provided filename, but ensure it's safe
        filename = filename_hint.strip()
        # Remove path components for safety
        filename = Path(filename).name
        # Ensure it ends with .md
        if not filename.endswith('.md'):
            filename = f"{filename}.md"
        return filename
    
    # Generate from title
    title_slug = slugify(title)
    if not title_slug:
        title_slug = "untitled"
    
    return f"{title_slug}.md"


def file_exists_for_page(page_id, core_dir):
    """Check if a file already exists for this Notion page ID."""
    for file in core_dir.iterdir():
        if file.is_file() and file.suffix == ".md":
            # Read frontmatter to check notion_id
            try:
                content = file.read_text(encoding='utf-8')
                if content.startswith('---'):
                    # Extract frontmatter
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        if f'notion_id: "{page_id}"' in frontmatter or f"notion_id: '{page_id}'" in frontmatter:
                            return file
            except Exception:
                continue
    return None


def create_context_file(page, core_dir):
    """Create or update a markdown file for a Notion page."""
    page_id = page["id"]
    title = page["title"]
    filename_hint = page.get("filename")
    original_url = page.get("original_url")
    last_modified = page["last_modified"]
    url = page["url"]
    content = page.get("content", "")
    
    # Check if file already exists for this page
    existing_file = file_exists_for_page(page_id, core_dir)
    
    # Generate filename
    filename = generate_filename(title, filename_hint)
    filepath = core_dir / filename
    
    # If filename conflicts with a different page, add page_id suffix
    if filepath.exists() and (not existing_file or existing_file != filepath):
        name_part = filepath.stem
        filepath = core_dir / f"{name_part}-{page_id[:8]}.md"
    
    # Format last modified date
    if last_modified.tzinfo:
        last_modified_str = last_modified.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    else:
        last_modified_str = last_modified.strftime("%Y-%m-%d %H:%M:%S")
    
    # Build markdown content
    lines = [
        "---",
        f'title: "{title.replace('"', '\\"')}"',
        f"last_modified: {last_modified_str}",
        f'notion_url: "{url}"',
        f'notion_id: "{page_id}"',
    ]
    
    if filename_hint:
        lines.append(f'filename: "{filename_hint.replace('"', '\\"')}"')
    
    if original_url:
        lines.append(f'original_url: "{original_url.replace('"', '\\"')}"')
    
    lines.extend([
        "---",
        "",
    ]
    )
    
    # Add visible metadata section with clickable links
    # Format as regular markdown content right after frontmatter
    if original_url:
        lines.append(f"**Original URL:** [{original_url}]({original_url})")
        lines.append("")
    lines.append(f"**My Notion URL:** [{url}]({url})")
    lines.append("")
    lines.append(f"**Last Modified:** {last_modified_str}")
    lines.append("")
    lines.append("<hr>")
    lines.append("")
    
    # Add content
    if content:
        lines.append(content)
        lines.append("")
    
    # Write file
    file_content = "\n".join(lines)
    filepath.write_text(file_content, encoding='utf-8')
    
    if existing_file and existing_file == filepath:
        return filepath, "updated"
    else:
        return filepath, "synced"


def main():
    """Main sync function."""
    # Check if database ID is configured
    if not NOTION_CONTEXT_DATABASE_ID:
        print("❌ NOTION_CONTEXT_DATABASE_ID not set in config.py")
        print("   Please set it to your Notion database ID for context files")
        return 1
    
    # Ensure core directory exists
    CORE_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Syncing context files from Notion database")
    print(f"📁 Target directory: {CORE_DIR}")
    print()
    
    # Get last sync time
    last_sync = get_last_sync_time(SYNC_STATE_FILE)
    if last_sync:
        print(f"📅 Last sync: {last_sync.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Fetching pages modified since then...")
    else:
        print(f"📅 No previous sync found - fetching all pages...")
        # Use a date far in the past to get all pages
        last_sync = datetime(2000, 1, 1, tzinfo=timezone.utc)
    
    print()
    
    # Get pages modified since last sync
    try:
        pages = get_notion_pages_modified_since(
            NOTION_CONTEXT_DATABASE_ID,
            last_sync,
            NOTION_API_KEY
        )
    except Exception as e:
        print(f"❌ Error loading pages from Notion: {e}")
        return 1
    
    if not pages:
        print(f"ℹ️  No pages found modified since last sync")
        return 0
    
    print(f"Found {len(pages)} page(s) to sync")
    print()
    
    # Sync each page
    synced = []
    updated = []
    errors = []
    
    for page in pages:
        try:
            filepath, status = create_context_file(page, CORE_DIR)
            if status == "synced":
                synced.append((page["title"], filepath))
            elif status == "updated":
                updated.append((page["title"], filepath))
        except Exception as e:
            errors.append((page["title"], str(e)))
    
    # Update last sync time
    sync_time = datetime.now(timezone.utc)
    update_last_sync_time(SYNC_STATE_FILE, sync_time)
    
    # Report results
    print("=" * 60)
    print("Sync Results")
    print("=" * 60)
    
    if synced:
        print(f"\n✅ Synced {len(synced)} file(s):")
        for title, filepath in synced:
            print(f"   • {title}")
            print(f"     → {filepath.name}")
    
    if updated:
        print(f"\n🔄 Updated {len(updated)} file(s):")
        for title, filepath in updated:
            print(f"   • {title}")
            print(f"     → {filepath.name}")
    
    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for title, error in errors:
            print(f"   • {title}: {error}")
    
    print()
    total = len(pages)
    print(f"Total: {total} | Synced: {len(synced)} | Updated: {len(updated)} | Errors: {len(errors)}")
    print(f"Last sync time updated to: {sync_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    return 0 if not errors else 1


if __name__ == "__main__":
    exit(main())
