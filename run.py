__author__ = "Shivam Shekhar"
made_by = "OldKokiri-6"


from src.game import *


def main():
    db.init_db()
    isGameQuit = introscreen()
    if not isGameQuit:
        introscreen()


if __name__ == "__main__":
    main()