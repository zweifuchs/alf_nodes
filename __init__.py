"""
ALF Nodes package initialization.
Provides timestamp and resolution utility nodes for ComfyUI.
"""


# from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
from .nodes.timestamp import ALF_Timestamp
from .nodes.resolutions_by_ratio import ALF_Resolutions_by_Ratio
from .nodes.dynamic_text import ALF_DynamicText
from .nodes.showText import ALF_ShowText



# Constants
VERSION = "1.0.1"
MAX_RESOLUTION = 8192  # Common max resolution for most GPUs

def print_banner() -> None:
    """Print the ASCII art banner with version information."""
    print(f"""
    ___    __    ______   _   __           __
   /   |  / /   / ____/  / | / /___  ____/ /__  _____
  / /| | / /   / /_     /  |/ / __ \/ __  / _ \/ ___/
 / ___ |/ /___/ __/    / /|  / /_/ / /_/ /  __(__  )
/_/  |_/_____/_/      /_/ |_/\____/\__,_/\___/____/
=================================================
              Custom Nodes Package
                 by ALF - v{VERSION}
=================================================
""")


# Specify web directory for JavaScript files
WEB_DIRECTORY = "./web"

print("✓ Successfully loaded ALF Nodes")


# Initialize nodes
print_banner()
print("Initializing ALF Nodes...")

NODE_CLASS_MAPPINGS = {
    "ALF_Timestamp": ALF_Timestamp,
    "ALF_Resolutions_by_Ratio": ALF_Resolutions_by_Ratio,
    "ALF_DynamicText": ALF_DynamicText,
    "ALF_ShowText": ALF_ShowText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ALF_Timestamp": "ALF - Timestamp Filename Generator",
    "ALF_Resolutions_by_Ratio": "ALF - Resolutions by Aspect Ratio",
    "ALF_DynamicText": "ALF - Dynamic Text Generator",
    "ALF_ShowText": "ALF - Show Text"
}

print(f"✓ ALF Nodes v{VERSION} registered successfully")
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
