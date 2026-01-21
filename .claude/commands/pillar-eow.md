---
description: "Generate End of Week (EOW) pillar update for Core Experiences pillar from Slack messages and Granola calls"
---

# Pillar EOW Update

## Task: Generate Core Experiences Pillar EOW Update

**Trigger phrase:** "generate my pillar eow update" or "create pillar eow"

**Description:** Generate an End of Week (EOW) update for the Core Experiences pillar by analyzing Slack messages from #pillar-core-experiences and #product-announce channels, plus Granola calls from the past week, and sending a formatted draft to the user via Slack DM for review.

**Important:** This task requires current KR metrics to be provided in the command. The user will include metrics in their message.

### Complete Workflow

1. **Parse KR metrics from user input**
   - Extract metric values from the user's command message
   - Expected metrics:
     - Experience launch success rate (target: 80%, baseline: 75%)
     - Quick-End rate (target: 10%, baseline: 14%)
     - % accounts with live components (target: 5%, baseline: 2.42%)
     - On-site editor problems (target: 60, baseline: 120)
   - Accepts various formats:
     - "launch: 77%, quickend: 12%, components: 3.2%, editor: 95"
     - "experience launch success is 77%, quick-end rate is 12%..."
     - Natural language descriptions

2. **Get date range**
   - Calculate last Friday to this Friday (same as weekly summary)
   - Generate week label (e.g., "Week of Nov 28 - Dec 5")

3. **Fetch Slack messages**
   - Connect to Slack API using bot token
   - Fetch messages from:
     - #pillar-core-experiences
     - #product-announce
   - Filter by date range (last Friday to this Friday)
   - Extract: user, timestamp, text, permalink

4. **Fetch Granola calls**
   - Use existing `get_meetings_in_range()` function
   - Get personal meetings from the date range
   - Extract: title, date, notes, transcript, URL

5. **Filter for pillar relevance**
   - Filter Slack messages and Granola calls for Core Experiences pillar content
   - Keywords: core experiences, experience launch, quick-end, component, editor, friction, high volume, etc.
   - Include all messages from #pillar-core-experiences channel

6. **Generate AI prompt**
   - Include pillar context (objective, KRs)
   - Include current KR metrics with targets and baselines
   - Include filtered Slack messages grouped by channel
   - Include filtered Granola meetings
   - Include EOW format template instructions

7. **Generate EOW update with Claude**
   - Read the prompt file from `/tmp/pillar_eow_prompt.txt`
   - Generate formatted EOW update following the exact template structure provided in the prompt
   - Include:
     - Current KR Metrics section (with progress indicators)
     - Progress on Objectives
     - Key Decisions & Launches
     - Blockers & Risks (if any)
     - Next Week Preview
   - Save generated update to `/tmp/pillar_eow_draft.md`

8. **Send draft to user via Slack DM**
   - Read the generated update from `/tmp/pillar_eow_draft.md`
   - Look up user by email (from config)
   - Open DM conversation
   - Send formatted update as markdown
   - If DM fails, inform user where file is saved

### Expected Output

```
🔄 Generating Core Experiences pillar EOW update...

📊 Step 1: Parsing KR metrics from input...
   Parsed 4 metrics
   - Experience launch success rate: 77.0%
   - Quick-End rate: 12.0%
   - % accounts with live components: 3.2%
   - On-site editor problems: 95.0 mentions/month

📅 Step 2: Getting date range...
   Week: Week of Nov 28 - Dec 5
   Date range: 2024-11-28 to 2024-12-05

💬 Step 3: Fetching Slack messages...
   Found 45 messages in #pillar-core-experiences
   Found 12 messages in #product-announce

📞 Step 4: Fetching Granola calls...
   Found 8 meetings

🔍 Step 5: Filtering content for pillar relevance...
   Filtered to 38 relevant Slack messages
   Filtered to 5 relevant meetings

📝 Step 6: Generating AI prompt...
   Prompt length: 15234 characters
   ✅ Prompt ready with X Slack messages and Y meetings
   📄 Saved to: /tmp/pillar_eow_prompt.txt

[Claude reads prompt and generates update]

📤 Step 8: Sending draft to Slack DM...
   ✅ Draft sent to Slack DM

✅ EOW update generation complete!
```

### Key Implementation Notes

- Use the virtual environment at `/Users/katewhite/ai-assistant/.venv`
- Metrics parsing is flexible - handles various input formats
- Content filtering focuses on Core Experiences pillar relevance
- EOW format is stakeholder-friendly and scannable
- If Slack DM fails, draft is saved to file for manual retrieval

### Environment Variables Required

- `SLACK_BOT_TOKEN` - Slack bot OAuth token (required for fetching messages and sending DM)
- `SLACK_USER_EMAIL` - User email for DM delivery (optional, defaults to kate@intelligems.io)
- `SLACK_CHANNELS` - Comma-separated channel list (optional, defaults to pillar-core-experiences,product-announce)

**Note:** No Anthropic API key needed - Claude generates the update directly when running this command, just like the weekly Granola summary.

### Files Used

- `generate_pillar_eow.py` - Main script
- `slack_reader.py` - Slack API integration
- `granola_reader.py` - Granola cache reading
- `pillar_eow_template.py` - EOW format template
- `metrics_parser.py` - Metrics parsing from input
- `config.py` - Configuration

### Success Criteria

Task is complete when:
1. Metrics are parsed from user input
2. Slack messages and Granola calls are fetched
3. Content is filtered for pillar relevance
4. EOW update is generated following the template
5. Draft is sent to user via Slack DM (or saved to file)

### Usage Examples

**Structured format:**
```
generate my pillar eow update - launch: 77%, quickend: 12%, components: 3.2%, editor: 95
```

**Natural language:**
```
generate my pillar eow update. Current metrics: experience launch success is 77%, quick-end rate is 12%, component adoption is 3.2%, and editor problems are at 95 mentions
```

**Mixed format:**
```
create pillar eow. Metrics: launch 77%, quick-end 12%, components 3.2%, editor problems 95
```
