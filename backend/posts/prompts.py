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