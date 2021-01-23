import requests
import sys
import json
import functools


def check_for_request_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            print("Cannot establish connection")
            print("Full error message: ")
            print(e)
            sys.exit(1)
        except requests.exceptions.Timeout as e:
            print("Request timed out")
            print("Full error message: ")
            print(e)
            sys.exit(1)
        except requests.exceptions.HTTPError as e:
            print("An HTTP error occurred")
            print("Full error message: ")
            print(e)
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print("An SSL error occurred")
            print("Full error message: ")
            print(e)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print("Something went wrong. Check your request")
            print("Full error message: ")
            print(e)
            sys.exit(1)

    return wrapper

