"""
Simplified Granola cache reader for extracting personal meeting notes.
Based on the existing MCP server logic but standalone.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse as parse_date
from config import GRANOLA_CACHE_PATH, MY_USER_ID, GRANOLA_NOTE_BASE_URL


def load_granola_cache():
    """Load and parse the Granola cache-v3.json file."""
    if not GRANOLA_CACHE_PATH.exists():
        raise FileNotFoundError(f"Granola cache not found at: {GRANOLA_CACHE_PATH}")

    with open(GRANOLA_CACHE_PATH, "r") as f:
        top = json.load(f)

        # Double-decode the embedded JSON string if necessary
        if isinstance(top.get("cache"), str):
            top["cache"] = json.loads(top["cache"])

        return top


def get_granola_url(doc_id):
    """Generate Granola note URL from document ID."""
    return f"{GRANOLA_NOTE_BASE_URL}{doc_id}"


def is_personal_meeting(doc, state, my_user_id=MY_USER_ID, debug=False):
    """
    Determine if this is a meeting the user actually participated in.
    More restrictive: only include meetings where the user was present.
    """
    if not isinstance(doc, dict):
        return False

    title = doc.get("title", "Untitled")

    # Strategy 1: Check user_id field (if it exists, user must match)
    user_id = doc.get("user_id")
    if user_id and str(user_id) != my_user_id:
        if debug:
            print(f"  ❌ Excluded by Strategy 1 (user_id mismatch): {user_id} != {my_user_id}")
        return False

    # Strategy 2: Check visibility and public flags
    visibility = doc.get("visibility")
    is_public = doc.get("public", False)
    if is_public or visibility == "public":
        if debug:
            print(f"  ❌ Excluded by Strategy 2 (public/visible): is_public={is_public}, visibility={visibility}")
        return False

    # Strategy 3: Check attendee count (people.attendees is a list)
    # If too many attendees, likely a team meeting
    people = doc.get("people", {})
    if isinstance(people, dict):
        attendees = people.get("attendees", [])
        if isinstance(attendees, list):
            # Count real attendees (not groups)
            real_attendees = [a for a in attendees if isinstance(a, dict) and not a.get("details", {}).get("group")]
            if len(real_attendees) > 4:
                if debug:
                    print(f"  ❌ Excluded by Strategy 3 (too many attendees): {len(real_attendees)} attendees")
                return False

    # Strategy 4: Check title patterns for team meetings
    title_lower = title.lower()
    team_patterns = [
        'cycle planning', 'daily standup', 'standup', 'sprint', 'retrospective', 'planning',
        'all hands', 'team meeting', 'scrum', 'demo', 'review meeting'
    ]
    for pattern in team_patterns:
        if pattern in title_lower:
            if debug:
                print(f"  ❌ Excluded by Strategy 4 (team meeting pattern): matched '{pattern}'")
            return False

    # Strategy 5: Check for client/external meeting patterns
    client_patterns = [
        'intelligems &', '& intelligems', '<>', 'shopify split testing',
        'demo call', 'intro call', 'discovery call'
    ]
    for pattern in client_patterns:
        if pattern in title_lower:
            if debug:
                print(f"  ❌ Excluded by Strategy 5 (client meeting pattern): matched '{pattern}'")
            return False

    # Strategy 6: Look for personal meeting patterns (strong signals to include)
    personal_patterns = [
        '1:1', 'one-on-one', 'career', 'feedback',
        'check-in', 'catch up', 'sync', '/ kate', 'kate /', '/ helen', 'helen /'
    ]
    for pattern in personal_patterns:
        if pattern in title_lower:
            if debug:
                print(f"  ✅ Included by Strategy 6 (personal meeting pattern): matched '{pattern}'")
            return True

    # Strategy 7: If no user_id, be restrictive
    if not user_id:
        if debug:
            print(f"  ❌ Excluded by Strategy 7 (no user_id)")
        return False

    # Default: include if we've passed all filters (has user_id, not workspace, not too many attendees, not team meeting pattern)
    if debug:
        print(f"  ✅ Included by default (passed all exclusion filters)")
    return True


def extract_text_from_panel_content(content_dict):
    """Extract plain text from Granola's panel content structure."""
    if not isinstance(content_dict, dict):
        return ""

    text_parts = []

    def extract_recursive(obj):
        if isinstance(obj, dict):
            if 'text' in obj:
                text_parts.append(str(obj['text']))

            if 'content' in obj and isinstance(obj['content'], list):
                for item in obj['content']:
                    extract_recursive(item)
        elif isinstance(obj, list):
            for item in obj:
                extract_recursive(item)

    extract_recursive(content_dict)
    result = ' '.join(text_parts).strip()

    # Clean up extra whitespace
    import re
    result = re.sub(r'\s+', ' ', result)

    return result


def extract_markdown_from_content(content_dict):
    """Extract markdown-formatted text from Granola's content structure, preserving formatting."""
    if not isinstance(content_dict, dict):
        return ""
    
    # If content is already a markdown string, return it
    if isinstance(content_dict, str):
        return content_dict
    
    markdown_parts = []
    
    def extract_recursive(obj, indent_level=0):
        if isinstance(obj, dict):
            # Check for markdown field first
            if 'markdown' in obj:
                markdown_parts.append(str(obj['markdown']))
                return
            
            # Check for text with formatting
            if 'text' in obj:
                text = str(obj['text'])
                # Check for formatting hints
                if obj.get('bold'):
                    text = f"**{text}**"
                if obj.get('italic'):
                    text = f"*{text}*"
                if obj.get('code'):
                    text = f"`{text}`"
                markdown_parts.append(text)
            
            # Handle content list (preserve structure)
            if 'content' in obj and isinstance(obj['content'], list):
                for item in obj['content']:
                    extract_recursive(item, indent_level)
            # Handle blocks/children structure
            elif 'blocks' in obj and isinstance(obj['blocks'], list):
                for block in obj['blocks']:
                    extract_recursive(block, indent_level)
            elif 'children' in obj and isinstance(obj['children'], list):
                for child in obj['children']:
                    extract_recursive(child, indent_level)
        elif isinstance(obj, list):
            for item in obj:
                extract_recursive(item, indent_level)
    
    extract_recursive(content_dict)
    
    # Join with newlines to preserve structure
    result = '\n'.join(markdown_parts).strip()
    
    # Clean up excessive blank lines but preserve intentional spacing
    import re
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result


def extract_ai_content_from_panels(doc_id, document_panels):
    """Extract AI-generated content from document panels."""
    if doc_id not in document_panels:
        return ""

    panels = document_panels[doc_id]
    if not isinstance(panels, dict):
        return ""

    # Look for summary panels
    for panel_id, panel_data in panels.items():
        if not isinstance(panel_data, dict):
            continue

        template_slug = panel_data.get('template_slug', '')
        title = panel_data.get('title', '')

        if 'summary' in template_slug.lower() or 'summary' in title.lower():
            content = panel_data.get('content', {})
            if isinstance(content, dict):
                extracted_text = extract_text_from_panel_content(content)
                if extracted_text.strip():
                    return extracted_text

    return ""


def extract_enhanced_notes(doc_id, doc, document_panels):
    """
    Extract enhanced notes combining manual notes AND AI-generated panel content.
    Preserves markdown formatting when available.
    """
    if not isinstance(doc, dict):
        return ""

    combined_content = []

    # Strategy 1: Get manual notes first (prefer markdown)
    manual_notes = ""
    
    # Try notes_markdown first (should preserve formatting)
    if 'notes_markdown' in doc:
        value = doc['notes_markdown']
        if isinstance(value, str) and value.strip():
            manual_notes = value.strip()
        # If it's a dict, try to extract markdown from structure
        elif isinstance(value, dict):
            manual_notes = extract_markdown_from_content(value).strip()
    
    # Try notes_content (structured content that might contain markdown)
    if not manual_notes and 'notes_content' in doc:
        value = doc['notes_content']
        if isinstance(value, dict):
            manual_notes = extract_markdown_from_content(value).strip()
        elif isinstance(value, str) and value.strip():
            manual_notes = value.strip()
    
    # Fallback to notes_plain (but this won't have markdown)
    if not manual_notes and 'notes_plain' in doc:
        value = doc['notes_plain']
        if isinstance(value, str) and value.strip():
            manual_notes = value.strip()

    # Strategy 2: Get AI-generated panel content
    ai_content = extract_ai_content_from_panels(doc_id, document_panels)

    # Strategy 3: Combine manual notes + AI content
    if manual_notes and ai_content:
        combined_content = f"""{manual_notes}

---

## AI-Generated Summary
{ai_content}"""
        return combined_content
    elif manual_notes:
        return manual_notes
    elif ai_content:
        return ai_content

    # Strategy 4: Check summary as final fallback
    if 'summary' in doc:
        summary = doc['summary']
        if isinstance(summary, dict):
            # Try to extract markdown from structured summary
            if 'markdown' in summary:
                summary_text = summary['markdown']
                if isinstance(summary_text, str):
                    cleaned_value = summary_text.strip()
                    if cleaned_value:
                        return cleaned_value
            elif 'text' in summary:
                summary_text = summary['text']
                if isinstance(summary_text, str):
                    cleaned_value = summary_text.strip()
                    if cleaned_value:
                        return cleaned_value
            # Try content structure
            elif 'content' in summary:
                extracted = extract_markdown_from_content(summary)
                if extracted.strip():
                    return extracted.strip()
        elif isinstance(summary, str):
            cleaned_value = summary.strip()
            if cleaned_value:
                return cleaned_value

    return ""


def extract_transcript(doc_id, transcripts, doc=None, state=None):
    """Extract transcript text for a document with speaker labels based on source field."""
    if doc_id not in transcripts:
        return ""

    transcript_data = transcripts[doc_id]
    
    # Get attendee information from document
    real_attendees = []
    other_attendee_name = None
    KATE_EMAIL = "kate@intelligems.io"  # Kate's email to identify her
    
    if doc and isinstance(doc, dict):
        people = doc.get("people", {})
        
        if isinstance(people, dict):
            # Get attendees list
            attendees = people.get("attendees", [])
            # Also get creator (Kate is often the creator, not in attendees)
            creator = people.get("creator", {})
            
            # Helper function to extract name and email from attendee/creator structure
            def extract_person_info(person_dict):
                """Extract name and email from person structure."""
                if not isinstance(person_dict, dict):
                    return None, None
                
                # Try to get email
                email = person_dict.get("email", "")
                
                # Try to get name from various possible locations
                name = None
                details = person_dict.get("details", {})
                if isinstance(details, dict):
                    person_info = details.get("person", {})
                    if isinstance(person_info, dict):
                        name_obj = person_info.get("name", {})
                        if isinstance(name_obj, dict):
                            # Prefer givenName (first name) over fullName
                            name = name_obj.get("givenName") or name_obj.get("fullName")
                
                # Fallback to email if no name found
                if not name and email:
                    name = email.split("@")[0].capitalize()
                
                return name, email
            
            # Process creator first (if exists)
            if creator:
                name, email = extract_person_info(creator)
                if name and email:
                    real_attendees.append({
                        "email": email,
                        "name": name
                    })
            
            # Process attendees list
            if isinstance(attendees, list):
                for attendee in attendees:
                    if isinstance(attendee, dict):
                        details = attendee.get("details", {})
                        if isinstance(details, dict):
                            # Skip groups
                            if details.get("group"):
                                continue
                        
                        name, email = extract_person_info(attendee)
                        if name and email:
                            # Check if this person is already in the list (avoid duplicates)
                            if not any(a.get("email") == email for a in real_attendees):
                                real_attendees.append({
                                    "email": email,
                                    "name": name
                                })
            
            # If exactly 2 attendees, find the other attendee (not Kate)
            if len(real_attendees) == 2:
                for attendee in real_attendees:
                    attendee_email = attendee.get("email", "").lower()
                    # Compare emails to identify Kate
                    if attendee_email != KATE_EMAIL.lower():
                        other_attendee_name = attendee["name"]
                        break
                
                # Fallback: if we still haven't found the other attendee, use the first one
                if not other_attendee_name and len(real_attendees) > 0:
                    # Use the first attendee that's not Kate
                    for attendee in real_attendees:
                        if attendee.get("email", "").lower() != KATE_EMAIL.lower():
                            other_attendee_name = attendee["name"]
                            break
                    # If still not found, just use first attendee
                    if not other_attendee_name:
                        other_attendee_name = real_attendees[0]["name"]

    if isinstance(transcript_data, list):
        transcript_parts = []
        
        for segment in transcript_data:
            if isinstance(segment, dict):
                # Get the source field
                source = segment.get("source", "").lower() if segment.get("source") else None
                
                # Get text content
                text = segment.get("text", "") or segment.get("content", "") or segment.get("transcript", "")
                
                if text:
                    text_str = str(text).strip()
                    if text_str:
                        # Determine speaker label based on source
                        speaker_label = None
                        
                        if source == "microphone":
                            # Kate's microphone
                            speaker_label = "Kate"
                        elif source == "system":
                            # Other attendee(s)
                            if len(real_attendees) == 2:
                                # Exactly 2 attendees, use the other attendee's name
                                # First try to use other_attendee_name if it was set
                                if other_attendee_name:
                                    speaker_label = other_attendee_name
                                
                                # If speaker_label not set yet, find the other attendee directly
                                if not speaker_label:
                                    for attendee in real_attendees:
                                        attendee_email = attendee.get("email", "").lower()
                                        if attendee_email != KATE_EMAIL.lower():
                                            speaker_label = attendee["name"]
                                            break
                                
                                # Final fallback
                                if not speaker_label:
                                    speaker_label = "Other attendee"
                            elif len(real_attendees) > 2:
                                # More than 2 attendees, use generic label
                                speaker_label = "Other attendee"
                            else:
                                # Fallback if we can't determine
                                speaker_label = "Other attendee"
                        
                        # Format with speaker label if available
                        if speaker_label:
                            transcript_parts.append(f"**{speaker_label}:** {text_str}")
                        else:
                            # No source field or unknown source, just add text
                            transcript_parts.append(text_str)
            elif isinstance(segment, str):
                transcript_parts.append(segment)
        
        # Join with double newlines to separate speaker turns
        return "\n\n".join(transcript_parts)
    elif isinstance(transcript_data, str):
        return transcript_data
    elif isinstance(transcript_data, dict):
        return str(transcript_data.get("text", ""))

    return ""


def get_last_friday_range():
    """
    Calculate the Friday-to-Friday date range for the current week.

    Returns:
        tuple: (start_datetime, end_datetime) representing last Friday 00:00 to this Friday 23:59
    """
    now = datetime.now()

    # Find the most recent Friday (0=Monday, 4=Friday, 6=Sunday)
    # If today is Friday, use today; otherwise find the previous Friday
    days_since_friday = (now.weekday() - 4) % 7

    if days_since_friday == 0:
        # Today is Friday
        end_date = now.replace(hour=23, minute=59, second=59, microsecond=0)
        start_date = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # Find the most recent past Friday
        end_date = (now - timedelta(days=days_since_friday)).replace(hour=23, minute=59, second=59, microsecond=0)
        start_date = (end_date - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)

    return start_date, end_date


def has_external_attendees(doc):
    """
    Check if a meeting has external (non-Intelligems) attendees.

    Returns:
        tuple: (has_external, attendee_count)
    """
    people = doc.get("people", {})
    if not isinstance(people, dict):
        return (False, 0)

    attendees = people.get("attendees", [])
    if not isinstance(attendees, list):
        return (False, 0)

    # Count real attendees (not groups)
    real_attendees = [a for a in attendees if isinstance(a, dict) and not a.get("details", {}).get("group")]
    attendee_count = len(real_attendees)

    # Check for external attendees by looking at email domains
    # Intelligems employees typically have @intelligems.io emails
    external_count = 0
    for attendee in real_attendees:
        email = attendee.get("details", {}).get("email", "")
        if email and "@intelligems.io" not in email.lower():
            external_count += 1

    has_external = external_count > 0
    return (has_external, attendee_count)


def get_meetings_in_range(start_date=None, end_date=None):
    """
    Get personal meetings within a date range.

    Args:
        start_date: datetime object or None (uses last Friday if None)
        end_date: datetime object or None (uses this Friday if None)

    Returns:
        list: List of meeting dicts with keys: id, title, date, url, notes, transcript, has_external_attendees, attendee_count
    """
    # Load cache
    cache_data = load_granola_cache()
    state = cache_data.get("cache", {}).get("state", {})
    documents = state.get("documents", {})
    transcripts = state.get("transcripts", {})
    document_panels = state.get("documentPanels", {})

    # Use last Friday range if dates not provided
    if start_date is None or end_date is None:
        start_date, end_date = get_last_friday_range()

    # Ensure dates are timezone-naive for comparison
    if start_date.tzinfo is not None:
        start_date = start_date.replace(tzinfo=None)
    if end_date.tzinfo is not None:
        end_date = end_date.replace(tzinfo=None)

    meetings = []

    for doc_id, doc in documents.items():
        # Filter to personal meetings only (meetings where user was present)
        if not is_personal_meeting(doc, state):
            continue

        created = doc.get("created_at")
        if not created:
            continue

        try:
            created_dt = parse_date(created)

            # Convert to timezone-naive
            if created_dt.tzinfo is not None:
                created_dt = created_dt.astimezone(timezone.utc).replace(tzinfo=None)

            # Check if within date range
            if start_date <= created_dt <= end_date:
                title = doc.get("title", "Untitled")
                notes = extract_enhanced_notes(doc_id, doc, document_panels)
                transcript = extract_transcript(doc_id, transcripts, doc, state)
                has_external, attendee_count = has_external_attendees(doc)

                meetings.append({
                    "id": doc_id,
                    "title": title,
                    "date": created_dt.strftime("%Y-%m-%d %H:%M"),
                    "url": get_granola_url(doc_id),
                    "notes": notes,
                    "transcript": transcript,
                    "has_external_attendees": has_external,
                    "attendee_count": attendee_count
                })

        except Exception as e:
            print(f"Warning: Failed to process document {doc_id}: {e}")
            continue

    # Sort by date (most recent first)
    meetings.sort(key=lambda x: x["date"], reverse=True)

    return meetings


def get_week_label(start_date, end_date):
    """
    Generate a week label from the start and end dates.

    Args:
        start_date: datetime object
        end_date: datetime object

    Returns:
        str: Formatted string like "Week of Jan 9 - Jan 16"
    """
    # Format: "Week of Jan 9 - Jan 16"
    # Use portable date formatting (remove leading zero from day)
    start_day = start_date.day
    end_day = end_date.day
    start_str = start_date.strftime(f"%b {start_day}")
    end_str = end_date.strftime(f"%b {end_day}")
    return f"Week of {start_str} - {end_str}"


def find_folder_by_name(folder_name, state):
    """
    Find a folder/collection by name in the Granola cache state.

    Args:
        folder_name: Name of the folder to find (case-insensitive)
        state: The state dict from the Granola cache

    Returns:
        str: The folder/list ID if found, None otherwise
    """
    document_lists_metadata = state.get("documentListsMetadata", {})
    
    for list_id, metadata in document_lists_metadata.items():
        if isinstance(metadata, dict):
            title = metadata.get("title", "")
            if title.lower() == folder_name.lower():
                return list_id
    
    return None


def get_documents_in_folder(folder_name):
    """
    Get all documents from a specific Granola folder/collection.

    Args:
        folder_name: Name of the folder to get documents from (e.g., "Claude Context")

    Returns:
        list: List of document dicts with keys: id, title, date, url, notes, transcript
    """
    # Load cache
    cache_data = load_granola_cache()
    state = cache_data.get("cache", {}).get("state", {})
    documents = state.get("documents", {})
    transcripts = state.get("transcripts", {})
    document_panels = state.get("documentPanels", {})
    document_lists = state.get("documentLists", {})

    # Find the folder by name
    folder_id = find_folder_by_name(folder_name, state)
    if not folder_id:
        return []

    # Get document IDs from the folder
    doc_ids = document_lists.get(folder_id, [])
    if not doc_ids:
        return []

    # Build list of documents
    result = []

    for doc_id in doc_ids:
        if doc_id not in documents:
            continue

        doc = documents[doc_id]
        if not isinstance(doc, dict):
            continue

        try:
            # Extract document data
            title = doc.get("title", "Untitled")
            created = doc.get("created_at")
            
            if created:
                created_dt = parse_date(created)
                # Convert to timezone-naive
                if created_dt.tzinfo is not None:
                    created_dt = created_dt.astimezone(timezone.utc).replace(tzinfo=None)
                date_str = created_dt.strftime("%Y-%m-%d %H:%M")
            else:
                date_str = "Unknown date"

            notes = extract_enhanced_notes(doc_id, doc, document_panels)
            transcript = extract_transcript(doc_id, transcripts, doc, state)

            result.append({
                "id": doc_id,
                "title": title,
                "date": date_str,
                "url": get_granola_url(doc_id),
                "notes": notes,
                "transcript": transcript
            })

        except Exception as e:
            print(f"Warning: Failed to process document {doc_id}: {e}")
            continue

    # Sort by date (most recent first)
    result.sort(key=lambda x: x["date"], reverse=True)

    return result


if __name__ == "__main__":
    # Test the functions
    print("Testing Granola reader...")
    print(f"Cache path: {GRANOLA_CACHE_PATH}")
    print(f"Cache exists: {GRANOLA_CACHE_PATH.exists()}")

    start, end = get_last_friday_range()
    print(f"\nDate range: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
    print(f"Week label: {get_week_label(start, end)}")

    meetings = get_meetings_in_range(start, end)
    print(f"\nFound {len(meetings)} personal meetings")

    for i, meeting in enumerate(meetings[:3], 1):  # Show first 3
        print(f"\n{i}. {meeting['title']}")
        print(f"   Date: {meeting['date']}")
        print(f"   URL: {meeting['url']}")
        print(f"   Notes length: {len(meeting['notes'])} chars")
        print(f"   Transcript length: {len(meeting['transcript'])} chars")
