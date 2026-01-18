"""
Template for weekly Granola summary following the 11-section structure.
This will be used by Claude Code when generating the weekly summary.
"""

WEEKLY_SUMMARY_INSTRUCTIONS = """You're reviewing a week's worth of meeting notes and transcripts from a Lead Product Manager at Intelligems. Your job is to extract only the most meaningful and career-relevant highlights — this is not a status update or a full recap.

The goal is to create a timeline entry someone could scan years later to trace strategic leadership, product thinking, and long-term impact.

📋 Team Context (Critical for Prioritization)

**Leadership & High-Impact Feedback:**
- **Helen** (VP Product & Design, Kate's manager) - Any feedback is career-critical
- **Adam** (CTO/Co-founder) - Calls the shots, strategic decisions with him are highly significant
- **Drew** (CEO/Co-founder) - Less frequent but very important when it happens

**Kate's Direct Reports:**
- **Hannah** (Product Manager, Kate's first direct report) - All mentorship, coaching, wins, and challenges worth tracking for reviews
- **Jerica** (Product Manager, newer direct report) - Track development progress, wins, and coaching opportunities

**Kate's Growth Priorities:**
- **Data team (Jerry, Andrew, Michael)** - Kate wants to guide/mentor them more; shows expanding influence

**Regular Collaborators:**
- Shane (PMM), Emily (Growth PM), Angela/Angel/Craig (Designers) - Note significant strategic work, but routine collaboration is less noteworthy

**Prioritization:**
1. Feedback/decisions from Helen, Adam, or Drew (career-critical)
2. Direct report moments with Hannah and Jerica (coaching, wins, challenges) - track for performance reviews
3. Instances of guiding the data team (expanding influence)
4. Strategic product decisions (especially with Adam)
5. Operational improvements and process changes - how we work, team enablement, tools that increase impact (e.g., enabling Attention in Pylon for product insights)

🧠 Principles

- **Career timeline mindset**: Write as if you're building a career portfolio to review years from now. Highlight what shaped your growth, influence, and impact—not what you did day-to-day. Think: "What would I want to remember about this week when I'm reflecting on my career trajectory?"

- **Ultra-high bar for inclusion**: Ask "Would this make my career highlight reel?" Focus on:
  - Career growth moments (new responsibilities, team changes, feedback)
  - Major strategic pivots or organizational changes
  - Significant launches or business wins
  - Conflict/debate that changed direction

  **Cut everything else.** Routine planning, tactical coordination, and incremental progress don't belong here.

- **BUT: Always include every feature worked on. Always include every internal collaboration (every colleague you met with). Always include every customer call in the Customer Call Tracker.** Keep these sections comprehensive even if individual bullets are brief.

- **Ultra-concise bullets**: 2 sentences maximum. 1 sentence is better. Get straight to the point—what happened and why it matters. Cut all filler words and unnecessary context.

- **Scannable tone**: Write conversationally, like you're telling a friend about your week. Avoid corporate jargon and overly formal language. Make it easy to skim.

- Include a link to the source note at the end of each bullet: `([Meeting Name](https://notes.granola.ai/link))`

📝 High-Level Summary (REQUIRED)

Before generating the full summary, write a 2-3 sentence high-level overview capturing what you'll remember years from now when reflecting on your career growth. Prioritize in this order:
1. **Career growth moments** - team restructuring, new responsibilities, direct reports, promotions, significant feedback
2. **Organizational/strategic pivots** - product area mergers, pillar ownership changes, major philosophical shifts
3. **Big launches** - only if truly significant releases
4. **Strategic decisions** - only if they fundamentally changed direction

Skip tactical work, planning sessions, and routine product development. Focus on: "What changed about my role, influence, or the company structure?"

Format this as:
```
HIGH-LEVEL SUMMARY: [2-3 sentences focusing on career growth and structural changes]
```

---

# ✍️ Output Template (Markdown Format – Use Exactly)

### 💬 Communication Summary

Analyze communication patterns across the week—how you showed up, where you were most effective, and where you could improve. Keep it reflective but practical.

- **This Week's Communication Style:** [2-3 sentences analyzing your communication patterns—Were you clear and direct? Collaborative? Asking good questions? Driving alignment? Being proactive or reactive? Did you communicate timely or wait too long on important topics?]

- **One Tip for Next Week:** [1 actionable tip to improve communication next week based on this week's patterns. Be specific—not generic advice like "communicate better." Examples: "Follow up decisions in writing within 24hrs," "Ask clarifying questions before jumping to solutions," "Give Hannah more context on why, not just what."]

### 👩‍💻 Product Development Focus

Feature-level work this week. Include ALL features but keep bullets ultra-brief—only highlight major decisions, pivots, or milestones worth remembering. 2 sentences max, 1 is better.

- **[Feature]** → [What's the key decision or outcome? 1-2 sentences.] ([Meeting Name](https://notes.granola.ai/link))

### 🚀 Releases

Features that launched publicly. Include ship date + current status.

- **[Feature]** → [ship date + summary] ([Meeting Name](https://notes.granola.ai/link))

### 📊 Business Impact Highlights

Only include wins with real numbers or significant risks. 2 sentences max.

- **[Topic]** → [What's the metric/impact? 1-2 sentences.] ([Meeting Name](https://notes.granola.ai/link))

### 🧠 Key Decisions Made

Only major strategic or structural decisions that changed direction. 2 sentences max.

- **[Topic]** → [What changed and why it matters? 1-2 sentences.] ([Meeting Name](https://notes.granola.ai/link))

### 💼 Career Growth or Feedback Moments

Capture both explicit and implicit feedback from key stakeholders (especially Helen, Adam, Drew). Explicit: direct praise, critique, new responsibilities, team changes (include exact quotes). Implicit: How stakeholders respond to your ideas—trust and deference OR pushback and concern. Look for signals in debate style, communication patterns, hesitation, questioning your judgment, or showing confidence in your decisions. Include both positive and critical signals. 2 sentences max.

- **[Topic]** → [What happened? Include direct quote if explicit feedback. For implicit, describe the signal and what it suggests—whether positive (trust, deference) or critical (concern, pushback, hesitation). 1-2 sentences.] ([Meeting Name](https://notes.granola.ai/link))

### 👥 Direct Reports Feedback Moments

Track notable moments with direct reports (Hannah and Jerica) worth remembering for performance reviews. Include both positive highlights (wins, growth, strong work, initiative) and areas for coaching (mistakes, resistance, skill gaps, behavioral issues). Be specific and objective—what happened, how they responded, what it reveals about their performance and development needs. 2 sentences max.

- **[Name - Topic]** → [What happened and why it matters for their development or review? Include both context and your assessment. 1-2 sentences.] ([Meeting Name](https://notes.granola.ai/link))

### ⚔️ Conflict / Intense Debate Moments

Meaningful disagreements or debates that shifted direction. 2 sentences max.

- **[Topic]** → [What was the tension and how did it resolve? 1-2 sentences.] ([Meeting Name](https://notes.granola.ai/link))

### 🚧 Blockers or Delivery Risks

Only include if it meaningfully threatens a major deliverable. 2 sentences max.

- **[Topic]** → [What's blocked and what's the impact? 1-2 sentences.] ([Meeting Name](https://notes.granola.ai/link))

### 📞 Customer Calls

**Definition of Customer Call:** Any call with external participants (non-Intelligems employees). First, identify if there are external participants. Then look at the call topic/title to classify:
- **Customer calls:** External businesses using Intelligems (e.g., Serenity Kids, merchant calls, demo calls, discovery calls)
- **Vendor calls:** External tool/service providers (don't count these in the total)
- **Internal calls:** Only Intelligems employees (don't count these)

Count ONLY customer calls (exclude vendor calls and internal calls).

- **Total customer calls:** [Number - count only customer calls, not vendor or internal calls]
- **Customers:** [Business names only - list the customer companies]
- **Topics:** [1-2 sentence summary of key themes or specific feedback from customers]

### 🤝 Cross-Functional Collaboration Highlights

Include **every** internal collaborator but keep bullets brief—just the key outcome. 2 sentences max, 1 is better.

- **[Name]** → [What was the outcome or decision? 1-2 sentences.] ([Meeting Name](https://notes.granola.ai/link))

### 🏢 Notable Recurring Meetings

Include Weekly Team Meeting and Tech Team Retro (if happened). Focus on key decisions or takeaways. 2 sentences max.

- **Weekly Team Meeting / [Org]** → [Key themes or decisions? 1-2 sentences.] ([Meeting Name](https://notes.granola.ai/link))
- **Tech Team Retro** → [Key topics or action items? 1-2 sentences.] ([Meeting Name](https://notes.granola.ai/link))

# 📐 Output Format Rules (Critical)

- Section headers must start with `###`
- **Strict 2-sentence maximum per bullet.** 1 sentence is better. Get straight to the point—no filler.
- Write conversationally. Avoid corporate jargon. Make it scannable.
- Each bullet: **[Topic/Name]** → [Outcome in 1-2 sentences] ([Meeting Name](link))
- Use exact meeting titles from source data for link text
- Leave blank line between sections
- **Career timeline mindset**: Would you include this in a highlight reel of your career growth? If no, cut it.
- **Communication Summary exception**: This section has 2-3 sentences for style analysis + 1 specific actionable tip. No meeting links needed here—it's a meta-reflection on the week."""


def get_summary_prompt_for_meetings(meetings):
    """
    Format the meetings data into a prompt for Claude Code to generate the summary.

    Args:
        meetings: List of meeting dicts with keys: id, title, date, url, notes, transcript,
                  has_external_attendees, attendee_count

    Returns:
        str: Formatted prompt string
    """
    meetings_text = ""
    for i, meeting in enumerate(meetings, 1):
        meetings_text += f"\n\n## Meeting {i}: {meeting['title']}\n"
        meetings_text += f"Date: {meeting['date']}\n"
        meetings_text += f"Granola Link: {meeting['url']}\n"

        # Include attendee information to help classify customer calls
        has_external = meeting.get('has_external_attendees', False)
        attendee_count = meeting.get('attendee_count', 0)
        meetings_text += f"Has External Attendees: {'Yes' if has_external else 'No'}\n"
        meetings_text += f"Total Attendees: {attendee_count}\n\n"

        if meeting.get('notes'):
            meetings_text += f"**Notes:**\n{meeting['notes']}\n\n"

        if meeting.get('transcript'):
            meetings_text += f"**Transcript:**\n{meeting['transcript']}\n\n"

        meetings_text += "---\n"

    return f"""{WEEKLY_SUMMARY_INSTRUCTIONS}

---

# Meeting Data for This Week

{meetings_text}

---

Please analyze the above meetings and generate a summary following the exact template structure above."""
