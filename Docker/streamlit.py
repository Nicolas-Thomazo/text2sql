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

from text2sql import logger

st.session_state["chat_started"] = st.session_state.get("chat_started", False)

# Model
vertexai.init(project="text2sql-412908", location="us-central1")
parameters = {
    # "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0,
    # "top_k": 1,
}
processed_path = Path("data/processed")
db_path = processed_path / "bike_store.db"
schema = get_db_schema(f"sqlite:///{db_path.resolve().as_posix()}")
# model = TextGenerationModel.from_pretrained("text-bison@002")
# model = CodeGenerationModel.from_pretrained("code-bison@002")
if not st.session_state["chat_started"]:
    model = CodeChatModel.from_pretrained("codechat-bison@002")
    logger.info("\n\n\nstart chat\n\n\n")
    model_chat = model.start_chat(**parameters)
    model_chat.send_message(SYSTEM_PROMPT.format(sql_schema=schema))
    st.session_state["chat_started"] = True
    st.session_state["chat_model"] = model_chat


def parse_response(dict_response):
    print("dict_response", dict_response)
    return dict_response.text


# Streamlit App
st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Pour quelle question voulez vous que je génère une requête SQL?",
        },
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    logger.info(f"\n\n\nadd prompt: {prompt}\n\n\n")
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    raw_msg = st.session_state["chat_model"].send_message(prompt)
    msg = parse_response(raw_msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
