import base64
import copy
import json
import os
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from pathlib import Path

import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

# ================================================================================
# gmail api
# ================================================================================


def authorize_and_save_token(client_secret_path='credentials/credentials.json', token_path='credentials/token.json'):
    """Creates token.json"""
    # Scopes: read and send
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

    # Start OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the new token
    with open(token_path, 'w') as token:
        token.write(creds.to_json())

    return creds


def call_gmail_api(token_file='credentials/token.json'):
    """Call the Gmail API"""
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
    # Get credentials
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    # Return
    return service


def create_message(sender, to, subject, body_text):
    """Create message"""
    message = MIMEText(body_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}


def send_email(service, sender, to, subject, body):
    """Send email"""
    message = create_message(sender, to, subject, body)
    sent = service.users().messages().send(userId='me', body=message).execute()
    return sent


def get_labels(service):
    """Get a list of labels in the user's mailbox."""
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return labels
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def get_label_id_by_name(service, label_name):
    """Get the label ID by label name."""
    labels = get_labels(service)
    if labels:
        for label in labels:
            if label['name'] == label_name:
                return label['id']
    return None


# TODO: not used
# def get_msg_by_date_range(
#     service,
#     label_name: str,  # 'scholar'
#     start_date,  # "2025-01-01"
#     end_date,  # "2025-01-07"
#     maxResults=500,  # apparently, 500 is the maximum allowed by Gmail API
# ):
#     query = f'after:{start_date} before:{end_date}'
#     label_id = get_label_id_by_name(service, label_name)
#     result = service.users().messages().list(userId='me', labelIds=[label_id], maxResults=maxResults, q=query).execute()
#     messages = result.get('messages', [])
#     print(messages)


def get_scholar_text(msg):
    """Get text of Google Scholar email"""
    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
    subject = headers.get('Subject', '(No Subject)')
    # sender = headers.get("From", "(No Sender)")
    snippet = msg.get('snippet', '')

    # postprocessing of subject
    subject_improved = copy.deepcopy(subject)
    subject_improved = subject_improved.replace(' - new articles', '')  # english
    subject_improved = subject_improved.replace(' - nuovi articoli', '')  # italian
    subject_improved = subject_improved.replace(' కర్రి రమేష్', '')  # keeping only English script of Ramesh Kerri

    # postprocessing of snippet
    snippet_improved = copy.deepcopy(snippet)
    snippet_improved = snippet_improved.replace('[PDF]', '')
    snippet_improved = snippet_improved.replace('[HTML]', '')
    snippet_improved = snippet_improved.replace('POSTER:', '')
    snippet_improved = snippet_improved.lstrip()

    return subject_improved, snippet_improved


# ================================================================================
# ollama
# ================================================================================


def ollama(
    prompt: str,
    model,  # 'gemma3:1b'
):
    # NOTE: you need to:
    # - install in ollama the models that you need, like gemma3:1b
    # - run `ollama serve` first in the terminal

    # call ollama
    response = requests.post('http://localhost:11434/api/generate', json={'model': model, 'prompt': prompt})

    # Parse NDJSON (newline-delimited JSON)
    full_response = ''
    for line in response.text.strip().splitlines():
        if line.strip():
            data = json.loads(line)
            full_response += data.get('response', '')

    # strip
    response_str = full_response.strip()

    return response_str


# ================================================================================
# parsemind
# ================================================================================


def get_today_and_week_ago():
    """Get dates of today and one week ago"""
    today = datetime.today().date()
    week_ago = today - timedelta(days=7)
    format = '%Y-%m-%d'
    dates = {'start_date': week_ago.strftime(format), 'end_date': today.strftime(format)}
    return dates


def get_weeks_after(date_str):
    """Get full Monday–Sunday weeks after a given date, until today."""
    format = '%Y-%m-%d'
    start_date = datetime.strptime(date_str, format).date()
    today = datetime.today().date()

    # Move start_date to the next Monday if it's not already a Monday
    days_to_next_monday = (7 - start_date.weekday()) % 7
    if days_to_next_monday == 0:
        next_monday = start_date
    else:
        next_monday = start_date + timedelta(days=days_to_next_monday)

    weeks = []
    current_start = next_monday
    while current_start + timedelta(days=6) <= today:
        current_end = current_start + timedelta(days=6)
        start_date = current_start.strftime(format)
        end_date = current_end.strftime(format)
        weeks.append({'start_date': start_date, 'end_date': end_date, 'range_date': f'{start_date}_{end_date}'})
        current_start += timedelta(days=7)

    return weeks


def get_scholar_summary(service, dates, verbose=False, debug=False):
    """Generate Google Scholar section of the summary"""
    # select label
    label = 'scholar'
    label_id = get_label_id_by_name(service, label)

    # gmail query
    q = f'after:{dates["start_date"]} before:{dates["end_date"]}'

    # get messages
    if verbose:
        print('Scholar: Get messages...')
    result = (
        service.users()
        .messages()
        .list(
            userId='me',
            labelIds=[label_id],
            q=q,
        )
        .execute()
    )
    messages = result.get('messages', [])

    # get subjects and snippets
    if verbose:
        print('Scholar: Get subjects and snippets...')
    scholar = []
    for message in messages:
        msg_id = message['id']
        msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        [subject_improved, snippet_improved] = get_scholar_text(msg)
        scholar.append([subject_improved, snippet_improved])

    # scholar text
    scholar_text = ''
    for s in scholar:
        scholar_text += f'- **{s[0]}**: {s[1]}\n'

    scholar_text_before_llm = copy.deepcopy(scholar_text)

    # llm parsing with ollama
    if verbose:
        print('Scholar: LLM parsing with ollama...')

    if debug:
        if verbose:
            print('Scholar: [DEBUG] Running with small LLM model')
        model = 'gemma3:1b'
    else:
        model = 'gemma3:12b'

    prompt = f"""
    The text below is a bullet point list.
    Each bullet point reports the reference author in bold, the title, the complete list of authors, and additional information.
    Remove the complete list of authors and the additional information **after** the title of each bullet point.
    Keep the reference author and the title, as they are now.
    Between the author and the title, write '(patent)' if the bullet point is a patent or '(paper)' if the bullet point is a paper.

    Example of input bullet point:
    - **Subhasish Mitra**: Generalized qed pre-silicon verification framework S Mitra, C BARRETT, CJ Trippel, S Chattopadhyay - US Patent App. 18/541722, 2025 Abstract Systems and methods of verifying a hardware processing
    The output should be:
    - **Subhasish Mitra** (patent): Generalized qed pre-silicon verification framework

    Example of input bullet point:
    - **Luca Benini***: RapidChiplet: A Toolchain for Rapid Design Space Exploration of Inter-Chiplet Interconnects P Iff, B Bruggmann, B Morel, M Besta, L Benini… - Proceedings of the 22nd …, 2025
    The output should be:
    - **Luca Benini*** (paper): RapidChiplet: A Toolchain for Rapid Design Space Exploration of Inter-Chiplet Interconnects

    Return the modified text without any comment or request from you.
    {scholar_text_before_llm}
    """
    scholar_summary = ollama(prompt=prompt, model=model)

    # add header
    scholar_summary = '## Google Scholar\n' + scholar_summary

    # space at the end
    scholar_summary += '\n\n'

    # debug
    if debug and verbose:
        print('Scholar: [DEBUG] scholar_text_before_llm')
        print(scholar_text_before_llm)
        print('Scholar: [DEBUG] scholar_summary')
        print(scholar_summary)

    # return
    return scholar_summary


def get_summary(
    dates,
    # summaries
    scholar=True,
    # markdown
    markdown=False,  # save summary as markdown
    output_folder='output',
    markdown_file='parsemind.md',
    homepage_file='parsemind.md',
    # print
    do_print=False,
    # misc
    verbose=False,
    debug=False,
):
    """Generate the summary of the newsletters"""
    # call gmail api
    service = call_gmail_api()

    # summary
    summary = f'# ParseMind: {dates["start_date"]} ~ {dates["end_date"]}\n\n'
    summary += f'[Back to homepage.]({homepage_file})\n'
    if scholar:
        summary += get_scholar_summary(service=service, dates=dates, verbose=verbose, debug=debug)

    # markdown
    if markdown:
        # Create folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        # Create file if it doesn't exist
        markdown_path = os.path.join(output_folder, markdown_file)
        with open(markdown_path, 'w') as f:
            f.write(summary)

    # print
    if do_print:
        print(summary)


def update_markdown_homepage(
    output_folder='output',
    markdown_file='parsemind.md',
):
    """Update markdown homepage"""
    # Create folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # get list of markdown editions
    folder = Path(output_folder)
    files = [f.name for f in folder.iterdir() if f.is_file()]
    files = [f for f in files if not (f == markdown_file or '_last_week.md' in f or f == '.gitignore')]

    # sort the list
    files = sorted(files, reverse=True)

    def format_date_range(date_str: str) -> str:
        # Input example: 'parsemind_2025-07-07_2025-07-13'
        parts = date_str.split('_')
        start_date = datetime.strptime(parts[1], '%Y-%m-%d')
        end_date = datetime.strptime(parts[2], '%Y-%m-%d')

        # Format: '7 July 2025 - 13 July 2025'
        return f'{start_date.day} {start_date.strftime("%B %Y")} - {end_date.day} {end_date.strftime("%B %Y")}'

    # content
    content = '# ParseMind\n'
    for file in files:
        # remove .md extension
        file_text = file.replace('.md', '')

        # format date range
        file_text = format_date_range(date_str=file_text)

        content += f'- [{file_text}]({file})\n'

    # write to file
    markdown_path = os.path.join(output_folder, markdown_file)
    with open(markdown_path, 'w') as f:
        f.write(content)
