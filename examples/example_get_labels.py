"""Get all labels from your Gmail"""

from parsemind import call_gmail_api, get_labels

service = call_gmail_api()
labels = get_labels(service)

print("Labels in your Gmail account:")
for label in labels:
    print(f"\t{label['name']}")
