import os
import streamlit as st
from groq import Groq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document as LangchainDocument
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import pandas as pd
from dotenv import load_dotenv
import base64

load_dotenv()

st.set_page_config(page_title="Cricbot Pro 🏏", layout="centered")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


bat_base64 = get_base64_image("bat.png")
ball_base64 = get_base64_image("ball.png")


st.markdown(f"""
    <style>
        @keyframes moveBat {{
            0% {{ left: -100px; opacity: 0; }}
            50% {{ left: 450px; opacity: 1; }}
            60% {{ left: 450px; transform: rotate(0deg); }}
            65% {{ left: 450px; transform: rotate(-20deg); }}
            70% {{ left: 450px; transform: rotate(-40deg); }}
            75% {{ left: 450px; transform: rotate(-20deg); }}
            80% {{ left: 450px; transform: rotate(0deg); }}
            100% {{ opacity: 0; }}
        }}

        @keyframes moveBall {{
            0% {{ right: -100px; opacity: 0; transform: translateY(0); }}
            40% {{ right: 450px; opacity: 1; transform: translateY(0px); }}
            50% {{ right: 440px; opacity: 1; transform: translateY(0); }}
            60% {{ right: 475px; opacity: 1; transform: translateY(0px); }}
            65% {{ right: 470px; opacity: 1; transform: translateY(0); }}
            70% {{ right: 470px; opacity: 1; transform: translateY(0); }}
            75% {{ right: 350px; opacity: 1; transform: translateY(-100px); }}
            80% {{ right: 300px; opacity: 1; transform: translateY(-150px); }}
            90% {{ right: 200px; opacity: 1; transform: translateY(-200px); }}
            95% {{ right: 150px; opacity: 1; transform: translateY(-250px); }}
            100% {{ right: 50px; opacity: 0; transform: translateY(-280px); }}
        }}

        @keyframes blastEffect {{
            0% {{ transform: scale(0); opacity: 0; }}
            50% {{ transform: scale(1.5); opacity: 1; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}

        .container {{
            position: relative;
            height: 50vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}

        .bat {{
            transform: scale(1.2);
            position: absolute;
            left: -100px;
            opacity: 0;
            width: 100px;  /* Adjust the size */
            height: auto;
            animation: moveBat 2s ease-in-out forwards;
        }}

        .ball {{
            position: absolute;
            right: -100px;
            opacity: 0;
            width: 50px;  /* Adjust the size */
            height: auto;
            animation: moveBall 2s ease-in-out forwards;
        }}

        .blast {{
            position: absolute;
            font-size: 70px;
            font-weight: bold;
            opacity: 0;
            animation: blastEffect 1s ease-in-out 2s forwards;
        }}

        .subtitle {{
            position: absolute;
            font-size: 20px;
            font-weight: normal;
            opacity: 0;
            animation: blastEffect 1s ease-in-out 2.5s forwards;
        }}

    </style>

    <div class="container">
        <img src="data:image/png;base64,{bat_base64}" class="bat" />
        <img src="data:image/png;base64,{ball_base64}" class="ball" />
        <div class="blast">CricBot</div>
    </div>
""", unsafe_allow_html=True)

st.markdown(
    "<h3 style='text-align: center;'>Smashing Your Cricket Queries Like a Pro! 💥</h3>", 
    unsafe_allow_html=True
)

# Set API keys
api_key = os.getenv("GROQ_API_KEY")
scrapingbee_key = os.getenv("SCRAPINGBEE_API_KEY")

# Initialize clients
client = Groq(api_key=api_key)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Configure headless browser for dynamic content
chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)

def scrape_cricinfo(player_name):
    """Scrape player data from ESPN Cricinfo using Selenium"""
    try:
        driver.get(f"https://www.espncricinfo.com/search?q={player_name}")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ds-p-4"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract key player stats
        stats = {
            'batting_avg': soup.find('div', {'title': 'Batting average'}).text,
            'runs': soup.find('div', {'title': 'Runs scored'}).text,
            'wickets': soup.find('div', {'title': 'Wickets taken'}).text,
            'recent_performance': [m.text for m in soup.select('.ds-text-compact-xs')[:5]]
        }
        return str(stats)
    
    except Exception as e:
        return f"Error scraping Cricinfo: {str(e)}"

def scrape_howstat(query):
    """Scrape structured data from HowStat using ScrapingBee"""
    try:
        response = requests.get(
            "https://app.scrapingbee.com/api/v1/",
            params={
                'api_key': scrapingbee_key,
                'url': f'http://www.howstat.com/cricket/Statistics/Players/{query}',
                'extract_rules': {
                    'batting_stats': 'table#battingGrid td',
                    'bowling_stats': 'table#bowlingGrid td'
                }
            }
        )
        return response.json()
    except Exception as e:
        return f"Error scraping HowStat: {str(e)}"

def update_knowledge_base(query):
    """Dynamic web scraping and vector store update"""
    try:
        # Scrape multiple sources
        cricinfo_data = scrape_cricinfo(query)
        howstat_data = scrape_howstat(query)
        
        # Create documents
        docs = [
            LangchainDocument(page_content=f"Cricinfo Data: {cricinfo_data}"),
            LangchainDocument(page_content=f"HowStat Data: {howstat_data}")
        ]
        
        # Update vector store
        splits = text_splitter.split_documents(docs)
        global db
        db = FAISS.from_documents(splits, embeddings)
        db.save_local("faiss_index")
        
        return True
    except Exception as e:
        st.error(f"Knowledge update failed: {str(e)}")
        return False

def enhanced_retrieval(query):
    """Enhanced retrieval with dynamic data fetching"""
    try:
        # First attempt with existing knowledge
        retrieved_docs = db.similarity_search(query, k=3)
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        
        # If insufficient context, fetch new data
        if len(context) < 500:
            if update_knowledge_base(query):
                retrieved_docs = db.similarity_search(query, k=3)
                context = "\n".join([doc.page_content for doc in retrieved_docs])
        
        return context
    except Exception as e:
        return f"Retrieval error: {str(e)}"

# Initialize vector store
if not os.path.exists("faiss_index"):
    db = FAISS.from_texts(["Initial cricket knowledge"], embeddings)
else:
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# Streamlit UI
st.title("Cricbot Pro 🏏")
user_input = st.text_input("Ask about any player, match, or statistic:")

if user_input:
    with st.spinner("Fetching latest cricket data..."):
        context = enhanced_retrieval(user_input)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"Cricket Question: {user_input}\n\nContext: {context}"
            }],
            temperature=0.7,
            max_tokens=500
        )
        
        st.write(response.choices[0].message.content)
        st.success("Data sources: ESPN Cricinfo & HowStat")