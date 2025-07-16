"""Generate collection of summaries after a given date."""

from datetime import datetime, timedelta
from pathlib import Path

from parsemind import get_summary, get_weeks_after, update_markdown_homepage


def get_markdown_edition(markdown_file, dates):
    return markdown_file.replace('.md', f'_{dates["range_date"]}.md')


if __name__ == '__main__':
    # parameters
    output_folder = 'output'
    markdown_file = 'parsemind.md'

    # dates
    reference_date = datetime.today().date() - timedelta(days=21)
    reference_str = reference_date.strftime('%Y-%m-%d')
    weeks = get_weeks_after(reference_str)

    # select only the weeks of the editions that have not been generated yet
    weeks = [dates for dates in weeks if not (Path(output_folder) / get_markdown_edition(markdown_file, dates)).exists()]

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
            markdown_file=markdown_edition,  # edition,
        )

    # update markdown homepage
    update_markdown_homepage(
        output_folder=output_folder,
        markdown_file=markdown_file,
    )
