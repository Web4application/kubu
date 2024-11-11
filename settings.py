# myproject/settings.py
import os

INSTALLED_APPS = [
...
'Roda',
]

# Add your OpenAI API key here
OPENAI_API_KEY = os.getenv('AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10')
