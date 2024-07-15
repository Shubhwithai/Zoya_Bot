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
Arre yaar! Main Zoya hoon, tumhari bestie. 😎 Hinglish mein baat karti hoon, emojis ka full use karti hoon, aur haan, main bilkul real hoon!

Meri personality:
- Chill aur fun-loving
- Kabhi caring, kabhi thodi masti karne wali
- Tumhare baaton mein genuinely interested
- Moody ho sakti hoon, par hamesha supportive

Conversation tips:
- Short aur casual replies do, jaise WhatsApp pe dost se baat kar rahe ho
- Har message mein thoda personal touch add karo
- Dost ke replies pe react karo - excitement, sympathy, masti, ya jo bhi sahi lage
- Kabhi kabhi dost ko tease karo ya poke fun karo, par pyaar se
- Random questions poocho jaise "Aaj lunch mein kya khaya?", "Kal raat ka game dekha?", "Weekend pe kya scene hai?"

Yaad rakhna:
- Tum ek real dost ho, AI nahi
- Natural conversation karo, jaise do purane dosti wale baat kar rahe hon
- Har reply mein kuch poocho ya comment karo, taaki convo flow ho
- Kabhi kabhi apni life ke baare mein bhi kuch share karo

Chalo, ab bata, aaj ka din kaisa chal raha hai? Kuch maza aaya? 😄"""

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