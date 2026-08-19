# what-reddit-thinks
This is a simple web app for analyzing reddit threads using an LLM.

# how it works
* The user enters the link to a reddit thread into the web interface.
* The comments from the thread get parsed, extracted, bundled with an instructional prompt and sent via an API call to an LLM.
* The user receives feedback from the LLM on screen - a structured analysis of the recurring themes within the thread.

