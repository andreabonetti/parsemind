"""Get weeks after a certain date"""

from parsemind import get_weeks_after
from datetime import datetime, timedelta

def print_vocab_recursively(d, indent=0):
    """Recursively print a dictionary with indentation."""
    for key, value in d.items():
        print('  ' * indent + str(key) + ':', end=' ')
        if isinstance(value, dict):
            print()  # newline before nested dict
            print_vocab_recursively(value, indent + 1)
        else:
            print(str(value))


def main():
    some_weeks_ago = datetime.today().date() - timedelta(days=21)
    some_weeks_ago_str = some_weeks_ago.strftime("%Y-%m-%d")

    weeks = get_weeks_after(some_weeks_ago_str)

    for week in weeks:
        print_vocab_recursively(week)
        print('')

    return True # for testing


if __name__ == "__main__":
    main()
