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
import polars as pl

# Model
vertexai.init(project="text2sql-412908", location="us-central1")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0,
}
processed_path = Path("data/processed")
db_path = processed_path / "bike_store.db"
# model = TextGenerationModel.from_pretrained("text-bison@002")
# model = CodeGenerationModel.from_pretrained("code-bison@002")
model = CodeChatModel.from_pretrained("codechat-bison@002")
model_chat = model.start_chat()
db_uri = f"sqlite:///{db_path.resolve().as_posix()}"
schema = get_db_schema(db_uri)
model_chat.send_message(SYSTEM_PROMPT.format(sql_schema=schema))


def parse_response(dict_response):
    print("dict_response", dict_response)
    return dict_response.text


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
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    raw_msg = model_chat.send_message(prompt, **parameters)
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
    # df1 = pl.read_database_uri(query=msg, uri=db_uri)
    # msg += df1

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
