import os
import json
import logging
import torch
from cpufeature import CPUFeature
from petals.constants import PUBLIC_INITIAL_PEERS
from dataclasses import dataclass
from typing import Optional

# Load configuration from a JSON file
def load_config(config_path='config.json'):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

config = load_config()

# Setup logging
def setup_logging(log_level=logging.INFO):
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logging()
logger.info("Kubu-Hai package initialized")

# Utility function
def print_welcome_message():
    print("Welcome to the Kubu-Hai AI package!")

print_welcome_message()

# ModelInfo class
@dataclass
class ModelInfo:
    repo: str
    adapter: Optional[str] = None

# Model configurations
MODELS = [
    ModelInfo(repo="meta-llama/Llama-2-70b-chat-hf"),
    ModelInfo(repo="stabilityai/StableBeluga2"),
    ModelInfo(repo="enoch/llama-65b-hf"),
    ModelInfo(repo="enoch/llama-65b-hf", adapter="timdettmers/guanaco-65b"),
    ModelInfo(repo="bigscience/bloomz"),
]
DEFAULT_MODEL_NAME = "enoch/llama-65b-hf"

INITIAL_PEERS = PUBLIC_INITIAL_PEERS
# Set this to a list of multiaddrs to connect to a private swarm instead of the public one, for example:
# INITIAL_PEERS = ['/ip4/10.1.2.3/tcp/31234/p2p/QmcXhze98AcgGQDDYna23s4Jho96n8wkwLJv78vxtFNq44']

DEVICE = "cpu"

if DEVICE == "cuda":
    TORCH_DTYPE = "auto"
elif CPUFeature["AVX512f"] and CPUFeature["OS_AVX512"]:
    TORCH_DTYPE = torch.bfloat16
else:
    TORCH_DTYPE = torch.float32  # You can use bfloat16 in this case too, but it will be slow

STEP_TIMEOUT = 5 * 60
MAX_SESSIONS = 50  # Has effect only for API v1 (HTTP-based)

# Importing necessary modules from the package
from .ai_kubu import some_function
from .ai_main import main_function
from .ai_model import build_model

# Package-level variable
__version__ = '1.0.0'

# Initialization code
def initialize():
    print("Kubu-Hai package initialized")

# Define what gets imported when using 'from package import *'
__all__ = ['some_function', 'main_function', 'build_model', 'initialize', 'load_config', 'setup_logging', 'print_welcome_message']
