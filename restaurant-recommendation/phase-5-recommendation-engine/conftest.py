"""Root conftest for Phase 5 recommendation engine tests."""

import sys
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Add phase directories to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "phase-3-preference-processing"))
sys.path.insert(0, str(project_root / "phase-4-llm-integration"))
