#!/usr/bin/env python3
"""
Sync call transcripts from Granola "Claude Context" folder to .claude/context/calls/
"""

import re
from pathlib import Path
from datetime import datetime
from granola_reader import get_documents_in_folder

# Paths
PROJECT_ROOT = Path(__file__).parent
CALLS_DIR = PROJECT_ROOT / ".claude" / "context" / "calls"
GRANOLA_FOLDER_NAME = "Claude Context"


def slugify(text):
    """Convert text to a URL-safe filename."""
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Remove all non-alphanumeric characters except hyphens
    text = re.sub(r'[^a-z0-9\-]', '', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    # Limit length
    if len(text) > 100:
        text = text[:100]
    return text


def generate_filename(title, date_str, doc_id):
    """Generate a safe filename from title and date."""
    # Extract date part (YYYY-MM-DD)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', date_str)
    if date_match:
        date_part = date_match.group(1)
    else:
        # Fallback to current date if parsing fails
        date_part = datetime.now().strftime("%Y-%m-%d")
    
    # Slugify the title
    title_slug = slugify(title)
    if not title_slug:
        title_slug = "untitled"
    
    # Use doc_id as fallback for uniqueness
    doc_id_short = doc_id[:8] if doc_id else "unknown"
    
    filename = f"{date_part}-{title_slug}.md"
    
    # If filename is too long, truncate title part
    if len(filename) > 200:
        max_title_len = 200 - len(date_part) - len(doc_id_short) - 3  # -3 for dashes and .md
        title_slug = title_slug[:max_title_len]
        filename = f"{date_part}-{title_slug}-{doc_id_short}.md"
    
    return filename


def file_exists_for_doc(doc_id, calls_dir):
    """Check if a file already exists for this document ID."""
    for file in calls_dir.iterdir():
        if file.is_file() and file.suffix == ".md":
            # Read frontmatter to check doc_id
            try:
                content = file.read_text(encoding='utf-8')
                if content.startswith('---'):
                    # Extract frontmatter
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        if f'granola_id: "{doc_id}"' in frontmatter or f"granola_id: '{doc_id}'" in frontmatter:
                            return True
            except Exception:
                continue
    return False


def create_call_file(doc, calls_dir):
    """Create a markdown file for a call document."""
    doc_id = doc["id"]
    title = doc["title"]
    date_str = doc["date"]
    url = doc["url"]
    transcript = doc.get("transcript", "")
    notes = doc.get("notes", "")
    
    # Check if file already exists
    if file_exists_for_doc(doc_id, calls_dir):
        return None, "skipped (already exists)"
    
    # Generate filename
    filename = generate_filename(title, date_str, doc_id)
    filepath = calls_dir / filename
    
    # If filename conflicts, add doc_id suffix
    if filepath.exists():
        name_part = filepath.stem
        filepath = calls_dir / f"{name_part}-{doc_id[:8]}.md"
    
    # Build markdown content
    lines = [
        "---",
        f'title: "{title.replace('"', '\\"')}"',
        f"date: {date_str}",
        f'granola_url: "{url}"',
        f'granola_id: "{doc_id}"',
        "---",
        "",
    ]
    
    # Add transcript
    if transcript:
        lines.append("## Transcript")
        lines.append("")
        lines.append(transcript)
        lines.append("")
    
    # Add notes if available
    if notes:
        if transcript:
            lines.append("---")
            lines.append("")
        lines.append("## Notes")
        lines.append("")
        lines.append(notes)
        lines.append("")
    
    # Write file
    content = "\n".join(lines)
    filepath.write_text(content, encoding='utf-8')
    
    return filepath, "synced"


def main():
    """Main sync function."""
    # Ensure calls directory exists
    CALLS_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Syncing calls from Granola folder: '{GRANOLA_FOLDER_NAME}'")
    print(f"📁 Target directory: {CALLS_DIR}")
    print()
    
    # Get documents from folder
    try:
        documents = get_documents_in_folder(GRANOLA_FOLDER_NAME)
    except Exception as e:
        print(f"❌ Error loading documents from Granola: {e}")
        return 1
    
    if not documents:
        print(f"ℹ️  No documents found in folder '{GRANOLA_FOLDER_NAME}'")
        return 0
    
    print(f"Found {len(documents)} document(s) in folder")
    print()
    
    # Sync each document
    synced = []
    skipped = []
    errors = []
    
    for doc in documents:
        try:
            filepath, status = create_call_file(doc, CALLS_DIR)
            if status == "synced":
                synced.append((doc["title"], filepath))
            elif status.startswith("skipped"):
                skipped.append(doc["title"])
        except Exception as e:
            errors.append((doc["title"], str(e)))
    
    # Report results
    print("=" * 60)
    print("Sync Results")
    print("=" * 60)
    
    if synced:
        print(f"\n✅ Synced {len(synced)} call(s):")
        for title, filepath in synced:
            print(f"   • {title}")
            print(f"     → {filepath.name}")
    
    if skipped:
        print(f"\n⏭️  Skipped {len(skipped)} call(s) (already exist):")
        for title in skipped:
            print(f"   • {title}")
    
    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for title, error in errors:
            print(f"   • {title}: {error}")
    
    print()
    print(f"Total: {len(documents)} | Synced: {len(synced)} | Skipped: {len(skipped)} | Errors: {len(errors)}")
    
    return 0 if not errors else 1


if __name__ == "__main__":
    exit(main())
