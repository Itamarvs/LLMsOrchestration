import sys
import os
from pathlib import Path

# Add project root to sys.path so that 'src' and 'DEEPFAKE' can be imported
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))
