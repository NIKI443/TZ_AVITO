from dotenv import load_dotenv


def pytest_configure():
    load_dotenv(".env", override=True)

pytest_plugins = ["tests.fixtures"]
