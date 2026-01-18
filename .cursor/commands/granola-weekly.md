---
description: "Generate a comprehensive weekly summary from Granola meeting notes and upload to Notion automatically"
---

# Granola Weekly Summary

## Task: Weekly Granola Summary

**Trigger phrase:** "generate my weekly granola summary" or "Execute the weekly Granola summary task"

**Description:** Generate a comprehensive weekly summary from Granola meeting notes and upload to Notion automatically.

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

3. **Extract metadata**
   - Parse the generated summary to extract:
     - HIGH-LEVEL SUMMARY text (before the --- separator)
     - Feature names from "Product Development Focus" section
     - Customer call count from "Customer Calls" section
   - Get week metadata (start date, end date, week label)

4. **Upload to Notion**
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

5. **Completion**
   - Display success message with Notion URL
   - Clean up temporary files

### Expected Output

```
🔄 Generating weekly Granola summary...
📅 Loading meetings from Granola... [✓]
🤖 Generating AI summary... [✓]
🔍 Extracting metadata... [✓]
☁️  Uploading to Notion... [✓]

✅ SUCCESS! Your weekly summary is in Notion:
   https://www.notion.so/[page-id]
```

### Key Implementation Notes

- Use the virtual environment at `/Users/katewhite/ai-assistant/.venv`
- The prompt file can be large (300KB+), read it in chunks if needed
- Customer calls should ONLY count external businesses (customers), not vendors or internal calls
- All features in Product Development Focus should be included, even if brief
- Every internal collaborator should be listed in Cross-Functional Collaboration
- Use TodoWrite tool to track progress through the steps
- If any step fails, report the error clearly but don't stop - try to complete as much as possible

### No Approval Required

This task is designed to run automatically. Do NOT:
- Ask for user confirmation before proceeding
- Request approval to run commands
- Stop and wait between steps
- Ask if the user wants to continue

Simply execute all steps in sequence and report the final Notion URL.

### Environment

- Working directory: `/Users/katewhite/ai-assistant`
- Python virtual environment: `.venv`
- Granola cache: `~/Library/Application Support/Granola/cache-v3.json`
- Notion API key: In `config.py` or environment variable
- Notion database ID: `24394399495980dbaae5d60a00d17b27`

### Files Used

- `run_summary.py` - Fetches meetings and generates prompt
- `granola_reader.py` - Reads Granola cache and extracts meetings
- `prompt_template.py` - Contains summary template
- `notion_helper.py` - Uploads to Notion
- `config.py` - Configuration (API keys, database IDs)

### Success Criteria

Task is complete when:
1. Summary is generated following the template exactly
2. Metadata is extracted correctly
3. Page is created/updated in Notion
4. User receives the Notion URL
