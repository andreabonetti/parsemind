from parsemind import get_label_id_by_name
from parsemind import call_gmail_api
from parsemind import get_labels
from parsemind import get_label_id_by_name
from parsemind import get_scholar_text
from parsemind import get_today_and_week_ago
from parsemind import ollama

import copy

if __name__ == "__main__":
    # call gmail api
    service = call_gmail_api()
    labels = get_labels(service)

    # select label
    label = 'scholar'
    label_id = get_label_id_by_name(service, label)

    # get dates
    [end_date, start_date] = get_today_and_week_ago()

    # query
    q = f"after:{start_date} before:{end_date}"

    # get messages
    result = service.users().messages().list(
        userId='me',
        labelIds=[label_id],
        q=q,
        ).execute()
    messages = result.get('messages', [])

    # get subjects and snippets
    print('Running: get subjects and snippets...')
    scholar = []
    for message in messages:
        msg_id = message['id']
        msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        [subject_improved, snippet_improved] = get_scholar_text(msg)
        scholar.append([subject_improved, snippet_improved])

    # get length of longest subject string
    # max_len = 0
    # for s in scholar:
    #     max_len = max(max_len, len(s[0]))
    # max_len += 2 # some margin for better printing

    # scholar text
    scholar_text=''
    for s in scholar:
        # scholar_text += f"- {s[0]:<{max_len}}{s[1]}\n"
        scholar_text += f"- **{s[0]}**: {s[1]}\n"

    scholar_text_before_llm = copy.deepcopy(scholar_text)

    
    # model = 'gemma3:4b'
    model = 'gemma3:12b'

    # llm parsing
    print('Running: LLM parsing...')
    prompt = f"""
    The text below is a bullet point list.
    Each bullet point reports the reference author in bold, the title, the complete list of authors, and additional information.
    Remove the complete list of authors and the additional information **after** the title of each bullet point.
    Keep the reference author and the title, as they are now.

    Example of input bullet point:
    - **Subhasish Mitra**: Generalized qed pre-silicon verification framework S Mitra, C BARRETT, CJ Trippel, S Chattopadhyay - US Patent App. 18/541722, 2025 Abstract Systems and methods of verifying a hardware processing

    Output should be:
    - **Subhasish Mitra**: Generalized qed pre-silicon verification framework

    Return the modified text without any comment or request from you.
    {scholar_text_before_llm}
    """
    scholar_text_after_llm = ollama(prompt=prompt, model=model)

    # # llm summary
    # print('Running: LLM summary...')
    # prompt = f"""
    # Summarize the content of these papers.
    # Do not ask questions or add comments.
    # {scholar_text_before_llm}
    # """
    # scholar_summary = ollama(prompt=prompt, model=model)

    # add headers
    scholar_text_before_llm = 'Google Scholar - New Articles\n' + scholar_text_before_llm
    scholar_text_after_llm = 'Google Scholar - New Articles\n' + scholar_text_after_llm
    # scholar_summary = 'Google Scholar - Summary\n' + scholar_summary

    # print
    print('')
    print(scholar_text_before_llm)
    print('')
    print(scholar_text_after_llm)
    print('')
    # print(scholar_summary)
    # print('')