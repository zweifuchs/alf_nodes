from typing import Dict, Any, Tuple, Union, List
import random

class ALF_DynamicText:
    """
    Node for generating dynamic text with random choices from templates.
    Supports unlimited nested {a|b|c} syntax with empty options, counter-based cycling,
    and autoincrement.
    """

    def __init__(self):
        """Initialize instance-specific counter and debug log."""
        self.instance_counter = -1
        self.debug_log = []

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        """Define input types with current counter value."""
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Hello {fast|slow|{small|huge}} {green|red|blue} car!"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                }),
                "counter": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 0xffffffffffffffff
                }),
                "shuffle_mode": ("BOOLEAN", {
                    "default": False
                }),
                "autoincrement": ("BOOLEAN", {
                    "default": False
                })
            },
            "hidden": { "node_id": "UNIQUE_ID" },
            "optional": {
                "input_text": ("STRING",)
            }
        }

    RETURN_TYPES = ("STRING", "INT", "STRING")
    RETURN_NAMES = ("text", "counter", "debug")
    FUNCTION = "process_text"
    CATEGORY = "alf_nodes/text"

    def parse_pattern(self, text: str, pos: int = 0) -> Tuple[Union[str, List[str]], int]:
        """
        Parse a pattern starting at the given position.
        Handles nested patterns and empty options.

        Args:
            text: Input text to parse
            pos: Starting position

        Returns:
            Tuple of (parsed_result, new_position)
            parsed_result can be either a string or list of options
        """
        if pos >= len(text) or text[pos] != '{':
            return text[pos:], len(text)

        options = []
        current = []
        i = pos + 1  # Skip opening brace

        while i < len(text):
            char = text[i]

            if char == '{':
                # Start of nested pattern
                nested_result, new_pos = self.parse_pattern(text, i)
                if isinstance(nested_result, list):
                   current.append('{' + '|'.join(nested_result) + '}')
                else:
                   current.append(nested_result)
                i = new_pos

            elif char == '}':
                # End of current pattern
                options.append(''.join(current))
                return options, i + 1
            elif char == '|':
                # Option separator
                options.append(''.join(current))
                current = []
                i += 1
            else:
                current.append(char)
                i += 1

        # If we reach here, we had an unclosed pattern
        # Return the partial result as a string
        return text[pos:], len(text)

    def expand_pattern(self, pattern: Union[str, List[str]], debug_path: str = "") -> List[Tuple[str, str]]:
        """
        Recursively expand a pattern into all possible combinations, tracking choices.

        Args:
            pattern: Either a string or list of pattern options
            debug_path: String to track the choices made so far

        Returns:
            List of tuples, each containing (expanded string, debug path)
        """
        if isinstance(pattern, str):
            if '{' not in pattern:
                return [(pattern, debug_path)]

            # Find and expand all patterns in the string
            results = [('', debug_path)]
            i = 0
            while i < len(pattern):
                if pattern[i] == '{':
                    nested_pattern, new_pos = self.parse_pattern(pattern, i)
                    if isinstance(nested_pattern, list):
                        new_results = []
                        for j, option in enumerate(nested_pattern):
                            option_expanded = self.expand_pattern(
                                option,
                                debug_path + f"{{{j + 1}/{len(nested_pattern)}}}"
                            )
                            for result, path in results:
                                for expanded, sub_path in option_expanded:
                                    new_results.append((result + expanded, sub_path))
                        results = new_results
                        i = new_pos
                    else:
                        # Handle invalid pattern as literal
                        for j in range(len(results)):
                            results[j] = (results[j][0] + pattern[i], results[j][1])
                        i += 1
                else:
                    for j in range(len(results)):
                        results[j] = (results[j][0] + pattern[i], results[j][1])
                    i += 1
            return results

        # For a list of patterns, expand each one
        expanded = []
        for j, option in enumerate(pattern):
            expanded.extend(self.expand_pattern(option, debug_path + f"{{{j + 1}/{len(pattern)}}}" ))
        return expanded

    def get_combination(self, combinations: List[Tuple[str, str]], index: int) -> Tuple[str, str]:
        """Get a specific combination by index with wraparound."""
        if not combinations:
            return "", ""  # Handle empty combinations case
        return combinations[index % len(combinations)]

    @classmethod
    def IS_CHANGED(cls, node_id, text: str, seed: int, counter: int, input_text: str,
                   shuffle_mode: bool, autoincrement: bool) -> float:
        """Return NaN when autoincrement is enabled to ensure updates."""
        if autoincrement:
            print("Autoincrement enabled, forcing update")
            return f"{seed}_{counter}"
        print(f"Autoincrement disabled, returning seed: {seed}")
        return seed


    def process_text(self, text: str, node_id, seed: int = 0, counter: int = -1,
                    shuffle_mode: bool = False, autoincrement: bool = False,
                    input_text: str = None) -> Tuple[str, int, str]:
        """
        Process the input text, replacing {a|b|c} patterns with choices.

        Args:
            text: Input text with patterns
            seed: Random seed (used in normal mode)
            counter: Position counter (-1 for initial state)
            shuffle_mode: Whether to use shuffle mode
            autoincrement: Whether to automatically increment counter
            input_text: Optional prefix text

        Returns:
            Tuple of (processed_text, current_counter, debug_string)
        """
        self.debug_log = []  # Reset debug log

        try:
            # Get all possible combinations with debug paths
            combinations_with_paths = self.expand_pattern(text)
            total_combinations = len(combinations_with_paths)

            # Update counter state
            if counter == -1 and autoincrement:
                if self.instance_counter == -1:
                    self.instance_counter = 0
                else:
                    self.instance_counter = (self.instance_counter + 1) % total_combinations
            elif counter != -1:
                if counter != self.instance_counter:
                    self.instance_counter = counter
                elif autoincrement:
                    self.instance_counter = (self.instance_counter + 1) % total_combinations

            # Select combination
            if shuffle_mode:
                combination_index = self.instance_counter % total_combinations
            else:
                rng = random.Random(seed + self.instance_counter)
                combination_index = rng.randrange(total_combinations)

            result, debug_path = self.get_combination(combinations_with_paths, combination_index)

            # Add input_text if provided
            if input_text:
                result = f"{input_text.strip()} {result}"

            # Create debug string
            debug_string = f"'{text}' -> '{result}' {debug_path} (combination {combination_index + 1}/{total_combinations})"
            self.debug_log.append(debug_string)
            print(f"Generated text: {result} {debug_path} (combination {combination_index + 1}/{total_combinations})")
            print("----------------------------------")

            return (result, self.instance_counter, debug_string)

        except Exception as e:
            error_message = f"Error processing text: {str(e)}"
            self.debug_log.append(error_message)
            print(error_message)
            return (text, self.instance_counter, error_message)
