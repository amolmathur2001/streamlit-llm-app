import os
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

from reviews import GoogleReviewsScrapper


st.title("📍🗣️ What :blue[Reviewers] Say? based on Latest Reviews")
st.caption("Did it ever happen to you, that Google Review Rating of a restaurant or that museum showed 4+ rating, but after going there you realized it was not worth it? Well, we summarize the latest Google Reviews of a place, which we consider a very relevant relevant signal, in a easy to read format for you.")
st.subheader(":blue[Hit search] before you go!")


# openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
# outscraper_api_key = st.sidebar.text_input("Outscraper API Key", type="password")

openai_api_key = os.environ["OPENAI_API_KEY"]
outscraper_api_key = os.environ["OUTSCRAPER_API_KEY"]

reviews_scraper = GoogleReviewsScrapper(outscraper_api_key)


def generate_response(review_info):
    model = ChatOpenAI(model_name='gpt-4o-mini', temperature=0.2, api_key=openai_api_key)

    messages = [("system", """You are ChatGPT, a helpful online assistant"""),
    ('human', f"""I am providing you with latest (sorted by time) google reviews of a a place. 
Today's date: 22nd Sep 2024

It has format:
name of place
number of reviews
date time rating review_text

Review Data:\n```{review_info}```

Now, your task is to provide a short summary for various parameters, deriving as much insights from the latest reviews as possible.

Basically, we want to have summary provide information that - "what are reviewers saying lately about this places's <...>". Give positive and negative aspects both. Be critical.

Output parameter:
<decide 5 most significant, concrete and unique parameters on your own. The parameters should tell about a specific aspect of the place. For example, in case of a restaurant, parameters can be food, ambience, parking, service etc.>


KEEP IN MIND:
- Do not output a 'overall' parameter.
- Rate the place on each parameter out of 5. This rating should be based on reviews (eg. if most reviews about parking are negative, give a low rating).
- Each parameter summary should not be more than 50 words.
""")]
    # st.info(model.invoke(input_text))
    output = model.invoke(messages)
    st.markdown(output.content)


def generate_review_info(search_query):
    reviews = reviews_scraper.get_latest_reviews(search_query)
    review_info = []
    for review in reviews:
      review_info.append(" ".join([str(review.time), str(review.rating), str(review.text)]))
    return "\n".join(review_info)


with st.form("my_form"):
    text = st.text_area(
        "Enter name of place and location:",
        "Rameshwaram Cafe, Indiranagar",
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    if submitted and openai_api_key.startswith("sk-"):
        with st.spinner('Fetching latest reviews...'):
          review_info = generate_review_info(text)
        with st.spinner('Generating a summary for you...'):
          generate_response(review_info)
