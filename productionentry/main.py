from productionentry.utils import error_logging_decorator
from productionentry.db.sqlite.utils import initialise_db


@error_logging_decorator
def main():
    initialise_db()


if __name__ == "__main__":
    main()
