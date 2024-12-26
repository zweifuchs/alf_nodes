import datetime
import os
from typing import Tuple, Dict, Any, Union, List


class ALF_Timestamp:
    """
    Node for generating timestamp-based filenames and paths.

    Outputs:
        - STRING: A formatted path string including timestamp and optional prefix/postfix
    """

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        """Define the input types and default values for the node."""
        return {
            "required": {},
            "hidden": { "node_id": "UNIQUE_ID" },
            "optional": {
                "prefix": ("STRING", {"default": ""}),
                "postfix": ("STRING", {"default": ""}),
                "subfolder": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_timestamp"
    CATEGORY = "alf_nodes/utils"

    def get_timestamp_parts(self) -> Tuple[str, str]:
        """
        Generate the current timestamp parts.

        Returns:
            Tuple containing (date_folder, time_string)
        """
        now = datetime.datetime.now()
        date_folder = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%Y-%m-%d-%H%M%S")
        return date_folder, time_str

    def generate_timestamp(self, node_id, prefix: str = "", postfix: str = "", subfolder: str = "") -> Tuple[str]:
        """
        Generate a timestamp-based filename with optional prefix, postfix, and subfolder.

        Args:
            prefix: Optional prefix for the filename
            postfix: Optional postfix for the filename
            subfolder: Optional subfolder path

        Returns:
            Tuple containing the full path as a string
        """
        date_folder, time_str = self.get_timestamp_parts()

        # Clean up inputs
        prefix = prefix.strip()
        postfix = postfix.strip()
        subfolder = subfolder.strip()

        # Construct filename
        filename_parts = []
        if prefix:
            filename_parts.append(prefix)
        filename_parts.append(time_str)
        if postfix:
            filename_parts.append(postfix)
        filename = "_".join(filename_parts)

        # Construct path
        path_parts = [date_folder]
        if subfolder:
            subfolders = [f for f in subfolder.replace('\\', '/').split('/') if f]
            path_parts.extend(subfolders)

        full_path = os.path.join(*path_parts, filename)
        print(f"Generated path: {full_path}")
        return (full_path,)

    @classmethod
    def IS_CHANGED(cls, node_id, prefix: str = "", postfix: str = "", subfolder: str = "") -> float:
        """Always return NaN to ensure the node updates on every execution."""
        return float("nan")
