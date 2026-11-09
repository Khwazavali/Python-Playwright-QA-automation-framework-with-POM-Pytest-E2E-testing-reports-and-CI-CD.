
import os

DEFAULT_BASE_URL = "https://www.saucedemo.com/"

BASE_URL = os.getenv(
    "BASE_URL",
    DEFAULT_BASE_URL
).rstrip("/")
