from typing import List, Tuple
from converter.converter_config import TOOLS
from converter.converter_config.system_prompt import SYSTEM_PROMPT
import enchant
from enchant.checker import SpellChecker
import re


def get_ignored_words() -> List[str]:
    """
    Returns a list of words to ignore during spell check.
    """
    return [
        "britive's", "britive", "eq", "sw", "neq", "nco", "aws", "checkin", "whoami", "mcp", "otp",
        "xyz", "userids", "papids", "firstname", "usedin", "ai", "checkedout"
    ]


def split_camel_case(word: str) -> List[str]:
    """
    Splits a camelCase or PascalCase word into individual components.
    """
    return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', word)


def is_word_valid(word: str, dictionary: enchant.Dict, ignored_words: List[str]) -> bool:
    """
    Check if a word or its split parts are valid.
    """
    word_lower = word.lower()
    if word_lower in ignored_words:
        return True
    parts = split_camel_case(word)
    return all(dictionary.check(part) or part.lower() in ignored_words for part in parts)


def format_spell_check_error(source: str, spell_check_err_info: List[Tuple[str, str]]) -> str:
    """
    Format a readable error message for spell check.
    """
    error = [f"Spell Check error found in {source}"]
    for word, context in spell_check_err_info:
        error.append(f"  • Misspelled '{word}'. Context: '{context}{word}'")
    return "\n".join(error)


def run_spell_check(text: str, source: str, dictionary: enchant.Dict, ignored_words: List[str]) -> None:
    """
    Run spell check on the given text and print formatted errors.
    """
    checker = SpellChecker(lang="en_US", text=text)
    spell_check_err_info = []

    for err in checker:
        if not is_word_valid(err.word, dictionary, ignored_words):
            spell_check_err_info.append((err.word, checker.leading_context(10)))

    if spell_check_err_info:
        print(format_spell_check_error(source, spell_check_err_info))


def spell_check_system_prompt(dictionary: enchant.Dict, ignored_words: List[str]) -> None:
    """
    Spell check the SYSTEM_PROMPT string.
    """
    run_spell_check(SYSTEM_PROMPT, "SYSTEM_PROMPT", dictionary, ignored_words)


def spell_check_tools(dictionary: enchant.Dict, ignored_words: List[str]) -> None:
    """
    Spell check all tool descriptions in TOOLS.
    """
    for controller, tool_list in TOOLS.items():
        for tool in tool_list:
            source = f"{controller}:{tool.tool_name or tool.function_name}"
            run_spell_check(tool.ai_description, source, dictionary, ignored_words)


def main():
    dictionary = enchant.Dict("en_US")
    ignored_words = get_ignored_words()

    spell_check_system_prompt(dictionary, ignored_words)
    spell_check_tools(dictionary, ignored_words)

    print("✅ Successfully ran Spell Check on SYSTEM_PROMPT and tool descriptions.")


if __name__ == "__main__":
    main()
