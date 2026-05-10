import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
KEY = os.getenv("AZURE_OPENAI_KEY")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")


client = AzureOpenAI(
    azure_endpoint=ENDPOINT,
    api_key=KEY,
    api_version="2024-12-01-preview"
)

st.set_page_config(page_title="Chat With ME", page_icon="💬✨")


st.markdown("""
<style>
@keyframes glow {
  0% { text-shadow: 0 0 5px #4b9fff; }
  50% { text-shadow: 0 0 20px #9b59ff; }
  100% { text-shadow: 0 0 5px #4b9fff; }
}
.glow-title {
  font-size: 40px;
  font-weight: 700;
  text-align: center;
  animation: glow 2s ease-in-out infinite;
}
</style>
           
<h1 class="glow-title">✨💬 Chat With Me💬✨</h1>



            """, unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state["messages"] = []


for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])


user_input = st.chat_input("Enter your message here")

if user_input:
   
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

   
    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=st.session_state["messages"]
    )
    bot_reply = response.choices[0].message.content

  
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)