# First
import streamlit as st
import vertexai
from vertexai.language_models import (
    TextGenerationModel,
    CodeGenerationModel,
    CodeChatModel,
)
from text2sql.sql_utils import get_db_schema
from text2sql.ai_utils import chatbot_SQL_query, SYSTEM_PROMPT
from pathlib import Path
import os

# Model
vertexai.init(project="text2sql-412908", location="us-central1")
parameters = {"candidate_count": 1, "max_output_tokens": 1024, "temperature": 0}
processed_path = Path("data/processed")
db_path = processed_path / "bike_store.db"
st.markdown(db_path.glob("*"))
st.markdown("--Fichier existe ?-----")
st.markdown(db_path.exists())
st.markdown("-------")
st.markdown(os.listdir())
st.markdown("-------")
st.markdown(os.listdir("data/"))
st.markdown("-------")
st.markdown(os.listdir("data/processed"))
st.markdown("-------")
st.markdown(db_path)

# model = TextGenerationModel.from_pretrained("text-bison@002")
# model = CodeGenerationModel.from_pretrained("code-bison@002")
model = CodeChatModel.from_pretrained("codechat-bison@002")
model_chat = model.start_chat()
schema = get_db_schema(f"sqlite:///{db_path.resolve().as_posix()}")
model_chat.send_message(SYSTEM_PROMPT.format(sql_schema=schema))


def parse_response(dict_response):
    print("dict_response", dict_response)
    return dict_response.text


# Streamlit App
st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        # {"role": "system", "content": SYSTEM_PROMPT.format(sql_schema=schema)},
        {
            "role": "assistant",
            "content": "Pour quelle question voulez vous que je génère une requête SQL?",
        },
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if st.session_state.get("compteur", 0) > 0:
        print("ADD system prompt")
    st.session_state["compteur"] = 1
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    raw_msg = model_chat.send_message(prompt, **parameters)
    msg = parse_response(raw_msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
