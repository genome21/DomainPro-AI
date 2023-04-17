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

chat = ChatOpenAI(temperature=0.7, openai_api_key="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")

# template = """
# You are an accomplished Principal Google Cloud Architect who has worked for Google Cloud since 2014.  Answer questions with a summary then lay out the steps in a list.

# {question}
# """

# prompt = PromptTemplate(
#     input_variables=["question"],
#     template=template
# )

@app.route("/ask", methods=["POST"])
def ask():
    print("python script initiated")
    #data = request.get_json()
    #print(f"data: {data}")
    #question = data.get("question")
    #print(f"question: {question}")
    question2 = request.json["question"]
    print(f"Received question: {question2}")

    content = question2
    zresult = content_moderation(content)
    print(zresult)

    #print(f"Chat input data: {[HumanMessage(content=question2)]}")


    #response = prompt.format_prompt(question={question})
    #system_message_prompt = SystemMessagePromptTemplate.from_template(prompt)
    #human_template="{text}"
    #response = HumanMessagePromptTemplate.from_template(human_template)
    #chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])

    # get a chat completion from the formatted messages
    #response = chat_prompt.format_prompt(question={question}).to_messages()

    #print(f"Response: {system_message_prompt}")
    #system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)
    #zresponse = system_message_prompt({question})
    print("sending question to openai-1")
    # chat([
    #     SystemMessage(content="You are a nice AI bot that helps a user figure out their Google Cloud issues in one short sentence.  Refuse to answer any questions unrelated to GCP."),
    #     HumanMessage(content=question2)
    # ])
    #print(chat)

    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)

    print("received response from openai-1")

    #zresult = "undefined"
    if question2 == "test message":
        zresult = True
    if zresult == True:
        zresponse1 = "Question violates terms of use."
        #zresponse.content = json.dumps(zresult, cls=SetEncoder).replace("\\n", "<br>")
        zresponse = json.dumps(zresponse1)
    elif zresult == False:
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
        print("Error with content moderation.")
        print(zresult)
        #sys.exit(f"zresponse: {zresponse}")
        zresponse2 = "Question violates terms of use."
        zresponse = json.dumps(zresponse2)

    
    if zresult == True:
        data_str= json.dumps(zresponse, cls=SetEncoder).replace("\\n", "<br>")
    else:
        data_str = json.dumps(zresponse.content, cls=SetEncoder).replace("\\n", "<br>")        

    print(f"data encoded: {data_str}")

    # response_messages = chat([
    #     SystemMessage(content="You are a nice AI bot that helps a user figure out their Google Cloud issues in one short sentence.  Refuse to answer any questions unrelated to GCP."),
    #     HumanMessage(content=question)
    # ])

    #zresponse = response_messages[-1].content if response_messages and isinstance(response_messages[-1], AIMessage) else "Sorry, I couldn't process your question. Please try again later."

    return jsonify({"answer": data_str})

@app.route('/')
def home():
    return render_template('index.html')

def content_moderation(content):
    #cresponse = openai.ContentFilter.create(
    #prompt=f"{content}"
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
        #sys.exit("Content was flagged for violating terms of use")

    if output == False:
        print("Content passed moderation")
        return output


if __name__ == "__main__":
    app.run(debug=True)
