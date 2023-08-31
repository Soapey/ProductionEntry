import os
import random
import string
import datetime
import traceback


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def error_logging_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            random_string = generate_random_string(8)
            current_date = datetime.datetime.now().strftime("%d%m%y")
            file_name = f"{random_string}_{current_date}.txt"
            error_log_path = os.path.join("error_logs", file_name)
            simple_error_message = f"An error occurred in {func.__name__}: {str(e)}"
            traceback_info = traceback.format_exc()
            with open(error_log_path, "a") as f:
                f.write(f"{simple_error_message}\n{traceback_info}")
            raise  # Reraise the exception after logging
    return wrapper


def project_folder():
    return os.path.abspath(".")


def join_to_project_folder(relative_path):
    return os.path.join(project_folder(), relative_path)
