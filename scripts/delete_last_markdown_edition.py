from parsemind import delete_last_markdown_edition

if __name__ == '__main__':
    # parameters
    output_folder = 'output'
    markdown_file = 'parsemind.md'

    # delete last markdown edition
    delete_last_markdown_edition(
        output_folder=output_folder,
        markdown_file=markdown_file,
    )