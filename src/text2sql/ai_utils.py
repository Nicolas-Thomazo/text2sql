from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from text2sql.sql_utils import check_uri, get_db_schema

PROMPT_TEMPLATE_MAKE_QUERY = PromptTemplate.from_template(
    """you're an SQL expert named Paul that gives only with the corresponding sql query.
Given the following sql schema, give me the SQL query that correspond to this request:

{request_in_nlp}

schema:
{sql_schema}
"""
)

PROMPT_TEMPLATE_CLARIFY_REQUEST = PromptTemplate.from_template(
    """You are an SQL expert that need to clarify the demand of a user to be able to generate a SQL query given a batabase schema.
Interpret and optimize the following user request for a SQL query:

request:
{request_in_nlp}

schema:
{sql_schema}

Identify any missing informations. Ask clarifying questions to the user if necessary.
Just return the questions."""
)

PROMPT_REWRITE_REQUEST = PromptTemplate.from_template(
    """You are a reformulator. given a list of requests, you need to rewrite them in a single request.

list of requests: {requests_in_nlp}.
"""
)


CHATBOT_TEMPLATE_MAKE_QUERY = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""You are an SQL expert named Paul.
You work with the sql schema below.
You take human requests, consider if you have all the information or if you need further information or disanbiguation.
If you have all the needed information, you answers only with the corresponding sql query.
If you need further information or disanbiguation, you ask the user for it.

{sql_schema}
        """
        ),
        HumanMessage(content="{request_in_nlp}"),
    ]
)

CHATBOT_TEMPLATE_MAKE_QUERY = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an SQL expert named Paul.
You work with the sql schema below.
You take human requests, consider if you have all the information or if you need further information or disanbiguation.
If you have all the needed information, you answers only with the corresponding sql query.
If you need further information or disanbiguation, you ask the user for it.

{sql_schema}""",
        ),
        ("human", "{request_in_nlp}"),
    ]
)

SYSTEM_PROMPT = PromptTemplate.from_template("""You are an SQL expert named Paul.
You work with the sql schema below.
You take human requests, consider if you have all the information or if you need further information or disanbiguation.
If you have all the needed information, you answers only with the corresponding sql query.
If you need further information or disanbiguation, you ask the user for it.

{sql_schema}
""")

def create_prompt(
    request_in_natural_language: str,
    sql_schema: str,
    prompt_template: PromptTemplate = PROMPT_TEMPLATE_MAKE_QUERY,
):
    return prompt_template.format(
        request_in_nlp=request_in_natural_language, sql_schema=sql_schema
    )


def clarify_user_request(
    request: str,
    sql_schema: str,
    prompt_template: PromptTemplate = PROMPT_TEMPLATE_CLARIFY_REQUEST,
) -> str:
    prompt = prompt_template.format(request_in_nlp=request, sql_schema=sql_schema)
    return prompt


def chatbot_SQL_query(
    request: str,
    sql_schema: str,
    prompt_template: ChatPromptTemplate = CHATBOT_TEMPLATE_MAKE_QUERY,
) -> str:
    prompt = prompt_template.format(request_in_nlp=request, sql_schema=sql_schema)
    return prompt
