import os
from pathlib import Path
from unittest.mock import MagicMock

hw_path: str = str(Path(__file__).resolve().parent.parent.joinpath("hw14"))
os.environ["PATH"] += os.pathsep + hw_path
os.environ["PYTHONPATH"] += os.pathsep + hw_path

from src.database.models import User