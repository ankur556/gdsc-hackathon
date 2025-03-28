# gdsc-hackathon


## PS:
CricBot (4)
Create a cricket-based AI Agent to answer any complex queries of the user. Try out
web scraping or open-sourced models to answer a query.
Examples:
“Is Virat Kohli going to beat Sachin in a 1v1?”
“MS Dhoni runs against leg spinners and fast bowlers”.
Goal:
Maximise your range of complex queries that can be answered.


So we present:

# CricBot Pro 🏏

An AI-powered cricket assistant that answers complex queries about players, matches, and statistics by leveraging web scraping and LLM capabilities.

## Features

- Real-time data scraping from ESPN Cricinfo and HowStat
- Vector-based knowledge retrieval using FAISS
- Dynamic content fetching for up-to-date information
- Interactive Streamlit UI with cricket-themed animations
- Powered by Groq's LLama 3.3 70B model

## Technologies Used

- **LLM Integration**: Groq API with Llama 3.3 70B
- **Vector Database**: FAISS for similarity search
- **Embeddings**: HuggingFace Sentence Transformers
- **Web Scraping**: Selenium and ScrapingBee 
- **Frontend**: Streamlit

## Installation

```bash
git clone https://github.com/yourusername/gdsc-hackathon.git
cd gdsc-hackathon
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file with the following variables:
```
GROQ_API_KEY=your_groq_api_key
SCRAPINGBEE_API_KEY=your_scrapingbee_api_key
```

## Running the Application

```bash
streamlit run rag.py
```

## Example Queries

- "Is Virat Kohli going to beat Sachin in a 1v1?"
- "MS Dhoni runs against leg spinners and fast bowlers"
- "Compare Bumrah's bowling statistics with Brett Lee's"
- "Which opening batsman has the highest average in T20 cricket?"

## Demo

![CricBot Pro Demo](demo.gif)

