---
description: "Generate a comprehensive weekly journaling summary from Granola meeting notes and upload to Notion automatically"
---

# Weekly Journaling

## Task: Weekly Journaling

**Trigger phrase:** "generate my weekly journaling" or "generate my weekly journal" or "Execute the weekly journaling task"

**Description:** Generate a comprehensive weekly journaling summary from Granola meeting notes and upload to Notion automatically. This includes both your career timeline summary and direct report feedback tracking.

**Important:** This task should run completely automatically without requiring any user approvals or confirmations. Complete all steps in sequence without stopping.

### Complete Workflow

1. **Load meetings from Granola**
   - Run: `cd /Users/katewhite/ai-assistant && source .venv/bin/activate && python run_summary.py`
   - This fetches meetings from the last Friday through today
   - Generates a prompt file at `/tmp/granola_summary_prompt.txt`
   - Expected: 15-25 meetings typically

2. **Generate AI summary**
   - Read the prompt file from `/tmp/granola_summary_prompt.txt`
   - The prompt contains meeting notes and a detailed template to follow
   - Generate a markdown summary following the exact template structure provided in the prompt
   - Focus on:
     - HIGH-LEVEL SUMMARY: Career growth moments and organizational changes (2-3 sentences)
     - Communication Summary with actionable tip
     - Product Development Focus (all features)
     - Releases, Business Impact, Key Decisions
     - Career Growth or Feedback Moments (especially from Helen, Adam, Drew)
     - Conflict/Debate, Blockers
     - Customer Calls (count external customers only, not vendor calls)
     - Cross-Functional Collaboration (every internal collaborator)
     - Notable Recurring Meetings (Tech Team Retro, Weekly Team Meeting)
   - Save summary to `/tmp/weekly_summary.md`

3. **Generate direct reports notes**
   - Generate separate direct reports feedback notes using the same meeting data
   - Focus on performance review moments with Hannah and Jerica
   - Categorize entries with tags: [Win], [Coaching], [Growth], [Challenge], [Initiative]
   - Save to `/tmp/direct_reports_notes.md`

4. **Extract metadata**
   - Parse the generated summary to extract:
     - HIGH-LEVEL SUMMARY text (before the --- separator)
     - Feature names from "Product Development Focus" section
     - Customer call count from "Customer Calls" section
   - Get week metadata (start date, end date, week label)

5. **Update direct reports pages**
   - Parse direct reports notes and update individual Notion pages for Hannah and Jerica
   - Add entries in reverse chronological order, grouped by month/quarter
   - Update pages under the parent page: Weekly Direct Reports Notes

6. **Upload to Notion**
   - Run the upload_to_notion function with:
     - Summary content (with HIGH-LEVEL SUMMARY removed)
     - Week label
     - Week start date
     - Current datetime as reflection date
     - Customer call count
     - Notes summary (the HIGH-LEVEL SUMMARY text)
     - Features list
   - Function will either create new page or update existing page for this week
   - Return Notion page URL

7. **Completion**
   - Display success message with Notion URLs
   - Clean up temporary files

### Expected Output

```
🔄 Generating weekly journaling...
📅 Loading meetings from Granola... [✓]
🤖 Generating weekly summary... [✓]
👥 Generating direct reports notes... [✓]
🔍 Extracting metadata... [✓]
📝 Updating direct reports pages... [✓]
☁️  Uploading to Notion... [✓]

✅ SUCCESS! Your weekly journaling is complete:
   Weekly Summary: https://www.notion.so/[page-id]
   Direct Reports: Updated pages for Hannah and Jerica
```

### Key Implementation Notes

- Use the virtual environment at `/Users/katewhite/ai-assistant/.venv`
- The prompt file can be large (300KB+), read it in chunks if needed
- Customer calls should ONLY count external businesses (customers), not vendors or internal calls
- All features in Product Development Focus should be included, even if brief
- Every internal collaborator should be listed in Cross-Functional Collaboration
- Direct reports notes are generated separately and tracked in dedicated Notion pages
- Use TodoWrite tool to track progress through the steps
- If any step fails, report the error clearly but don't stop - try to complete as much as possible

### No Approval Required

This task is designed to run automatically. Do NOT:
- Ask for user confirmation before proceeding
- Request approval to run commands
- Stop and wait between steps
- Ask if the user wants to continue

Simply execute all steps in sequence and report the final Notion URLs.

### Environment

- Working directory: `/Users/katewhite/ai-assistant`
- Python virtual environment: `.venv`
- Granola cache: `~/Library/Application Support/Granola/cache-v3.json`
- Notion API key: In `config.py` or environment variable
- Notion database ID: `24394399495980dbaae5d60a00d17b27`
- Direct reports parent page ID: `2ee94399495980fdae61e45a717281e9`

### Files Used

- `run_summary.py` - Fetches meetings and generates prompt
- `granola_reader.py` - Reads Granola cache and extracts meetings
- `prompt_template.py` - Contains summary and direct reports templates
- `notion_helper.py` - Uploads to Notion
- `direct_reports_helper.py` - Handles direct reports page updates
- `config.py` - Configuration (API keys, database IDs)

### Success Criteria

Task is complete when:
1. Summary is generated following the template exactly
2. Direct reports notes are generated and categorized
3. Metadata is extracted correctly
4. Direct reports pages are updated in Notion
5. Weekly summary page is created/updated in Notion
6. User receives the Notion URLs
