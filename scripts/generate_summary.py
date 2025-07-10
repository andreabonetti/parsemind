"""Get all labels from your Gmail"""

from parsemind import get_summary

if __name__ == "__main__":
    # using debug mode for faster operation
    get_summary(
        scholar=True,
        markdown=True,
        do_print=True,
        debug=True,
    )
