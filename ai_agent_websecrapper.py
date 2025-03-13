# Import the required libraries
import streamlit as st
import asyncio
import sys
from scrapegraphai.graphs import SmartScraperGraph

# Fix asyncio event loop issue on Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Set up the Streamlit app
st.title("Web Scraping AI Agent 🕵️‍♂️")
st.caption("This app allows you to scrape a website using OpenAI API")

# Get OpenAI API key from user
openai_access_token = st.text_input("OpenAI API Key", type="password")

if openai_access_token:
    model = st.radio(
        "Select the model",
        ["gpt-3.5-turbo", "gpt-4"],
        index=0,
    )    

    graph_config = {
        "llm": {
            "api_key": openai_access_token,
            "model": model,
        },
    }

    # Get the URL of the website to scrape
    url = st.text_input("Enter the URL of the website you want to scrape")

    # Get the user prompt
    user_prompt = st.text_input("What do you want the AI agent to scrape from the website?")

    # Function to run scraping asynchronously
    async def scrape():
        smart_scraper_graph = SmartScraperGraph(
            prompt=user_prompt,
            source=url,
            config=graph_config
        )
        return await smart_scraper_graph.run()

    # Scrape the website when the button is clicked
    if st.button("Scrape"):
        if url and user_prompt:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(scrape())
            st.write(result)
        else:
            st.warning("Please enter a URL and a prompt before scraping.")
