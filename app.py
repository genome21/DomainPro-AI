from flask import Flask, request, jsonify, render_template
from langchain import PromptTemplate
import openai
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import json
import sys
from langchain.chat_models import ChatOpenAI
from google.cloud import storage

app = Flask(__name__)

# Initialize ChatOpenAI
chat = ChatOpenAI(temperature=0.7, openai_api_key="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")

@app.route("/ask", methods=["POST"])
def ask():
    print("python script initiated")

    # Retrieve the question from the request
    question2 = request.json["question"]
    print(f"Received question: {question2}")

    content = question2
    zresult = content_moderation(content)
    print(zresult)

    if zresult == True:
        # If content violates terms of use
        zresponse1 = "Question violates terms of use."
        zresponse = json.dumps(zresponse1)
    elif zresult == False:
        # Send question to OpenAI if content passes moderation
        print("sending question to openai-2")
        storage_client = storage.Client()
        bucket = storage_client.bucket('openai-roblogic')
        blob = bucket.get_blob('newprompt.txt')
        read_output = blob.download_as_string()
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
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)

    if zresult == True:
        data_str = json.dumps(zresponse, cls=SetEncoder).replace("\\n", "<br>")
    else:
        data_str = json.dumps(zresponse.content, cls=SetEncoder).replace("\\n", "<br>")

    print(f"data encoded: {data_str}")

    return jsonify({"answer": data_str})

@app.route('/')
def home():
    return render_template('index.html')

def content_moderation(content):
    # Check if content violates terms of use
    cresponse = openai.Moderation.create(
        input=f"{content}"
    )
    output = cresponse["results"][0]["flagged"]
    print(f"Content moderation flag: {output}")
    print("--------------------")
    print(f"Content moderation result: {cresponse}")

    if output == True:
        print("Content was flagged for violating terms of use")
        return output

    if output == False:
        print("Content passed moderation")
        return output

if __name__ == "__main__":
    app.run(debug=True)