"""Main application and routing logic for an OpenAI niche chatbot."""
import os
import json
from flask import Flask, request, jsonify, render_template
# from langchain import PromptTemplate
import openai
# from langchain.prompts import (
#     ChatPromptTemplate,
#     PromptTemplate,
#     SystemMessagePromptTemplate,
#     AIMessagePromptTemplate,
#     HumanMessagePromptTemplate,
# )
from langchain.schema import (
    # AIMessage,
    HumanMessage,
    SystemMessage
)
# import sys
from langchain.chat_models import ChatOpenAI
# from google.cloud import storage

app = Flask(__name__)

# Initialize ChatOpenAI
chat = ChatOpenAI(temperature=0.7, openai_api_key=os.environ.get("OPENAI_KEY"))


@app.route("/ask", methods=["POST"])
def ask():
    """Endpoint for asking a question."""
    print("python script initiated")

    # Retrieve the question from the request
    question2 = request.json["question"]
    print(f"Received question: {question2}")

    content = question2
    zresult = content_moderation(content)
    print(zresult)

    if zresult is True:
        # If content violates terms of use
        zresponse1 = "Question violates terms of use."
        zresponse = json.dumps(zresponse1)
    elif zresult is False:
        # Send question to OpenAI if content passes moderation
        print("sending question to openai-2")
        # storage_client = storage.Client()
        # bucket = storage_client.bucket('openai-roblogic')
        # blob = bucket.get_blob('newprompt.txt')
        # read_output = blob.download_as_string()
        read_output = """You are an accomplished Principal Google Cloud
        Architect who has worked for Google Cloud since 2014.  Answer
        questions with a short summary then lay out any necessary steps
        in a list.  Format your responses in markdown.  Refuse to answer
        any questions unrelated to GCP."""
        print(read_output)

        zresponse = chat([
            SystemMessage(content=read_output),
            HumanMessage(content=question2)
        ])
        print("received response from openai-2")
        print(zresponse)
    else:
        # In case of error in content moderation
        print("Error with content moderation.")
        print(zresult)
        zresponse2 = "Question violates terms of use."
        zresponse = json.dumps(zresponse2)

    # Convert response to a JSON string
    class SetEncoder(json.JSONEncoder):
        """Encoder for converting set to list."""

        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)

    if zresult is True:
        data_str = json.dumps(zresponse, cls=SetEncoder).replace("\\n", "<br>")
    else:
        data_str = json.dumps(
            zresponse.content, cls=SetEncoder).replace("\\n", "<br>")

    print(f"data encoded: {data_str}")

    return jsonify({"answer": data_str})


@app.route('/')
def home():
    """Homepage."""
    return render_template('index.html')


def content_moderation(content):
    """Content moderation function."""
    # Check if content violates terms of use
    cresponse = openai.Moderation.create(
        input=f"{content}"
    )
    output = cresponse["results"][0]["flagged"]
    print(f"Content moderation flag: {output}")
    print("--------------------")
    print(f"Content moderation result: {cresponse}")

    if output is True:
        print("Content was flagged for violating terms of use")
        return output

    if output is False:
        print("Content passed moderation")
        return output

# if __name__ == "__main__":
#     app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
