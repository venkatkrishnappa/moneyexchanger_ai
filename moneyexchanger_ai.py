from typing import Tuple, Dict
from dotenv import load_dotenv
import os
import requests
import json
import streamlit as st
from openai import OpenAI

load_dotenv()
EXCHANGERATE_API_KEY=os.getenv("EXCHANGERATE_API_KEY")

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
    response = json.loads(requests.get(url).text)
    return (base,target,amount,f'{response["conversion_result"]:.2f}')

def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt.
       The output from the LLM should be a JSON (dict) with the base, amount and target"""
    try:
        
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": textbox_input,
                }
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )          
    except Exception as e:
        print(f"Exception {e} for {textbox_input}")
    else:
        return completion.choices[0].message.content

def run_pipeline():
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""

    if True: #tool_calls
        # Update this
        st.write(f'{base} {amount} is {target} {exchange_response["conversion_result"]:.2f}')

    elif True: #tools not used
        # Update this
        st.write(f"(Function calling not used) and response from the model")
    else:
        st.write("NotImplemented")

# Title of the app
st.title("Multilingual Currency Converter")

# Create an input form
with st.form("currency_converter_form"):
    # Free text field for input
    user_input = st.text_input("Enter your amount and currencies (e.g., '100 USD to EUR')", "")
    
    # Submit button
    submitted = st.form_submit_button("Convert")

    if submitted and user_input:
        try:
            st.write(call_llm(user_input))

        except Exception as e:
            st.error("There was an error processing your request. Please check your input format.")        