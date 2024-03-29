# First
import streamlit as st
import vertexai
from vertexai.language_models import (
    TextGenerationModel,
    CodeGenerationModel,
    CodeChatModel,
)
import polars as pl
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
db_uri = f"sqlite:///{db_path.resolve().as_posix()}"
schema = get_db_schema(
    db_uri
)  # model = TextGenerationModel.from_pretrained("text-bison@002")
# model = CodeGenerationModel.from_pretrained("code-bison@002")
if not st.session_state["chat_started"]:
    model = CodeChatModel.from_pretrained("codechat-bison@002")
    logger.info("\n\n\nstart chat\n\n\n")
    model_chat = model.start_chat(**parameters)
    model_chat.send_message(SYSTEM_PROMPT.format(sql_schema=schema))
    st.session_state["chat_started"] = True
    st.session_state["chat_model"] = model_chat


def parse_response_sql(input):
    import re

    # Pattern to match the SQL code block
    # This pattern looks for the start of the string, followed by ```sql, then captures everything
    # until the closing ```, ensuring that it doesn't greedily go beyond the first closing ```
    pattern = r".*```sql(.*?)```.*"

    # The re.DOTALL flag allows the dot (.) to match newlines as well
    matches = re.search(pattern, input, flags=re.DOTALL)

    if matches:
        # Return the first captured group (the SQL query), and strip leading/trailing whitespace
        return matches.group(1).strip()
    else:
        # Return None or raise an error if no match is found
        return None


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
    try:
        print(f"query is {msg}")
        query = parse_response_sql(msg)
        print(f"now is {query}")
        df = pl.read_database_uri(query=query, uri=db_uri)
        msg += "\nVoici le resultat de votre requête sur la base de données\n"

        msg += "```python" + df.__str__()
        # if st.button("Download"):
        #     st.download_button(label="data", data=df)
    except Exception as e:
        print(f"not working {e}")

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
