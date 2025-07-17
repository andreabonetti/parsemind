from parsemind import call_gmail_api, get_messages_from_query


def main():
    service = call_gmail_api()

    # query
    q = """
    from:newsletter@semi-mags.com
    label:newsletters
    after:2025-07-01
    """

    # get messages from query
    content_list = get_messages_from_query(
        service=service,
        q=q,
    )

    # get the last message content
    content = content_list[0]

    # print
    my_text = '\n'
    my_text += f'subject: {content["subject"]}\n\n'
    my_text += f'sender: {content["sender"]}\n\n'
    my_text += f'snippet: {content["snippet"]}\n\n'
    my_text += f'plain_text_body: {content["plain_text_body"]}\n\n'
    print(my_text)

    return True  # for testing


if __name__ == '__main__':
    main()
