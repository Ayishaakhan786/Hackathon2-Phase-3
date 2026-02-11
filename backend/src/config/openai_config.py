from openai import AsyncOpenAI
from ..config.settings import settings


# Configure OpenAI client
client = AsyncOpenAI(api_key=settings.openai_api_key)


def get_openai_client():
    """
    Returns the configured OpenAI client
    """
    return client


# Define the model to use
OPENAI_MODEL = settings.openai_model