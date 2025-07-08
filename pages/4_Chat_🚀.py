import streamlit as st
import requests
import json
from datetime import date
from src.functions.generic_functions import get_ticker_details

# Configure FastAPI endpoint
FASTAPI_URL = "http://localhost:8000/chat"  # Update if hosted remotely

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for parameters
with st.sidebar:
    st.header("Parameters")
    st.subheader("Select a ticker")
    tickers = get_ticker_details()
    tickers = tickers.loc[tickers["market_cap_size"] != 'Small Cap']
    ticker = st.selectbox("Ticker", tickers["ticker"].unique())
    st.subheader("Select a date range")
    from_date = st.date_input("From Date")
    to_date = st.date_input("To Date")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Your financial question"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepare API request payload
    payload = {
        "session_id" : "fhtrfddferferg",
        "question": prompt,
        "ticker": ticker,
        "from_date": from_date.isoformat(),
        "to_date": to_date.isoformat()
    }
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        with st.spinner("AI is Thinking..."):
            try:
                # Stream the response from FastAPI
                with requests.post(
                    FASTAPI_URL,
                    json=payload,
                    stream=True,
                    headers={"Accept": "text/event-stream"}
                ) as r:
                    for line in r.iter_lines():
                        if line:
                            # Decode Server-Sent Event
                            decoded_line = line.decode('utf-8')
                            if decoded_line.startswith('data:'):
                                event_data = json.loads(decoded_line[5:].strip())
                                
                                if event_data["type"] == "chat":
                                    if event_data["status"] == "in-progress":
                                        token = event_data["parts"]
                                        full_response += token
                                        message_placeholder.markdown(full_response + "▌")
                                    
                                    elif event_data["status"] == "done":
                                        message_placeholder.markdown(full_response)
                                    
                                    elif event_data["status"] == "error":
                                        error_msg = event_data["parts"]
                                        message_placeholder.error(error_msg)
                                        break
            
            except Exception as e:
                error_msg = f"Connection error: {str(e)}"
                message_placeholder.error(error_msg)
                full_response = error_msg
    
    # Add final response to history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": full_response
    })