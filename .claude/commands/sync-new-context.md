---
description: "Sync context files from Granola and Notion to the project's context directory"
---

# Sync New Context

## Task: Sync Context from Granola and Notion

**Trigger phrases:**
- "sync new context" or "sync all context" - Sync from both Granola and Notion
- "sync granola calls" or "sync calls from granola" - Sync only from Granola
- "sync from notion" or "sync notion context" - Sync only from Notion

**Description:** Sync context files from Granola "Claude Context" folder and/or Notion database to the project's context directories, making important content easily accessible as context for other commands.

**Important:** This is a manual command that Kate runs when she wants to sync new context. 
- Granola calls are curated by moving them to the "Claude Context" folder in Granola
- Notion pages are synced based on their "Last Modified" date (only pages modified since last sync)

### Complete Workflow

#### Option 1: Sync All Context (Both Sources)

1. **Run unified sync script**
   - Run: `cd /Users/katewhite/ai-assistant && source .venv/bin/activate && python sync_all_context.py`
   - This runs both Granola and Notion syncs sequentially
   - Displays results for each source

#### Option 2: Sync from Granola Only

1. **Run Granola sync script**
   - Run: `cd /Users/katewhite/ai-assistant && source .venv/bin/activate && python sync_granola_calls.py`
   - This fetches all documents from the "Claude Context" folder in Granola
   - For each document:
     - Generates a safe filename from title and date (e.g., `2025-01-15-strategy-chat-with-adam.md`)
     - Checks if file already exists (skips if already synced to avoid duplicates)
     - Creates markdown file with frontmatter (title, date, granola_url, granola_id), transcript, and notes

#### Option 3: Sync from Notion Only

1. **Run Notion sync script**
   - Run: `cd /Users/katewhite/ai-assistant && source .venv/bin/activate && python sync_notion_context.py`
   - This fetches pages from Notion database modified since last sync
   - For each page:
     - Uses Filename property if available, otherwise generates from Title
     - Checks if file already exists (updates if exists, creates if new)
     - Creates/updates markdown file with frontmatter (title, filename, notion_url, notion_id, last_modified) and content

2. **Display results**
   - Shows summary of:
     - Number of files synced/updated
     - Number of files skipped (if applicable)
     - Any errors encountered
   - Lists each synced file with its filename

### Expected Output (Granola)

```
📂 Syncing calls from Granola folder: 'Claude Context'
📁 Target directory: /Users/katewhite/ai-assistant/.claude/context/calls

Found 3 document(s) in folder

============================================================
Sync Results
============================================================

✅ Synced 2 call(s):
   • Strategy Chat with Adam
     → 2025-01-15-strategy-chat-with-adam.md
   • Product Vision Discussion
     → 2025-01-10-product-vision-discussion.md

⏭️  Skipped 1 call(s) (already exist):
   • Weekly Team Meeting

Total: 3 | Synced: 2 | Skipped: 1 | Errors: 0
```

### Expected Output (Notion)

```
📂 Syncing context files from Notion database
📁 Target directory: /Users/katewhite/ai-assistant/.claude/context/core

📅 Last sync: 2025-01-10 14:30:00
   Fetching pages modified since then...

Found 2 page(s) to sync

============================================================
Sync Results
============================================================

✅ Synced 1 file(s):
   • Product Strategy Document
     → product-strategy-document.md

🔄 Updated 1 file(s):
   • Vision 2026
     → vision-2026.md

Total: 2 | Synced: 1 | Updated: 1 | Errors: 0
Last sync time updated to: 2025-01-15 10:30:00 UTC
```

### Key Implementation Notes

**Granola Sync:**
- Uses the virtual environment at `/Users/katewhite/ai-assistant/.venv`
- Files are saved to `.claude/context/calls/` directory
- Filenames are generated from date and title (slugified)
- Deduplication is based on `granola_id` in frontmatter
- Each file includes:
  - Frontmatter with metadata (title, date, granola_url, granola_id)
  - Full transcript (if available)
  - Notes (if available)
- Files that already exist are skipped to avoid duplicates

**Notion Sync:**
- Files are saved to `.claude/context/core/` directory
- Filenames use Filename property if available, otherwise generated from Title (slugified)
- Only syncs pages modified since last sync (tracked in `.notion_sync_state.json`)
- Deduplication is based on `notion_id` in frontmatter
- Each file includes:
  - Frontmatter with metadata (title, filename, original_url, notion_url, notion_id, last_modified)
  - Full page content (converted from Notion blocks to markdown)
- Files are updated if the Notion page has been modified

### File Format

**Granola Call Files** (in `calls/` directory):

```markdown
---
title: "Call Title"
date: 2025-01-15 14:30
granola_url: "https://notes.granola.ai/d/[doc-id]"
granola_id: "[doc-id]"
---

**Granola URL:** [https://notes.granola.ai/d/[doc-id]](https://notes.granola.ai/d/[doc-id])

<hr>

## Transcript

[Full transcript text...]

---

## Notes

[Notes text if available...]
```

**Notion Context Files** (in `core/` directory):

```markdown
---
title: "Document Title"
last_modified: 2025-01-15 10:30:00 UTC
notion_url: "https://www.notion.so/[page-id]"
notion_id: "[page-id]"
filename: "document-title.md"
original_url: "https://example.com/original-source"
---

**Original URL:** [https://example.com/original-source](https://example.com/original-source)

**My Notion URL:** [https://www.notion.so/[page-id]](https://www.notion.so/[page-id])

**Last Modified:** 2025-01-15 10:30:00 UTC

<hr>

[Page content converted to markdown...]
```

### Environment

- Working directory: `/Users/katewhite/ai-assistant`
- Python virtual environment: `.venv`
- Granola cache: `~/Library/Application Support/Granola/cache-v3.json`
- Target folder in Granola: "Claude Context"
- Notion database ID: Set in `config.py` as `NOTION_CONTEXT_DATABASE_ID`
- Output directories:
  - Granola: `.claude/context/calls/`
  - Notion: `.claude/context/core/`

### Files Used

**Granola Sync:**
- `sync_granola_calls.py` - Granola sync script
- `granola_reader.py` - Reads Granola cache and extracts documents from folders

**Notion Sync:**
- `sync_notion_context.py` - Notion sync script
- `notion_reader.py` - Reads Notion database and converts blocks to markdown
- `.notion_sync_state.json` - Tracks last sync time

**Unified:**
- `sync_all_context.py` - Runs both syncs

### Success Criteria

**Granola Sync:**
1. All documents from "Claude Context" folder are processed
2. New calls are synced to markdown files
3. Existing calls are skipped (no duplicates created)
4. User receives a summary of synced/skipped calls

**Notion Sync:**
1. All pages modified since last sync are processed
2. New pages are synced to markdown files
3. Modified pages are updated
4. Last sync time is updated
5. User receives a summary of synced/updated files

### Notion Database Setup

The Notion database should have these properties:
- **Title** (title) - Page title
- **Filename** (rich_text) - Optional explicit filename (if not provided, derived from Title)
- **original URL** (url or rich_text) - Optional URL to the original source
- **Last Modified** (last_edited_time) - Automatically tracked by Notion

Set the database ID in `config.py` as `NOTION_CONTEXT_DATABASE_ID`.
