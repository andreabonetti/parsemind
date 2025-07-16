from parsemind import call_gmail_api, send_email

if __name__ == '__main__':
    service = call_gmail_api()

    print('This script will send a test email to the address that you specify:')

    # get email address from console
    to = input()

    # send email
    send_email(service=service, sender='', to=to, subject='Parsemind is...', body='...cool.')

    print('Email has been sent.')
