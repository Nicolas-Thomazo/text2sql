from typing import Any, Mapping

import flask
import functions_framework


# Google Cloud Function that responds to messages sent in
# Google Chat.
#
# @param {Object} req Request sent from Google Chat.
# @param {Object} res Response to send back.
@functions_framework.http
def hello_chat(req: flask.Request) -> Mapping[str, Any]:
    if req.method == "GET":
        return "Hello! This function must be called from Google Chat."

    request_json = req.get_json(silent=True)

    display_name = request_json["message"]["sender"]["displayName"]
    avatar = request_json["message"]["sender"]["avatarUrl"]

    response = create_message(name=display_name, image_url=avatar)

    return response


# Creates a card with two widgets.
# @param {string} name the sender's display name.
# @param {string} image_url the URL for the sender's avatar.
# @return {Object} a card with the user's avatar.
def create_message(name: str, image_url: str) -> Mapping[str, Any]:
    avatar_image_widget = {"image": {"imageUrl": image_url}}
    avatar_text_widget = {"textParagraph": {"text": "Your avatar picture:"}}
    avatar_section = {"widgets": [avatar_text_widget, avatar_image_widget]}

    header = {"title": f"Hello {name}!"}

    cards = {
        "text": "Here's your avatar",
        "cardsV2": [
            {
                "cardId": "avatarCard",
                "card": {
                    "name": "Avatar Card",
                    "header": header,
                    "sections": [avatar_section],
                },
            }
        ],
    }

    return cards

# #%%
# import vertexai
# from vertexai.language_models import TextGenerationModel

# vertexai.init(project="qwiklabs-gcp-04-c9a24bfdfa64", location="us-central1")
# parameters = {
#     "candidate_count": 1,
#     "max_output_tokens": 1024,
#     "temperature": 0.9,
#     "top_p": 1
# }
# model = TextGenerationModel.from_pretrained("text-bison")
# response = model.predict(
#     """the color of the sky is
# """,
#     **parameters
# )
# print(f"Response from Model: {response.text}")

# # %%
