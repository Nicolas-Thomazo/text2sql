# First
import streamlit as st
import vertexai
from vertexai.language_models import TextGenerationModel

# Model
vertexai.init(project="text2sql-412908", location="us-central1")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.9,
    "top_p": 1,
}
model = TextGenerationModel.from_pretrained("text-bison@002")


def parse_response(dict_response):
    print("dict_response", dict_response)
    return dict_response.text


# Streamlit App
st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    raw_msg = model.predict(prompt, **parameters)
    msg = parse_response(raw_msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
