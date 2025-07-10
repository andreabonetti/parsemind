from parsemind import call_gmail_api
from parsemind import get_today_and_week_ago
from parsemind import get_scholar_summary

import copy

if __name__ == "__main__":
    # call gmail api
    service = call_gmail_api()
    # get dates
    dates = get_today_and_week_ago()
    # summary
    summary = get_scholar_summary(service=service, dates=dates, verbose=True)