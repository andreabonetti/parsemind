"""Update markdown homepage"""

from parsemind import update_markdown_homepage

if __name__ == '__main__':
    # parameters
    output_folder = 'output'
    markdown_file = 'parsemind.md'

    # main
    update_markdown_homepage(
        output_folder=output_folder,
        markdown_file=markdown_file,
    )
