# what-reddit-thinks
This is a simple web app for analyzing reddit threads using an LLM.

# how it works
* The user enters the URL to a Reddit thread into the web interface.
* Using the PRAW Reddit API client, the application fetches the Reddit thread, traverses the comment tree, and extracts all comments.
* The extracted comments are combined with an instructional prompt and sent to an LLM through the OpenAI client.
* The user receives feedback from the LLM on screen - a structured analysis of the recurring themes within the thread.

