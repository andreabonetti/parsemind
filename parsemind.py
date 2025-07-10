import copy
import json
from datetime import datetime, timedelta

import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import os

import base64
from email.mime.text import MIMEText


def authorize_and_save_token(
    client_secret_path="credentials/client_secret.json",
    token_path="credentials/token.json"
):
    '''Creates token.json'''
    # Scopes: read and send
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send"
    ]

    # Start OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the new token
    with open(token_path, "w") as token:
        token.write(creds.to_json())
    
    return creds

def call_gmail_api(token_file="credentials/token.json"):
    '''Call the Gmail API'''
    # If modifying these scopes, delete the file token.json.
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send"
    ]
    # Get credentials
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    # Return
    return service


def get_labels(service):
    """Get a list of labels in the user's mailbox."""
    try:
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])
        return labels
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def get_label_id_by_name(service, label_name):
    """Get the label ID by label name."""
    labels = get_labels(service)
    if labels:
        for label in labels:
            if label["name"] == label_name:
                return label["id"]
    return None


def get_msg_by_date_range(
    service,
    label_name: str,  # 'scholar'
    start_date,  # "2025-01-01"
    end_date,  # "2025-01-07"
    maxResults=500,  # apparently, 500 is the maximum allowed by Gmail API
):
    query = f"after:{start_date} before:{end_date}"
    label_id = get_label_id_by_name(service, label_name)
    result = (
        service.users()
        .messages()
        .list(userId="me", labelIds=[label_id], maxResults=maxResults, q=query)
        .execute()
    )
    messages = result.get("messages", [])
    print(messages)


def get_scholar_text(msg):
    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    subject = headers.get("Subject", "(No Subject)")
    # sender = headers.get("From", "(No Sender)")
    snippet = msg.get("snippet", "")

    # postprocessing of subject
    subject_improved = copy.deepcopy(subject)
    subject_improved = subject_improved.replace(" - new articles", "")
    subject_improved = subject_improved.replace(" - nuovi articoli", "")
    subject_improved = subject_improved.replace(
        "కర్రి రమేష్", ""
    )  # keeping only English script of Ramesh Kerri

    # postprocessing of snippet
    snippet_improved = copy.deepcopy(snippet)
    snippet_improved = snippet_improved.replace("[PDF]", "")
    snippet_improved = snippet_improved.lstrip()

    return subject_improved, snippet_improved


def get_today_and_week_ago():
    today = datetime.today().date()
    week_ago = today - timedelta(days=7)
    return today.strftime("%Y-%m-%d"), week_ago.strftime("%Y-%m-%d")


def ollama(
    prompt: str,
    model,  # 'gemma3:1b'
):
    # NOTE: you need to:
    # - install in ollama the models that you need, like gemma3:1b
    # - run `ollama serve` first in the terminal

    # call ollama
    response = requests.post(
        "http://localhost:11434/api/generate", json={"model": model, "prompt": prompt}
    )

    # Parse NDJSON (newline-delimited JSON)
    full_response = ""
    for line in response.text.strip().splitlines():
        if line.strip():
            data = json.loads(line)
            full_response += data.get("response", "")

    # strip
    response = full_response.strip()

    return response



def create_message(
    sender,
    to,
    subject,
    body_text
):
    message = MIMEText(body_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw_message}

def send_email(service, sender, to, subject, body):
    message = create_message(sender, to, subject, body)
    sent = service.users().messages().send(userId="me", body=message).execute()
    return sent