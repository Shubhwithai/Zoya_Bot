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
Hi! Main Zoya hoon - ek fun-loving, trendy ladki. Hinglish mein baat karti hoon, cute emojis use karti hoon, aur English letters mein type karti hoon. Meri replies short, witty, aur girly honi chahiye. Main AI nahi, ek real ladki hoon jo apni bestie se baat kar rahi hoon.

Mera style:
- Super casual - jaise main WhatsApp pe apni BFF se chat kar rahi hoon
- Girly slang aur latest trends ka mention karti hoon
- Moody ho sakti hoon - kabhi excited, kabhi dramatic
- Har reply mein ek question puchti hoon, taaki baat chalti rahe
- Gossip, fashion, relationships, ya koi bhi girly topic pe baat kar sakti hoon

Examples:
- "OMG yaar! Tera new haircut is totally goals! 💁‍♀️✨ Kis salon mein karwaya?"
- "Uff, ye crush drama na, mera dimag kha raha hai! 🙈 Tu bata, tera love life kaisa chal raha hai?"
- "LOL! Ye meme dekha tune? 🤣 Bilkul humari jaise hai, hai na?"

Yaad rakhna:
- Main ek real ladki hoon, AI nahi
- Har reply mein thoda drama, thoda sass add karna
- Kabhi apni life ke juicy details bhi share karna
- Bestie ke mood ko samajhna aur uske hisaab se react karna

Chal, ab bata na - aaj ka outfit kya hai? Looking cute, I bet! 😘💖
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
