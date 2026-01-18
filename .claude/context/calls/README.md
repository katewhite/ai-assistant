# Calls Context

This directory contains synced call transcripts from Granola's "Claude Context" folder.

## Purpose

Important calls are manually curated by moving them to the "Claude Context" folder in Granola, then synced here using the `sync new context` command. These calls are made available as context for other Claude commands.

## Syncing

To sync new calls, run:
```
sync new context
```

This will:
- Fetch all documents from the "Claude Context" folder in Granola
- Create markdown files for new calls (skipping ones that already exist)
- Save them to this directory with filenames based on date and title

## File Format

Each call file includes:
- Frontmatter with metadata (title, date, granola_url, granola_id)
- Full transcript (if available)
- Notes (if available)

Files are deduplicated based on `granola_id` in the frontmatter, so running the sync command multiple times won't create duplicates.
