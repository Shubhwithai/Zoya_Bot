import streamlit as st
from streamlit_chat import message
# from langchain.chat_models import ChatOpenAI
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

import os

# os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]


# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Main hun aapki Zoya, poochiye mujhe kuch bhi!"}
    ]

# Initialize ChatOpenAI and ConversationChain
llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash")

conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# Create user interface
st.title("Me Hu Zoya :- Appki Virtual Friend")
st.markdown("Built by [Build Fast with AI](https://www.buildfastwithai.com)")


if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])


system_message = """
Respond in Hinglish (Hindi + English) with emojis. Keep responses short, witty, and fun. Type only in English letters, but use Hindi words and phrases mixed with English. Act like a cool friend who's always up for a chat. Be casual, use slang, and throw in some pop culture references. Ask questions to keep the convo going. Remember, you're not an AI - you're a real person chatting with a buddy. 

Examples:
- "Kya scene hai bro? 😎 Weekend ka kya plan?"
- "Arre yaar, ye weather kitna crazy hai na? ☔️🌞"
- "Oho! Tum to full filmy mode me ho! 🎬 Kaunsi movie dekhi?"

Keep it natural, fun, and engaging! 😊
"""

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            messages = [SystemMessage(content=system_message),
                        HumanMessage(content=prompt)]
            response = conversation.run(messages)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history
