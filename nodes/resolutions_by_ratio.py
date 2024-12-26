from typing import Dict, Any, Tuple, Union, List
import random

MAX_RESOLUTION = 8192  # Common max resolution for most GPUs

class ALF_Resolutions_by_Ratio:
    """
    Node for calculating image resolutions based on aspect ratios.
    Supports deterministic random direction selection via seed.

    Outputs:
        - INT: Width in pixels
        - INT: Height in pixels
    """

    aspects = ["1:1", "6:5", "5:4", "4:3", "3:2", "16:10", "16:9", "21:9", "43:18", "2:1", "3:1", "4:1"]
    directions = ["landscape", "portrait", "random"]

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        """Define the input types and default values for the node."""
        return {
            "required": {
                "aspect": (cls.aspects,),
                "direction": (cls.directions,),
                "shortside": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": MAX_RESOLUTION,
                    "step": 64
                })
            },
            "optional": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                })
            },
            "hidden": { "node_id": "UNIQUE_ID" },

        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "get_resolutions"
    CATEGORY = "alf_nodes/utils"

    def get_resolutions(self, node_id, aspect: str, direction: str, shortside: int, seed: int = 0) -> Tuple[int, int]:
        """
        Calculate width and height based on aspect ratio and shortest side length.

        Args:
            aspect: Aspect ratio string in format "x:y"
            direction: Either "landscape", "portrait", or "random"
            shortside: Length of the shortest side in pixels
            seed: Random seed for deterministic direction selection

        Returns:
            Tuple of (width, height) in pixels
        """
        try:
            x, y = map(int, aspect.split(':'))
            ratio = x / y

            width = int(shortside * ratio)
            # Round up to nearest multiple of 64
            width = (width + 63) & (-64)
            height = shortside

            if direction == "random":
                # Use seed for deterministic random choice
                rng = random.Random(seed)
                direction = rng.choice(["landscape", "portrait"])
                print(f"Random direction chosen (seed {seed}): {direction}")

            if direction == "portrait":
                width, height = height, width

            # Validate final dimensions
            if width > MAX_RESOLUTION or height > MAX_RESOLUTION:
                print(f"Warning: Dimensions {width}x{height} exceed MAX_RESOLUTION of {MAX_RESOLUTION}")
                return (512, 512)

            return (width, height)

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error calculating resolutions: {str(e)}")
            return (512, 512)  # Safe default

    @classmethod
    def IS_CHANGED(cls, direction: str, seed: int, aspect: str, shortside: int, node_id: str):
        """Return NaN only when direction is 'random' to ensure randomization."""
        if direction == "random":
            return seed
        return (f"{direction}_{aspect}_{shortside}")

