"""Generate summary"""

from parsemind import get_weeks_after, get_summary
from datetime import datetime, timedelta

if __name__ == "__main__":
    # dates
    today_date = datetime.today().date() - timedelta(days=14)
    today_str = today_date.strftime("%Y-%m-%d")
    weeks = get_weeks_after(today_str)
    # you should have received only a single set of dates, let's check that
    if len(weeks) != 1:
        raise Exception('The number of start/end dates should be one.')
    dates = weeks[0]

    # summary
    get_summary(
        dates=dates,
        scholar=True,
        markdown=True,
        do_print=True,
        debug=True
    )
