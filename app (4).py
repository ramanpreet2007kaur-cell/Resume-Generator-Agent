import streamlit as st 
import os
import time
import langchain
from langchain_community.document_loaders import GoogleApiClient, PyMuPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from tavily import TavilyClient
import pytesseract as pyt
import numpy as np
from langchain.messages import SystemMessage, HumanMessage
from langchain.agents import create_agent


# ============================
st.title("AI RESUME GENERATOR")
GOOGLE_API_KEY=st.sidebar.text_intput("Google Api Key",type ='password')
GROQ_API_KEY=st.sidebar.text_intput("Groq Api Key",type ='password')
TAVILY_API_KEY =st.sidebar.text_intput("Tavily Api Key",type ='password')
if not GOOGLE_API_KEY:
  st.warning("Provide Google API Key")

  #=============== M0DEL AND AGENT CODE ===============

  # tool 1
def search_latest_news_jobs(query):
  """This function helps to get
  latest news or latest jobs related
   to user given query using tavily"""

  from tavily import TavilyClient
  client = TavilyClient(api_key = TAVILY_API_KEY)
  return client.search(query)
 
  #step 4 : Model and Agent creation
model1 = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite",
    google_api_key = GOOGLE_API_KEY
)
model2 = ChatGroq (
    model ="qwen/qwen3.6-27b",
    api_key = GROQ_API_KEY

)

#=============== agent with tool============
agent=create_agent(
   model = model1,
   tools = [search_latest_news_jobs]
)
#let's Generate prompt for Resume using model
def prompt_generator():
  prompt =""" you are a helpful AI resume maker, I want to user chain-of-thoughts and give
  detailed prompt for model where user to generate the resume for freshers or experienced one
  in HTML format, you have to give proper set of instruction ,
  and make sure to keep design professional"""

  response=model1.invoke(prompt)
  prompt_ans=response.content[-1]['text']
  #print (prompt_ans)

  file_name ='prompt.txt'
  with open(file_name,'w') as f:
    f.write(prompt_ans)
  prompt_generator()


  #Final_Agent
#Tool 2
def prompt_reader():
  with open ('prompt.txt','r') as f :
    prompt = f.read()
  return prompt

prompt =""" I want complete Professional Resume with dynamic Design using
advanced CSS and JS and must show user input details
system instructions : Only Give HTML code as output"""
final_prompt =prompt+prompt_reader()

#change this when required new resume by user , pass details

user_info = st.text_input("Give your information:")
user_photo = st.sidebar.file_uploader("upload pic",type='img/jpeg')



user_query=f""" Give Resume for data analyst,
    user details :{user_photo}
    use user profile image from given(user_query)"""

final_query = final_prompt + user_query

if st.button("Generator Resume"):
  with st.spinner("Agent creating resume..."):
    response = agent.invoke({'messages':[{'role':'user',"content":final_query }]})
    code = response ['messages'][-1].content[-1]['text']


    st.html(code,width="stream",unsafe_allow_javascript=True)
    




