from converter.converter_config import TOOLS
from converter.converter_config.system_prompt import SYSTEM_PROMPT
from typing import List, Tuple

def find_unicode_characters(text: str) -> List[Tuple[int, str, int]]:
    """
    Find all non-ASCII characters in the given string.

    Returns:
        A list of tuples: (index, character, unicode_code_point)
    """
    return [(i, char, text[i-10 : i+10]) for i, char in enumerate(text) if ord(char) > 127]


def format_unicode_error(source: str, unicode_info: List[Tuple[int, str, int]]) -> str:
    """
    Format a readable error message for found unicode characters.
    """
    error = [f"Unicode characters found in {source}"]
    for index, char, code_point in unicode_info:
        error.append(f"  • Position {index}: '{char}'\n    → Found in: [{code_point}]")
    return "\n".join(error)


def check_unicode_in_system_prompt():
    unicode_info = find_unicode_characters(SYSTEM_PROMPT)
    if unicode_info:
        raise ValueError(format_unicode_error("SYSTEM_PROMPT", unicode_info))


def check_unicode_in_tools():
    for controller, tool_list in TOOLS.items():
        for tool in tool_list:
            unicode_info = find_unicode_characters(tool.ai_description)
            if unicode_info:
                source = f"{controller}:{tool.function_name}"
                raise ValueError(format_unicode_error(source, unicode_info))


def main():
    check_unicode_in_system_prompt()
    check_unicode_in_tools()
    print("✅ No Unicode characters found in SYSTEM_PROMPT or tool descriptions.")


if __name__ == "__main__":
    main()
