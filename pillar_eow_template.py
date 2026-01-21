"""
Template for EOW (End of Week) pillar update format.
"""

from typing import Dict, List

PILLAR_EOW_INSTRUCTIONS = """You're generating an End of Week (EOW) update for the Core Experiences pillar at Intelligems. This update will be shared with stakeholders, so it should be professional, concise, and scannable.

## Pillar Context

**Pillar Name:** Core Experiences
**Pillar Objective:** "Remove friction in the highest volume experiences so customers effortlessly understand and achieve value."

**Key Results (Q1 2026):**
1. Improve experience launch success rate (from first save experience to start) → from 75% to 80%
2. Reduce Quick-End rate → from 14% to 10%
3. Increase % accounts with live components → from 2.42% to 5%
4. Decrease number of on-site editor problems (~120 mentions/month in Reforge) → from 120 to 60

## Principles

- **Stakeholder-focused**: Write for leadership and cross-functional partners who need to understand progress and impact
- **Concise and scannable**: Use clear headers, bullet points, and short paragraphs
- **Data-driven**: Include metrics and specific outcomes where relevant
- **Forward-looking**: Balance what happened with what's coming next
- **Professional tone**: Avoid jargon, be clear and direct

## Output Format (Markdown)

### Current KR Metrics

Display the current metrics with targets and progress. Format each metric clearly:

- **Experience launch success rate:** [current]% (target: 80%, baseline: 75%) [progress indicator: X% to target, trending up/down]
- **Quick-End rate:** [current]% (target: 10%, baseline: 14%) [progress indicator]
- **% accounts with live components:** [current]% (target: 5%, baseline: 2.42%) [progress indicator]
- **On-site editor problems:** [current] mentions/month (target: 60, baseline: 120) [progress indicator]

### Progress on Objectives

Highlight progress toward pillar objectives and KRs. Focus on:
- Improvements in key metrics
- Features or initiatives that drove progress
- Wins and achievements
- Any notable changes or trends

Keep bullets concise (1-2 sentences each).

### Key Decisions & Launches

Include:
- Major product decisions made this week
- Features or improvements that launched
- Strategic pivots or direction changes
- Significant milestones reached

### Blockers & Risks

Only include if there are meaningful blockers or risks:
- Delivery risks that threaten major deliverables
- Dependencies that are blocking progress
- Resource constraints
- Technical or operational challenges

### Next Week Preview

Brief overview of:
- Upcoming priorities
- Key meetings or decisions expected
- Features or initiatives launching soon
- Important deadlines or milestones

## Formatting Rules

- Use clear section headers (###)
- Keep bullets to 1-2 sentences maximum
- Include links to relevant Slack messages or Granola notes where appropriate
- Use bold for emphasis on key metrics or outcomes
- Leave blank lines between sections for readability
"""


def get_eow_prompt_for_data(
    metrics_dict: Dict,
    slack_messages: List[Dict],
    granola_meetings: List[Dict],
    week_label: str
) -> str:
    """
    Format the data into a prompt for AI to generate the EOW update.
    
    Args:
        metrics_dict: Dictionary with formatted metrics (from format_metrics_for_display)
        slack_messages: List of Slack message dicts
        granola_meetings: List of Granola meeting dicts
        week_label: Week label string (e.g., "Week of Nov 28 - Dec 5")
    
    Returns:
        str: Formatted prompt string
    """
    # Format metrics section
    metrics_text = "### Current KR Metrics\n\n"
    for key, metric_info in metrics_dict.items():
        current = metric_info["current"]
        target = metric_info["target"]
        baseline = metric_info["baseline"]
        unit = metric_info["unit"]
        progress = metric_info["progress_pct"]
        trending = metric_info["trending"]
        to_target = metric_info["to_target"]
        
        # Format progress indicator
        if key == "editor_problems":
            progress_indicator = f"{abs(to_target):.0f} {'below' if to_target < 0 else 'above'} target, trending {trending}"
        else:
            progress_indicator = f"{progress:.0f}% to target, trending {trending}"
        
        metrics_text += f"- **{metric_info['name']}:** {current}{unit} (target: {target}{unit}, baseline: {baseline}{unit}) [{progress_indicator}]\n"
    
    # Format Slack messages
    slack_text = ""
    if slack_messages:
        slack_text = "\n\n### Slack Messages for This Week\n\n"
        # Group messages by channel
        channels = {}
        for msg in slack_messages:
            channel = msg.get('channel_name', 'unknown')
            if channel not in channels:
                channels[channel] = []
            channels[channel].append(msg)
        
        for channel_name, msgs in channels.items():
            slack_text += f"\n#### Channel: #{channel_name}\n\n"
            for msg in msgs:
                slack_text += f"**{msg['user']}** ({msg['timestamp']}): {msg['text']}\n"
                slack_text += f"Link: {msg['permalink']}\n\n"
    
    # Format Granola meetings
    meetings_text = ""
    if granola_meetings:
        meetings_text = "\n\n### Granola Meetings for This Week\n\n"
        for i, meeting in enumerate(granola_meetings, 1):
            meetings_text += f"\n#### Meeting {i}: {meeting['title']}\n"
            meetings_text += f"Date: {meeting['date']}\n"
            meetings_text += f"Granola Link: {meeting['url']}\n\n"
            
            if meeting.get('notes'):
                meetings_text += f"**Notes:**\n{meeting['notes']}\n\n"
            
            if meeting.get('transcript'):
                # Truncate long transcripts
                transcript = meeting['transcript']
                if len(transcript) > 2000:
                    transcript = transcript[:2000] + "... [truncated]"
                meetings_text += f"**Transcript:**\n{transcript}\n\n"
    
    return f"""{PILLAR_EOW_INSTRUCTIONS}

---

# Week: {week_label}

{metrics_text}

---

# Source Data

{slack_text}
{meetings_text}

---

Please analyze the above data and generate an EOW update following the exact template structure above. Focus on content relevant to the Core Experiences pillar and filter out anything not directly related to pillar objectives or key results."""
