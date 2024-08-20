import os

from dotenv import load_dotenv

from .base import BASE_DIR

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Get the MODE environment variable.
MODE = os.environ.get("MODE")

# Depending on the MODE, import the corresponding configuration settings
if MODE == "development":
    from .development import *
elif MODE == "production":
    from .production import *
else:
    # If MODE is neither 'development' nor 'production', raise an exception
    # Raises: Exception with a descriptive error message
    raise Exception(
        "MODE environment variable must be set to either 'development' or 'production'"
    )
