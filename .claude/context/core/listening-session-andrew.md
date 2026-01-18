Fall 2025

Andrew's Listening Session AI Vision Design Sprint.txt
25.03 KB •142 lines
•
Formatting may be inconsistent from source
>>Emily Brown	00:00
Charlie hates the car, the poor guy, he's like, the car makes him extremely scared, so feel bad about it, but he's going to love actually being there, you know? Is it worth it? Yeah. Yeah, I hope so. You can't ask him. How old is he? Charlie's three. Oh. Yeah. You would think that like a dog would get over this, but like, no, he somehow was like traumatized by the car as a puppy or something. Yeah, well.

>>Hannah Patterson	00:31
Can Charlie not get in the car?

>>Emily Brown	00:33
He hates the car, like he, it's like, gives him like panic attacks.

>>Hannah Patterson	00:37
Yeah. Yeah. And I'm a good driver.

>>Emily Brown	00:40
It's not like I'm a crazy driver or anything like that.

>>Hannah Patterson	00:47
He just has anxiety. Yeah.

>>Emily Brown	00:52
I mean, but of course I have a dog who has anxiety. It's like, it's just.

>>Hannah Patterson	00:57
My cousin's dog doesn't like getting in the car, but then like once he knows he's not going to the groomer or the vet, then he loves it. He needs to like know that that's not where they're going.

>>Angel Austin	01:11
Do dogs not have anxiety? Like is anyone not a dog without anxiety?

>>Hannah Patterson	01:20
Kimchi doesn't have a ton of anxiety, which is Christian's dog.

>>Angel Austin	01:25
That's amazing.

>>Hannah Patterson	01:26
He doesn't like when there's other dogs on TV. He does bark at them. But other than that, that's just a good bet. He also won't walk across a bridge, you know? Nevermind. I think he does have anxiety.

>>Emily Brown	01:42
Charlie doesn't like dogs on TV, but he really dislikes camels. It's like the one thing that he like notices and cares about.

>>Hannah Patterson	01:54
Isn't there a commercial for camels? I don't know. That would be bad.

>>Emily Brown	01:58
But we watched The Mummy over the weekend, and there are definitely camels in there, and he was not happy about it.

>>Hannah Patterson	02:04
That was a no.

>>Craig Phillips	02:09
All right. Hey, Andrew. Thanks for moving this last minute, everybody. Yeah, we swapped. I don't know if anybody noticed we swapped suit calls around. But yeah, thanks for moving it. Yeah, so Andrew, so we're doing the sessions. We've had five or so this week, trying to bring as many new inputs from across the business for us as we get into this design sprint. So some more customer -facing stuff, some more data -centric, looking at competitors, blah, blah, blah. So for you, there's probably a lot of different directions we could go chatting with you. The one thought was, because part of this work is to rethink our designing of tests and experiences, how that divide works, what sort of takes priority, all that kind of test experience type of discussion, and then a lot of early experience of using the product and creation flows. So with everything with Ai, that's kind of one thread I think would be really good to get your thoughts on. What is current vision, thinking, and where could we go with this, just so that we try to incorporate that into any designs that we are doing, that it's like designing in an AI -first reality that is not where we were a couple years ago. So that's a big thing, but also can be open to other things that feel relevant to you, and then obviously everybody can chime in with questions and thoughts. Does that sound relatively clear? Yeah.

>>Andrew Raftery	03:52
I can just start random thoughts that are coming to my head, but feel free to interrupt me, and I probably will say a bunch of things that you've heard before. So one thing that has always struck me as a problem that we have never really cracked is we push people to mechanisms, we organize the test creation process, but like, do you want to do a split URL test or a template test or a theme test? Which is not like, for content testing especially, it's just not, I think, how our customers think about it. They want to like, I want to test a landing page, or I want to test a product page, or I want to add something to my cart or whatever, and I think we don't meet them there. And so they have to, first of all, you can do any of those tests with any of those mechanisms. So then they get confused. I think if I were a new user, I would definitely be confused by that. So I think that's one thing. There's obviously lots of ways to solve that, but I think the problem is that we don't really highlight use cases in a great way, and we instead just show you the tools that you have.

>>Andrew Raftery	04:58
I think people get confused by the tools, not only because they might not know what the tools are, but also because even if they do know what they are, they overlap a lot and we don't really give them guidance on like when they should use one of the other. So that's something.

>>Emily Brown	05:12
I just watched a new install yesterday. She was clearly trying to set up some sort of Pdp test, but she like went to checkout blocks first as like a, as an attempt to do that. And I was like, no, why, why?

>>Andrew Raftery	05:26
Yeah, so that's the thing. I mean, I think also I, and then, so a separate piece of that just made me think of, so I used to understand the difference between, first we had campaigns and we had personalizations and it was like, okay, you can basically do anything with a personalization. It's sort of like a container for a bunch of modifications. You can also add offers, which are like things that we run at checkout. And we also, you know, we have volume discounts, all those kinds of things. And I have not been so close to that development recently. And so as I'm like seeing it in the information hierarchy and just sort of like checking things out, I actually have gotten to where now I'm really not sure where, what the difference between an experience and an offer is. So I mean, I think I probably could probably guess, but like, I sometimes am unsure. Do I tell a customer to do one or the other when I'm like helping them with something? So that's probably something we can clean up is like, what we, I don't know if that's in scope for this, but anyway, that's just something that I have, I feel like for customers actually could be clearer than it is for me. Like it might just be that I'm coming with some, you know, preconceived notions. I would have, the reason it's confusing for me is because I would have thought that an offer could contain an experience could contain an offer. And so that's something that I've been confused by recently, but I probably read some docs and figure it out regarding the Ai things, you brought that up. So a couple of thoughts. So one is, I think it could be a nice, I mean, again, I think that it shouldn't be the only solution, but it could be a way that we address this problem of like driving, like adjusting use cases, because, you know, if you came to the Ai assistant and it could, it probably wouldn't be that hard for an assistant to recommend a test type based on a use case in a way that might be harder to do, you know, with like a wizard blow.

>>Andrew Raftery	07:28
Although I think that like, I guess one theme that I would drive home with Ai is like, I don't think we should bet that it will just like work because like anything that we can do with Ai, I think we should still be able to do without it. We're not at a point yet where we can just like hang our hat on it and just say, it's gonna do everything. And that's true of like any software that I've used, like it could do some really cool magical things, but then you might find yourself frustrated because you can't get it all the way there, or it's misinterpreting this one thing. And if you could only do something through the Ai, that would be a really frustrating experience. So I think it has to be something that can be like, you know, I can like ask, maybe it's a chat experience. I can like ask it to do something for me And then it does something And then I can tweak it or I can start it and then ask it to finish it or something like that. I think it has to be collaborative. I don't think we're at a point where it's just gonna like one -shot It, even if it's something like, I mean, simple experiment setups, it probably could, but I still think like that's not probably a point where we're at with it yet. I mean, you know, a couple of years, I'm sure we'll get there But I still think people kind of like to be able to make changes. So that's a thought. I think going back to the use case thing, like that could be a nice solution for that as like, that's one path that we give a really good experience to our users to figure out how to address their use case. But I still think we would need a non -AI solution to that problem as well. In terms of how I would envision the Ai thing working, like, I mean, my mind just goes to like existing Ai products that I've used.

>>Andrew Raftery	09:09
So things that have like, you know, the co -pilot experience with a chat on the side and like, it's doing stuff for you and you can like make edits And it's aware of the edits you're making and you can like have a conversation about that. That's where my mind goes first, but that's probably just because that's what I've seen. I think if we go that route, as a user, I would want to be able to see like, when I ask it to do something and it's making changes, like one thing that I like about, like Claude does this in like the artifact thing that it has, like that panel that comes up. If you like ask it to change some code or something that's writing, it will like delete it. You can like see it get deleted and then it will like add it. And that's not because they need to do that. They do that because they want the user to see that they're deleting something, right? They could just re -pick, like what they get back from the model.

>>Andrew Raftery	09:57
Model is the new version. And then they could just paste it in. But instead of pasting it in, they show you that they're removing something and then adding something in. Sometimes it's actually kind of annoying how slow it is. But I think the user seeing the diff is kind of important. And that's actually, I think, one reason why some of the coding AI tools have been so successful is because the Ui and the semantics sort of already existed for how you overlay two changes on top of each other. So developers are really used to seeing the old version, the changes, and the new version. There's lots of software that visualizes diffs. And so it's kind of easy to work with text with an Llm because it's very easy to show you right in the context of your ID in a way that you're already used to using, like here's the difference. That doesn't exist for something like experiment setup in Intelligent. There's no existing paradigm for how we show a difference. When Rohan helps a customer change his experiment setup, what does he do? He goes in, he adds the experiment, he saves it, and he maybe writes a message about what he did. There's no existing way of saying, like, it used to look like this. We made these three changes, and now it's this. And that exists in other software. But anyway, I think it's most mature in software development, and it's very tech -heavy. And I think that's one reason why those products like Cursor have been very successful. So anyway, bringing something like that experience to our test setup, I think, would be ideal. I don't think it's necessary for Mvp. But as a user, being able to see, like, what did it do? I just feel like if it was like, I typed in something, hey, can you do this, this, and this? And it's like, OK, done. I don't know. That's not quite good enough for me. I feel like, do I trust that it actually did it?

>>Andrew Raftery	11:37
How do I know what it changed? Did it hallucinate something weird? Like, I would love to be able to see, these are the three things I changed without having to click through the menu and knowing where to go. One thing with regards to Ai that's, I think, interesting I've started noticing with the Ai chat and analytics is that people are asking questions that aren't necessarily related to analytics. People ask important questions. It has some connection to our docs. And it's like, we'll send people to support. But it occurs to me that if we put a chat window somewhere, people are going to use it for random stuff. So it's kind of interesting to think about. Like, if we have an experiment set up flow that has a co -pilot chat thing, what happens when they ask an unrelated support question? Or they ask it about some analytics thing. Or, hey, go copy, go look at this test set up. It's like, I think from the user perspective, they aren't thinking about it like there's an experiment set up chat agent flow. And there's an analytics chat agent flow. And there's a support chat agent flow. They're just thinking, I'm talking to Intelligems. So what does that mean and look like? And how can we make it work that people can kind of talk to it the way that they would talk to a member of our success or support team that has broad -ranging knowledge, rather than like, imagine we had the support agent, a support specialist, who only did experiment set up. And you ask them a question about anything else they can't help you, like a billing question. That would be a really bad experience. So Yeah, That's another random thought. I don't know, I've been talking for a while.

>>Andrew Raftery	13:20
I'll keep thinking. But if anyone has any questions or other things I haven't touched on, that's great.

>>Emily Brown	13:31
How have you seen the customer -based change with your interactions with customers as Intelligems has kind of changed the product offering as you've been here?

>>Andrew Raftery	13:44
Like what kinds of questions are different? Is that clear?

>>Emily Brown	13:46
Exactly, yeah. And who are you talking to? Like what kind of conversations are you having?

>>Andrew Raftery	13:54
So I think that the who I'm talking to hasn't changed that much. I guess a higher percentage of my customer touch points now are support -related than they used to be, because I used to do more like success and onboarding stuff. And so that's just the nature of, we have teams that are doing that, and that's better than I am. So most often, it's like I'm getting pulled into some support thing. But I don't know, I'm still. So anyway, that's like one thing that probably colors some of my seeing customers, but I also just like in most customer Slack channels and just like lurking. The size of customer and stuff, I mean, hasn't changed. I would say like that stuff hasn't changed that much because like the customers that we are talking to like in Slack and whatever, they're generally like a little bit on the larger side, less self -serve, more like getting success and support.

>>Andrew Raftery	14:56
Um, so yeah, I don't, I don't feel like it's actually changed all that much. There's, I guess what I'm saying. Um, we have a lot more agencies now than we used to. Um, a few years ago we've worked with very few agencies and we do like on a one -off basis. Now we have like lots of agency partners that we're talking to all the time. Um, so yeah.

>>Craig Phillips	15:25
Um, I think, yeah, I'm curious on the Ai side. I think, I think you've already given a good, a good framing of, of things. Um, I'd be curious if, if you have any thoughts on like what, either what would be like, if there could be one impactful thing in like test creation, like I guess from the very beginning of like, yeah, I want to create a test through to the completion of it. Like, is there a core that you feel is like the most impactful? And then on the flip side, is there something that maybe is like definitely not impactful based on your understanding? Like something that might be a waste of effort to like really think about AI for this. I'd be curious if anything comes to mind.

>>Andrew Raftery	16:13
Yeah. Um, I mean, I think where, where there are like existing good solutions today, we should lean on those. So like, I mean, my mind first goes to analytics, like, you know, instead of pasting a list of numbers in the chat, you PC and asking for the average, like we should just Excel for that. Like, I don't know if you guys are on that Halloween thing yesterday, but like drew is like copied the list of numbers into chat, Gpt that everyone was guessing for the number of candy corn and like asked it for the median and the average or whatever. And Jared did it in Excel and in less time, Jerry got the right answer and drew got the wrong answer. Uh, uh, so, you know, stuff like that. I mean, I think, um, I have also noticed people asking, cause I've been reading all those analytics chat logs, which are kind of interesting. If you guys ever check that out, there's a channel and you can kind of see like what's on people's mind. First of all, 90 % of the questions are, is my test at stats day or not? And when will it be? Um, but, uh, we get, there are also questions like, why did this, this is like kind of weird, why did it happen? And it's, and there are questions like that. You can ask about analytics where it's like, we can dig into the details. And then actually the chat bot did kind of a nice job of doing that. And then it got to a point where it was like, how could we know? Like, there's no good way. It's not like an Oracle. It's not like a, it's not like a, you know, magic eight ball. It was asking like, you know, it made a change And it caused more people to add to cart and fewer people to complete checkout or whatever. And it was like, well, maybe, you know, people were adding more enticed to add to cart, but they weren't such serious purchasers that they were actually going to check out. So it didn't really have an impact on conversion rate. And it was like, but why? It's like, you know, um, so I think sometimes people's, um, expectations are too high.

>>Andrew Raftery	17:58
Um, for like experiment sort of set up in creation and that kind of thing, I think. Um, we definitely have a gap today where using our tools that are not like template testing, like, so the onsite edits to do anything non -trivial really does require like a little bit of knowledge around HTML and Css and like dealing with some jankiness and like sometimes writing JavaScript code. And it's like, if you're a developer, it's pretty easy. Most, almost all of our users are not developers. And so like, that's a big point of, I mean, that's a point of improvement, I think, or, um, not just Ai, like if Ai didn't exist, we could make huge improvements in that anyway, but it's also an area where like the Ai is actually quite good at writing code. And so maybe it could help with that. And so that's a, you know, a situation where I could see, I think the challenge I see with that, with that, because I think that's like a no brainer is like, why don't we have the Ai create anytime we need to write custom JavaScript or Css or Html, why don't we just have the Ai do it for our customers? That would be amazing. But I go back to this idea of like, we still need people to be able to edit things. So like if the Ai were to just like write the code and create your custom add to cart widget or whatever, that would be great. Um, but then what if you want to change the color or what if you, what if the copy was wrong or you want to like bold some text or move it around on the page? I like, I don't think it's good enough to just have something that does a pretty good job of writing the Ai, writing the code for you. I do think we need a usable, uh, like editor experience.

>>Andrew Raftery	19:40
Um, and I don't think the Ai can be successful alone. So, um, so Yeah, That's a situation where it's like, I think it's a great, it's a great impactful use case for the Ai, but given what we have today, I'm not sure if you just plugged it in, it would really make a big impact.

>>Andrew Raftery	19:55
You kind of do need this experience. I think, unlike a person, if we had a person who was just creating experiences for customers, designing it for them, building it for them, testing it for them, we can be pretty confident that it's going to do a good job 99 % of the time. And that would probably be successful. It'd be expensive and successful. That 99 % for an Ai might be 90 % or maybe 85%. And that's just too low. The bar is 99%. And so if it can't one -shot it 99 % of the Time, then you need to be able to have the user go back and forth and edit things and have a nice preview experience. And I don't foresee a situation where we're getting to 99 % in the next year, just with where these tools are. So Yeah, That's another thought. I don't know if I answered your question.

>>Craig Phillips	20:46
Yeah, no, for sure. For sure. One more question from my side. So one of the kind of big questions we're wrestling with here, and it's a conversation that's come up quite a bit, but it's this sort of intelligence as a testing first sort of a product or platform, sort of more of an experience first type of platform, or kind of more like what it is today, where it's like we have testing, we have experiences that kind of sit next to each other. And those are three kind of, I guess, realities that we could embody. And there's been a lot of obviously back and forth conversations about these. We never really get to a resolution. I'm curious what your take on that sort of question is.

>>Andrew Raftery	21:32
Just to make sure I understand. So it's like, how do we unify experiences?

>>Craig Phillips	21:41
Yeah, do we unify? Do we keep it as like, these are separate things that we offer? We offer experiences, personalizations, and we offer tests, or like, we are a testing tool, you come here to test. And yet, we have experience functionality, but we are a testing tool, or we're an experience functionality that also has the ability to test things, you know?

>>Andrew Raftery	22:00
Yep, yep, yep, yep. It's interesting. Yeah, I mean, I think, so you guys I'm sure have all seen visually, they like really lean into the experiences first approach. People still, I think, think of them as some kind of testing tool. And that's how they talk about themselves a lot. But I think, like, one big advantage of leading with experiences is maybe there's some stickiness there, like we can get people to use components of ours and things like that, whether it's like the offers and the quantity buttons and all kind of stuff, and like, keep them around more, and think about intelligence and something like that you do. And rather than you test something once, then you rip it out and you go and, but I would question whether we have enough of those things today to make that successful. Because I don't, what I would, if I were a user, what I would expect a tool like that to have is like a component library, where I'm adding things in, maybe it has its own cart. Checkout blocks is an example of something that we do now have, but we probably need to add more of to make it like a broader offering. So I worry that if we like really lean into experiences first, that that will fall flat. And instead of being the best testing tool, we're like a mediocre experiences tool in people's minds. So that, that's an anxiety that I would have about that. But if we can, if we say, okay, this is a longer term vision, we can shore up those deficiencies if we believe they exist. Like let's assume we're at that point where we have like feature parity with all the, some of the visually, not that those are like amazing, but you know, they have like a component library, shoplift has one, maybe rebuy as an example.

>>Andrew Raftery	23:46
Maybe we have like an onsite editor experience or like an in -app editor experience with Ai that's, that's good. And you can create components and things like that. Then I think it's much more compelling. I think I do buy some of this like retention, the retention aspect of it. If there is a, if there is a strong builder experience in the app where I can like build a new component and it's in Intelligems and managed by Intelligems for me, and it gets like put in different places on my site. Then, and we're like a little bit more towards like a page builder idea. Then I think I, then I do see it. And it's like, that's a hard thing to turn off. I just feel like we're far from that today. And so like, and so for where we are today, playing to our strengths, leading with experiments feels like safer. That's the first thing that comes to mind. I also, I wonder whether we can, could we be both like, is there a way if we keep it separate, can we still make it feel unified and clear to users? Because maybe, maybe there's a way we can get some of the

>>Andrew Raftery	24:54
Of the good parts of leading with the experiences. And I mean, it's where I think I'm sure you guys have thought about this way more than I have, like what those things are. Like I mentioned the retention thing, there's probably other things. Get some of those good things without having to like, really overhaul what it is the way we talk about ourselves. So yeah, it feels a little risky to me.

>>Craig Phillips	25:22
Yeah, cool. Awesome. Okay, we've got a few minutes left. Anybody else have thoughts, questions, anything else? No? Okay. Well, Andrew, thanks for taking the time and jumping on and sharing your thoughts.

>>Andrew Raftery	25:47
Yeah, I'm excited to see some stuff at the onsite.

>>Craig Phillips	25:51
So yeah, we could make some progress next week. So Yeah,

>>Andrew Raftery	25:55
I'm sure. All right.

>>Craig Phillips	25:56
Cool, all right. Bye. You too, bye.