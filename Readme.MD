# DomainPro-AI

An AI chatbot specialized in domain-specific knowledge. Set the desired topic (e.g., "Financial Analytics") to access precise information, while the bot politely declines unrelated queries. A valuable tool for specialized expertise and support in niche fields.

## Setup
1. Clone the github repo
2. CD into the repo folder
3. Navigate to ```./templates/index.html```
4. Change the chatbot site title on <b>line 6</b>
5. Change the chatbot name in the header on <b>line 45</b>
6. Navigate to ```./app.py```
7. Change the bucket name storing the prompt template on <b>line 90</b>
8. Change the file name of the prompt template on <b>line 91</b>
9. Create a ```.env``` file in the root of the repo folder and set the following variables to client specs:
```
PROJECT_ID = "my-project-id"
APP_NAME = "my-chat-app"
APP_REGION = "us-central1"
OPENAI_KEY = "ab-cdefghijklmnopqrstuvwxyz01234567890987654321"
```

## Deployment
1. Ensure that your GCP admin account has access to the client's environment with the ```Admin Storage```, ```Cloud Run Deployment```, and ```Service Account User``` roles.
2. Run ```bash ./deploy.sh``` to deploy the custom chat app as a Cloud Run Service in the client's GCP project.