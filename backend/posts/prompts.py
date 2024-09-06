tag_post_prompt = f"""
You are a social media expert. Based on post content you MUST set a appropriate tags for the post. 


It should be thematical tag by topic. Example of topics:
- Artificial Intelligence
- Software Development
- Sport 
- Travel
- Food
- Music
- Books
- Careers
- Education
- Marketing
- Science
- Design
- Business
- Dating
- Politics
- Health
- Sport
- Lifestyle
- Gaming
- LLM

Or you have ability to create new topic by yourself. Be be aware to create it as general as possible. So it won't be too specific.


Output format: 
- User input: The first ultra high definition 3D scan AI database for games, film and VFX industries
- Output: Artificial Intelligence, Gaming, Design

- User input: Llama 3.1 and Groq - Edit Code Directly in VSCode. With CodeGPT Inline Edit Code feature, you can select AI at Meta Llama 3.1 model and ask it to make changes to your code. 
- Output: Artificial Intelligence, Software Development, LLM


Each post can only have maximum 3 tags. NOT MORE. ONLY 3 TAGS.

NEVER write Output: Category. Write only tags ONLY with comma separator.
"""


summary_posts_prompt = """
Your main goal is preapre great well structured summary of posts grouped by meaning. 


You will receive list of posts and you need based on meaning group them and provide summary. 

For each post you will have also ID which you need to end at the end of each groups. 


Example of input:
[
  {
    "id": "1829344168356757697",
    "url": "https://twitter.com/korzhov_dm/status/1829344168356757697#m",
    "date": "2024-08-30",
    "tags": "",
    "text": "WTF, why is X API so expensive?   Even to pull tweets you have to pay for it. Doesn't make any sense...",
    "title": "DiKo Tweet"
  },
  {
    "id": "1828836042516115917",
    "url": "https://twitter.com/korzhov_dm/status/1828836042516115917#m",
    "date": "2024-08-28",
    "tags": "",
    "text": "Share Trips — share and create trips (ofc with AI features). User rights, google auth and full onboarding flow for user.  https://github.com/diko0071/share_trips",
    "title": "DiKo Tweet"
  },
  {
    "id": "1828835838115090589",
    "url": "https://twitter.com/korzhov_dm/status/1828835838115090589#m",
    "date": "2024-08-28",
    "tags": "",
    "text": "AI-powered personal finance tracker (I use it for myself though). AI chat, AI add, dashboard and recurring transaction tracker.   https://github.com/diko0071/walletwave_backend",
    "title": "DiKo Tweet"
  },
  {
    "id": "1828835531821900196",
    "url": "https://twitter.com/korzhov_dm/status/1828835531821900196#m",
    "date": "2024-08-28",
    "tags": "",
    "text": "@ouraring extension that brings really useful insights.  https://github.com/diko0071/oura_ai",
    "title": "DiKo Tweet"
  },
  {
    "id": "1828835210332615123",
    "url": "https://twitter.com/korzhov_dm/status/1828835210332615123#m",
    "date": "2024-08-28",
    "tags": "",
    "text": "Since the biggest hype around @cursor_ai, I started to use it 4 month ago.  But there is big shout out for @vercel  and @v0.   I have built 3 full-stack projects from scratch, deployed and open-sourced them.   So, now I can claim that I'm Senior Cursor Engineer :)  Links 👇",
    "title": "DiKo Tweet"
  }
]

Example of output:
```
- AI-Powered Projects: Dmitry shared a series of projects utilizing AI, including a trip-sharing platform, a personal finance tracker, and an extension for Oura Ring insights. [1828836042516115917, 1828835838115090589, 1828835531821900196]

- Frustration with Pricing of APIs: Expressing frustration over the high cost of accessing X API for pulling tweets, questioning the reasoning behind it. [1829344168356757697]

- Projects Built and Deployed with Cursor.ai and Vercel: A reflection on using Cursor.ai and Vercel for building three full-stack projects, highlighting the benefits of these platforms and proudly claiming the title of “Senior Cursor Engineer.” [1828835210332615123]
```

MAIN RULE:
Format REQUIRED: `Group Name: Summary. [id of posts (JUST IDs)]`


NEVER BREAK THIS RULES. NEVER add anything else. ONLY USE THIS FORMAT.
"""