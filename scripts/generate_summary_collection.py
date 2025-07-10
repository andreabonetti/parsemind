"""Generate collection of summaries after a given date."""

from parsemind import get_weeks_after, get_summary, update_markdown_homepage
from datetime import datetime, timedelta
from pathlib import Path
import os

def get_markdown_edition(markdown_file, dates):
    return markdown_file.replace('.md', f"_{dates['range_date']}.md")

if __name__ == "__main__":
    # parameters
    output_folder='output'
    markdown_file='parsemind.md'

    # dates
    reference_date = datetime.today().date() - timedelta(days=21)
    reference_str = reference_date.strftime("%Y-%m-%d")
    weeks = get_weeks_after(reference_str)

    # select only the weeks of the editions that have not been generated yet
    for i, dates in enumerate(weeks):
        # name of the markdown edition
        markdown_edition = get_markdown_edition(markdown_file, dates)

        # check if file exists. If so, removes the date
        markdown_edition_path = Path(output_folder) / markdown_edition
        if markdown_edition_path.exists():
            del weeks[i]


    # generate editions
    for dates in weeks:
        # name of the markdown edition
        markdown_edition = get_markdown_edition(markdown_file, dates)

        # summary
        get_summary(
            dates=dates,
            scholar=True,
            markdown=True,
            output_folder=output_folder,
            markdown_file=markdown_edition, # edition,
            debug=True,
        )

    # update markdown homepage
    update_markdown_homepage(
        output_folder=output_folder,
        markdown_file=markdown_file,
    )
