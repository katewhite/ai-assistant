---
title: "Visual Experience Builder"
last_modified: 2026-01-19 16:19:00 UTC
notion_url: "https://www.notion.so/Visual-Experience-Builder-2ec94399495980b687d3f63c4d9e4849"
notion_id: "2ec94399-4959-80b6-87d3-f63c4d9e4849"
original_url: "https://www.notion.so/intelligems/Visual-experience-builder-2ce2b3722092806a9a0fe30d434ac5a7"
---

**Original URL:** [https://www.notion.so/intelligems/Visual-experience-builder-2ce2b3722092806a9a0fe30d434ac5a7](https://www.notion.so/intelligems/Visual-experience-builder-2ce2b3722092806a9a0fe30d434ac5a7)

**My Notion URL:** [https://www.notion.so/Visual-Experience-Builder-2ec94399495980b687d3f63c4d9e4849](https://www.notion.so/Visual-Experience-Builder-2ec94399495980b687d3f63c4d9e4849)

**Last Modified:** 2026-01-19 16:19:00 UTC

<hr>

## OKR(s)

**Core Experiences Pillar Objective: **Remove friction in the highest volume experiences so customers effortlessly understand and achieve value.



This work will directly impact our KR to **decrease on-site editor problems from ~120 mentions/month to 60**, and support **improved experience launch success rates** by eliminating reliability issues that prevent merchants from confidently setting up and publishing tests.



---

## Problem

Merchants can't trust our onsite editor to load regularly, reliably save changes, apply edits consistently across different themes and devices, or preview experiences. This forces them to either abandon visual editing entirely or burn hours troubleshooting with support.

The current editor fails across several critical interactions:

**Editor is slow and inconsistent to load.** The editor loads slowly, feels clunky, and provides unclear feedback about what can be edited.

> "I find the editor overall to be like pretty jumpy and just overall like a little bit clunky for lack of a better term."

> "Yeah, for me, it is really delayed. And so I find that very challenging when I'm trying to make edits on something, you know, a little impatient or I don't know if it like made the change or whatnot. that I find challenging."

> “I'm trying to do a content test (Early Bird vs Holiday Test) but the onsite editor is not showing up when I click the button. It just loads my page without any editor visible. Can you help please?”



**Edits don't save.** Work disappears when switching modes or saving, forcing merchants to redo changes or question whether they were captured.

> "when we are building tests...you make a change And sometimes it doesn't come up...the widget said all those changes because you're in the you've gone through the preview method so i haven't been able to save the changes...a couple of times we've just like lost the changes that we've done"

> "when he is in the preview mode, he makes changes, then goes back to edit the experience, and the content he changed is gone."



**Preview is unreliable.** Changes don't appear correctly or at all, creating a mismatch between what merchants build and what they expect to test.

> "The changes were not showing and I could not make any edits anymore the preview editor is not working"

> "hey guys - is the onsite editor experiencing any bugs? super slow for me - and my edits are not showing in the preview?"



**Can't target the right elements.** Merchants struggle to select specific elements, especially with nested or dynamic content. Elements become uneditable without explanation.

> "Merchant is struggling to target a specific element. There are two elements, one nested in another, and they can't get the inner element to be targeted."

> "it is really delayed...I find that very challenging when I'm trying to make edits on something...Targeting is challenging sometimes with specific elements of the site."



**Images don't work properly.** The option to replace images sometimes doesn't appear, and when it does, images render with incorrect styling or alignment.

> "When I right-click on the main product image / component, Intelligem correctly shows the 'Edit image' option...On this page, when I right-click on the same area, the 'Edit image' option is missing."

> "The new image loads, but its positioning/display is not optimal, it appears misaligned or not centered compared to the original. Is there a way to adjust how the replacement image is rendered."



**Mobile and desktop inconsistency.** Changes don't apply consistently across devices. Merchants can't reliably create device-specific variations.

> "I'm trying to simply hide an element on the mobile PDP but I'm unable to edit content from a mobile view"

> "sometimes I think I've targeted an element of our site and made the change and recognize that the element is named differently or like something different about it on each device. So I'm always doing it on desktop...I feel like I get there very quickly on desktop. And then all of a sudden I realize it's not applicable to mobile."



---

## Opportunity

When merchants can reliably create and preview content changes, they'll run more visual tests with confidence. This reduces support burden, accelerates test setup, and increases the volume of active tests per customer, directly impacting retention and expansion as customers see more value from the product.

A reliable visual editor also becomes the foundation for the broader experience building workflow and future agentic capabilities. This positions us to deliver on the strategic vision of making sophisticated optimization accessible without requiring significant merchant investment in time and effort, whether they're building experiences manually or having AI build them.

---

## Proposed Solution & Scope

Replace the current onsite editor with an embedded site editing experience built on reliable iframe-based rendering. Merchants will be able to view their site within Intelligems, toggle between pages and devices, and make content changes (hide/show elements, replace text and images, edit HTML/CSS) that preview and save consistently.

The core flow: merchants navigate to create or edit an experience, open the visual editor, select elements directly on their rendered site, make changes, and see those changes reflected immediately and reliably in preview before publishing.

**MVP capabilities:**

- View merchant's site embedded in Intelligems with toggle between home, collection, and product pages
- Toggle between mobile and desktop views
- Hide/show elements
- Replace text and images
- HTML/CSS editing
**Out of scope:**

- New editing capabilities beyond current onsite editor functionality
- Components, offers, and checkout integration with visual editor
- Agentic experience building
- Holistic experience creation flow improvements
- Headless storefront support
This MVP establishes the foundation for future expansion into components, agentic building, and consolidated experience creation—but focuses first on eliminating the reliability issues that prevent merchants from using visual editing with confidence today.



---

## Why now?

Editor issues are a top driver of support volume and merchant frustration. Every day we wait, merchants lose confidence in test setup, limit their testing, or churn entirely. The current technical debt makes incremental fixes unsustainable—we need a foundational reset.

This work is also critical infrastructure for our strategic direction. We can't deliver on the AI-powered experience building vision if the core editing experience is broken. Building this right now sets us up to expand into the full experience workflow later.

If we don't do this now, we continue bleeding support capacity, limiting merchant adoption of visual testing, and delaying progress on strategic initiatives that depend on reliable editing.

---

## Metrics

**Success:**

- 50% reduction in editor-related support tickets
- Increase in successful experience creation rate (experiences created → published → left running beyond 1 week)
- Reduction in time from experience creation to publish
**Failure:**

- Support tickets remain flat or increase
- Merchants report similar reliability issues with the new editor
- Experience creation rate doesn't improve
**Counter-metrics:**

- Time to create an experience doesn't increase significantly
- No decrease in overall experience creation volume during transition
---
