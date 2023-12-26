import os
import streamlit as st
import sys
sys.path.append("/")
from rag_rules.modules.llamaindex_rag.rag import RetrieverAssistedGenerator
DATA_FILE = "data/pdf/regles 40K ENGLISH.pdf"
EMBED_MODEL = "models/allminilm"
LLM_MODEL = "models/llms/zephyr-7b-beta.Q3_K_S.gguf"


@st.cache_resource
def load_data():
    my_rag = RetrieverAssistedGenerator(embedding_model=EMBED_MODEL, llm_model=LLM_MODEL)
    return my_rag.create_index(DATA_FILE)


st.header("Chat with the V10 rulebook")
if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about the rules of warhammer 40K !"}
    ]

my_index = load_data()
chat_engine = my_index.as_chat_engine(chat_mode="condense_question", verbose=True)
if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
