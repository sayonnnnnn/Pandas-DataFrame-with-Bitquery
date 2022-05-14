import requests 
import pandas as pd
from streamlit_ace import st_ace
import streamlit as st

st.set_page_config (
    page_title="Pandas with Bitquery",
    page_icon="https://test.bitquery.io/wp-content/uploads/2020/08/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Bitcoin Blocks Data with Bitquery")

def getAPIKey():
	return str(api)

def bitqueryAPICall(query: str):  
    headers = {'X-API-KEY': getAPIKey()}
    request = requests.post('https://graphql.bitquery.io/', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,query))

st.subheader("Write your GraphQL query here")
# Spawn a new Ace editor
content = st_ace()
# Display editor's content as you type
query = content

form = st.form("bitquery")
api = form.text_input("Enter your Bitquery API key")
# bitqueryAPIKey = api
submitted = form.form_submit_button("Submit")

result = 0
# height, count, transactionCount = [], [], []

def renderPandas(query: str, feature1="height", feature2="count", feature3="transactionCount"):
	res1, res2, res3 = [], [], []
	for i in query['data']['bitcoin']['blocks']:
		res1.append(i[feature1])
		res2.append(i[feature2])
		res3.append(i[feature3])
	df = pd.DataFrame(list(zip(res1, res2, res3)), columns=[feature1, feature2, feature3], dtype=float)
	st.subheader('The Pandas DataFrame rendered is as follows ')
	st.dataframe(df)
	

if submitted:
	result = bitqueryAPICall(query)
	st.success("The GraphQL query ran successfully!!")
	st.subheader("The output generated is as follows")
	st.write(result)

st.subheader("Generate your Pandas DataFrame")


form2 = st.form("pandas")
feature1 = form2.text_input("Enter the first feature")
feature2 = form2.text_input("Enter the second feature")
feature3 = form2.text_input("Enter the third feature")
api = form2.text_input("Enter your API key for confirmation")
submitted2 = form2.form_submit_button("Generate Pandas DataFrame")

if submitted2:
	result = bitqueryAPICall(query) 
	renderPandas(result, feature1, feature2, feature3) 
