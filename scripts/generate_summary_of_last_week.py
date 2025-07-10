"""Generate summary of last week"""

from parsemind import get_weeks_after, get_summary
from datetime import datetime, timedelta

if __name__ == "__main__":
    # dates
    reference_date = datetime.today().date() - timedelta(days=14)
    reference_str = reference_date.strftime("%Y-%m-%d")
    weeks = get_weeks_after(reference_str)
    # you should have received only a single set of dates, let's check that
    if len(weeks) != 1:
        raise Exception('The number of start/end dates should be one.')
    dates = weeks[0]

    # summary
    get_summary(
        dates=dates,
        scholar=True,
        markdown=True,
        output_folder='output',
        markdown_file='parsemind_last_week.md',
        do_print=True
    )

