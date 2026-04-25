import os

import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/e5-base-v2")
DEVICE = os.getenv("DEVICE", "cpu")

HF_TOKEN = os.getenv("HF_TOKEN")


# Base workspace directory
WORKSPACE_DIR = "workspace"

# Supported extensions
SUPPORTED_LANGUAGES = {
    ".py": "python",
    ".java": "java"
}

EMBEDDING_MODEL = "intfloat/e5-base-v2"
DEVICE = "cpu"   # or "cuda" if GPU