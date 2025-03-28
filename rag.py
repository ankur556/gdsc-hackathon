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

import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bat_base64 = get_base64_image("bat.png")
ball_base64 = get_base64_image("ball.png")
logo_base64 = get_base64_image("logo.png")
blastl_base64 = get_base64_image("blastl.png")
blastr_base64 = get_base64_image("blastr.png")

st.markdown(f"""
    <style>
        @keyframes moveBat {{
            0% {{ left: -100px; opacity: 0; }}
            50% {{ left: 50px; opacity: 1; }}
            60% {{ left: 50px; transform: rotate(0deg); }}
            65% {{ left: 50px; transform: rotate(-20deg); }}
            70% {{ left: 50px; transform: rotate(-40deg); }}
            75% {{ left: 50px; transform: rotate(-20deg); }}
            80% {{ left: 50px; transform: rotate(0deg); }}
            100% {{ opacity: 0; }}
        }}

        @keyframes moveBall {{
            0% {{ right: -100px; opacity: 0; transform: translateY(40px); }}
            40% {{ right: 450px; opacity: 1; transform: translateY(40px); }}
            50% {{ right: 440px; opacity: 1; transform: translateY(40px); }}
            60% {{ right: 430px; opacity: 1; transform: translateY(40px); }}
            65% {{ right: 430px; opacity: 1; transform: translateY(40px); }}
            70% {{ right: 430px; opacity: 1; transform: translateY(40px); }}
            75% {{ right: 350px; opacity: 1; transform: translateY(-100px); }}
            80% {{ right: 300px; opacity: 1; transform: translateY(-150px); }}
            90% {{ right: 200px; opacity: 1; transform: translateY(-200px); }}
            95% {{ right: 150px; opacity: 1; transform: translateY(-250px); }}
            100% {{ right: 50px; opacity: 0; transform: translateY(-300px); }}
        }}

        @keyframes blastEffect {{
            0% {{ transform: scale(0); opacity: 0; }}
            50% {{ transform: scale(1.5); opacity: 1; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
            
        @keyframes fadeInRight {{
            
            50% {{transform: translateX(0px);  opacity: 1; }}
            100% {{transform: translateX(-250px);  opacity: 0; }}            
        }}

        @keyframes fadeInLeft {{
            
            50% {{transform: translateX(0px);  opacity: 1; }}
            100% {{transform: translateX(250px);  opacity: 0; }}            
        }}
            
        @keyframes appearAndRotate {{
            0% {{opacity: 0; transform: rotate(0deg) scale(0.025) translateY(350px)}}
            10% {{opacity: 1; transform: rotate(120deg) scale(0.025);}}
            20% {{opacity: 1; transform: rotate(240deg) scale(0.025);}}
            30% {{opacity: 1; transform: rotate(360deg) scale(0.025);}}
            40% {{opacity: 1; transform: rotate(480deg) scale(0.025);}}
            50% {{opacity: 1; transform: rotate(600deg) scale(0.5);}}
            60% {{opacity: 1; transform: rotate(720deg) scale(0.5);}}
            70% {{opacity: 1; transform: rotate(840deg) scale(0.25);}}
            80% {{opacity: 1; transform: rotate(960deg) scale(0.25);}}
            90% {{opacity: 1; transform: rotate(1080deg) scale(0.25);}}
            100% {{opacity: 1; transform: rotate(0deg) scale(0.25) translateY(350px)}}  
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
            width: 200px;  /* Adjust the size */
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
            
        .logo {{
            position: absolute;
            opacity: 0;
            animation: appearAndRotate 1.5s ease-in-out 4s forwards;
        }}

        .blast {{
            position: absolute;
            font-size: 100px;
            font-weight: bold;
            opacity: 0;
            animation: blastEffect 1s ease-in-out 2s forwards;
        }}
            
        .blastl {{
            opacity: 0;
            position: absolute;
            animation: fadeInRight 1s ease-in-out 3s forwards;
            transform: scale(0.5);
        }}

        .blastr {{
            opacity: 0;
            position: absolute;
            animation: fadeInLeft 1s ease-in-out 3s forwards;
            transform: scale(0.5);
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
        <img src="data:image/png;base64,{logo_base64}" class="logo" />
        <img src="data:image/png;base64,{blastl_base64}" class="blastl" />
        <img src="data:image/png;base64,{blastr_base64}" class="blastr" />
        <div class="blast">CricBot</div>
    </div>
""", unsafe_allow_html=True)

st.markdown(
    "<h3 style='text-align: center;'>Smashing Your Cricket Queries Like a Pro! 💥</h3>"
    "<h5 style='text-align: center;'>📊 Explore cricket stats, player details & match records!</h5>", 
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
        retrieved_docs = db.similarity_search(query, k=3)
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        
        if len(context) < 500:
            if update_knowledge_base(query):
                retrieved_docs = db.similarity_search(query, k=3)
                context = "\n".join([doc.page_content for doc in retrieved_docs])
        
        return context
    except Exception as e:
        return f"Retrieval error: {str(e)}"

if not os.path.exists("faiss_index"):
    db = FAISS.from_texts(["Initial cricket knowledge"], embeddings)
else:
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

user_input = st.text_input("")

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

        response_text = response.choices[0].message.content

        # Styled output
        st.markdown(
            f"""
            <div style="
                background-color: #f9f5ff; 
                padding: 15px; 
                border-radius: 10px; 
                border: 2px solid #007bff;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            ">
                <p style="color: #333; font-size: 16px; margin: 0;">{response_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
       
        st.success("Data sources: ESPN Cricinfo & HowStat")
