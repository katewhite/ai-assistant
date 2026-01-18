# Product Strategy Briefing (Feb '20)

<aside>
â„¹ï¸

*Written by Brian Thomas*

</aside>

## **Intention: Send every message our customers need to deliver**

Feb 2020

# **Context**

Over the company's history, the strength of competitors like MailChimp and Intercom caused us to lean in to making our offering more sophisticated by embracing advanced use-cases like multi-step workflows. Weâ€™ve become exceptionally good at these complex messaging flows. Last year our work on the UI, workflow builder, and branching took us to a new level of making more sophisticated customer flows easier to create, understand, and manage.

This focus on going deeper has left gaps that prevent us from being adopted for all the messages our customers need to send. We have never gone back to strengthen our offering for simple, common use-cases, such as transactional messages and leads, which often require a surprisingly large amount of effort in Customer.io.

# Higher **Intent**

Fix the gaps preventing companies from using us to send all messages to their audience (in-app and out) and make CIO a platform early stage startups prefer to start with on day one of their business.

# **My Intent**

As a Product team, weâ€™ll focus on filling the gaps that prevent customers from sending every message they need to deliver through us. Weâ€™ll do this by first organizing our squads to achieve three complementary outcomes:

1. Gain adoption for all transactional messaging use cases
2. Get customers serving their whole audience, not just their web/mobile app users
3. Increase â€œconsolidation valueâ€, the value that customers unlock once theyâ€™ve switched more of their messaging to us

We also have 1350 and growing customers to support. We'll continue to staff Buzzard with roughly a quarter of our total capacity to help us keep up with usability improvements, bugs, and small improvements for existing functionality.

### Why?

I define these product "gaps" as the messaging use cases requiring a large number of steps (or a technical investment) for customer adoption. The gaps we'll focus on are those most likely to increase the share of customer messages we deliver. There are many opportunities to increase this share, but these three have the strongest potential:

1. We should start with transactional messages because these are the simplest use cases for our customers to adopt first and are closest to our core of sending automated messages people like to receive.
2. We should look at the customer's whole audience now because itâ€™s by far where we hear the most feedback from both prospects and existing customers. Itâ€™s near universal among our customers to send messages to their audience before they become app users, and the recommendations we make (e.g. multiple workspaces) are particularly high effort and often untenable.
3. We should invest to increase consolidation value so we have a strong pitch for why our customers should spend the time required to move additional message types to us. There are many customer challenges that we can only solved when messaging isn't divided across many platforms.

There are other opportunities with strong potential to increase messaging share that are important, but we have limited bandwidth so we'll need to tackle them next:

- Gaining more SMS and Push message adoption. I believe this should be our the next step after transactional as they're channels we already support
- Supporting In-App messages directly rather than asking customers to use webhooks. The lack of a more integrated solution means that customer need to invest an inordinate amount of time to send messages directly to their app.
- Improving the message creation and editing experience itself. There are many alternative tools, in particular those tailored to bulk messaging, that our customers continue use alongside us because common message creation and editing flows require too much effort. Examples of investments here could be a message library or a template-building language.

## Measures

**The outcome we want to achieve is for all customers to send all messages to their audience through us.**

In other words, we want to increase the average messaging share we handle for our customers. For example, weâ€™d have a 33% messaging share for a customer sending 100k monthly messages to leads via MailChimp and 50k monthly messages to app users via CIO.

It will be difficult to gather sufficient data to measure this precisely, but rough indicators are enough to drive our decision-making. We can use techniques such as surveys, MX records, and analytics data. Weâ€™ll start by establishing baselines using those tools.

Each squad will take on a more specific part of this outcome that contribute to closing the gaps that prevent us from reaching higher messaging share.

# **Instructions for the Squads**

## ðŸ¦† Figure out how to get adoption for all our customerâ€™s transactional messages

Hey LJ! Youâ€™ve done exceptional work on getting the self-service funnel in place, maintaining our conversion rates, and enabling our sales team to focus. Please continue your analysis of this funnel, but start handing off support to the TSE Team, wrapping up the tasks that will leave you confident about the current state of the funnel, and prepare the squad to transition to a new focus area.

Our bread and butter use cases are automated messages, and yet weâ€™ve underserved transactional messages. I suspect that people donâ€™t use us for transactional messages because theyâ€™ve built them in code before using CIO and the migration path to us is too hard. Figure out if thatâ€™s true and what we might be able to do to reduce that friction.

As you build the roadmap for your squad, I expect you to be exploring things like an SMTP endpoint, securing message contents (for cases like password reset), and a new api-triggered campaign type. You are likely to encounter cases where transactional messages are being sent to people who aren't yet stored as profiles, the id is unknown, and may need to be added. Be sure to collaborate closely with Brendan on this as he looks at id management solutions.

Itâ€™s important that we support transactional messages across all channels, but itâ€™s okay to prioritize email. For SMS and Push you may find that the reluctance to send transactional is because of weakness in our support for those channels - letâ€™s wait until later to improve those channels rather than including them in your roadmap now.

Keep in mind the onboarding tools youâ€™ve been building. Transactional messages should be one of the easiest first use cases to adopt. Look for ways of getting new customers sending faster in less time via the new tools you're building.

## ðŸ¦… Grow our offering to serve our customerâ€™s entire audience, not just their app users

Hey Brendan! I need you to figure out how we can get our customers sending to their whole audience. Every single customer we serve has an audience beyond their app users, and today we make it overly complicated to send messages to them.

Since you are actively managing the integration page, start focusing more on forms, landing pages, ads, and other sources where the user id isnâ€™t known yet. Talk to anyone requesting these and document their use cases. Is it sufficient that we donâ€™t have a first party solution for these cases? Or do we need to build our own?

Our lack of full audience support manifests with customers and prospects when theyâ€™re blocked by our id management constraints. Theyâ€™re looking to use email as id, migrate their id scheme, or use data other than id to identify a customer. Our sub-optimal solution is asking them to use multiple workspaces. Getting to the root of these highly requested needs is the best path I see to start learning how to accomplish this outcome.

I  expect you to evaluate the customerâ€™s mental model for keeping their audience and profile separate (yet overlapping) within a single workspace. While the data doesnâ€™t need to be split across workspaces, each group requires distinct messaging strategies.

You may end up overlapping with the transactional effort if that squad delivers an SMTP endpoint that can be used for people who may or may not be registered users. Keep this in mind and collaborate closely with LJ.

Itâ€™s important that we realize that every channel we send on manages non-app audiences in a slightly different way (e.g. device tokens for Push). Whatever solution we choose needs to be flexible enough to support our current channels and adapt as we add more.

## ðŸ¦‰ Increase the consolidation value of bringing many types of messages to us

Hey Kate! Your squad's work on improving branch conditions and improving our metrics has been essential for fully delivering on the promise of the branching workflow builder. While it does not directly connect to the messaging share outcome, I'd still like you to continue on this path a bit longer while limiting your focus to the things that will get the workspace and campaign dashboards to the next level.

The Campaign Dashboard today focuses primarily on email performance and is difficult to scan to get an understanding of whether a campaign is performing as expected. With contextual metrics, journey metrics, the ongoing date-filtering work, and Madeline's design proposals, all the tools are in place to finally replace the current dashboard.

The Workspace Dashboard today primarily shows raw message totals, but lacks meaningful insight into how a customer's messaging strategy is impacting their audience. Continue the progress you're making on tools like gathering segment membership over time and propose a new approach to summarizing overall activity.

Once you've delivered the dashboards, then it's time to align your squadâ€™s roadmap to the improvements that will most increase consolidation value and contribute to this strategy. There are tons of ways we create value through consolidation,  but we should start with the basics: things that require the most effort from customers that consolidation solves. Please explore this starting from customers problems - the examples I hear most frequently are: 

- Over-messaging: it's too difficult to understand and prevent situations where people might receive a lot of messages in too short a time period
- Consistently respecting unsubscribes + subscription preferences: it takes a lot of manual effort to make sure preferences are respected in all communications.
- Understanding the actions across all message types that contribute to conversions: to get a reasonable picture of this, customers usually need to export data to third party tools. They shouldn't need to do this for simple attribution cases where we already have all the message interaction data needed to provide better understanding.

## ðŸ¤¹â€â™‚ï¸ Design Team

Hey Madeline! Iâ€™m expecting you to own the design teamâ€™s alignment with this strategy briefing. Most importantly, I need you to continue driving the review and collaboration processes that ensures weâ€™re delivering a customer experience thatâ€™s unified and follows our design system across squads. Feel free to change the assignments of designers to squads where it helps us best achieve our goals.

I also need your help pushing the overall product team toward making usability improvements to help us accomplish our goals rather than over-relying on new features. We made a lot of progress last year by focusing a squad on refreshing our UI to implement the design system, but we havenâ€™t quite figured out how to make usability a bigger priority across everything we do.

I need you to complete the usability audit and use it as the launching point for maintaining a well organized backlog of usability projects ready for the squads and buzzard to implement. Iâ€™m looking for two categories in this list:

- Small usability and consistency issues defined well enough for us to deliver quickly in Buzzard. For example, fixing our Save Patterns.
- Bigger groups of usability issues that we can consider on squads. For example, the usability of our composers.

Where fixing usability issues will help achieve squad outcome, challenge the design team to advocate for items from this backlog with their PM counterparts. Deploy the usability audit tools to analyze the areas our squads are focused on and suggest improvements.

# **Boundaries**

## Freedoms

- Build out outcome-solution trees and pitch better ways of approaching these outcomes than Iâ€™ve suggested
- Challenge or validate my assumptions by collecting more data about which types of messages we arenâ€™t being adopted for.
- We can change PM and Design assignments to squads.
- Squads can change their names from birds to something descriptive of the outcomes you are trying to achieve. Remember that naming doesn't sign you up for every FR that contains that name.

## Constraints

- Donâ€™t fill messaging gaps unless we can show real examples where substitutes are being adopted or where consolidation was a blocker to adoption
- Donâ€™t force large features into Buzzard because it doesnâ€™t fit this strategy. Trade-offs are always rough and I wish we could do everything too!
- Weâ€™ll follow our product principles
- Stay focused on bulk and automated messages. We wonâ€™t stray into other communication types such as two-way chat.

# **Backbrief**

To keep us aligned on this strategy, I'm looking for documented squad plans in Notion as well as dashboards in Mixpanel or Mode for tracking our progress towards the outcomes we're working toward. I'd like each PM to create and finish reviewing a plan with the following format by March 13th:

Note that I don't expect a roadmap with high certainty and for all the investigation to be done in under two weeks. My primary goal is that you and I are aligned on intent and have a clear picture of what comes next. I realize that we have some self-serve and data pipeline work we're still committed to completing, and it's okay to exclude that from these plans.