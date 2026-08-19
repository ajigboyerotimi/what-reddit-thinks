import os
import streamlit as st
import praw
from openai import OpenAI
from streamlit_gtag import st_gtag

# --------------------------------------------------
# GOOGLE ANALYTICS
# --------------------------------------------------

st_gtag(
    key="ga_pageview",
    id="G-Q59C5H554Q",
    event_name="page_view"
)

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

REDDIT_CLIENT_ID = os.environ["REDDIT_CLIENT_ID"]

REDDIT_CLIENT_SECRET = os.environ["REDDIT_CLIENT_SECRET"]

REDDIT_USER_AGENT = os.environ["REDDIT_USER_AGENT"]

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="What Reddit Thinks",
    page_icon="wrt.png",
    layout="centered"
)

# --------------------------------------------------
# CLIENTS
# --------------------------------------------------

client = OpenAI(
    api_key=OPENAI_API_KEY
)

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# --------------------------------------------------
# LOAD SYSTEM PROMPT
# --------------------------------------------------

with open(
    "Reddit.txt",
    "r",
    encoding="utf-8"
) as file:

    system_message = file.read()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    st.image(
        "wrt.png",
        width=250
    )

st.write("Understand thousands of Reddit comments in seconds.")

# --------------------------------------------------
# INPUT
# --------------------------------------------------

url = st.text_input(
    "Paste Reddit URL"
)

# --------------------------------------------------
# ANALYZE
# --------------------------------------------------

if st.button("Analyze"):

    # Track analysis usage
    st_gtag(
        key="analysis_started",
        id="G-Q59C5H554Q",
        event_name="analysis_started"
    )

    if not url:

        st.error(
            "Please enter a Reddit URL."
        )

    else:

        try:

            with st.spinner(
                "Extracting Reddit comments..."
            ):

                submission = reddit.submission(
                    url=url
                )

                submission.comments.replace_more(
                    limit=0
                )

                comments = []

                for comment in submission.comments:

                    if comment.body:

                        comments.append(
                            comment.body
                        )

            st.success(
                f"Found {len(comments)} comments"
            )

            st.subheader(
                submission.title
            )

            combined_comments = "\n".join(
                comments
            )

            with st.spinner(
                "Analyzing discussion..."
            ):

                response = (
                    client.chat.completions.create(
                        model="gpt-5.4-nano",
                        messages=[
                            {
                                "role": "system",
                                "content": system_message
                            },
                            {
                                "role": "user",
                                "content": combined_comments
                            }
                        ]
                    )
                )

                analysis = (
                    response
                    .choices[0]
                    .message
                    .content
                )

            st.divider()

            st.markdown(
                analysis
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )
