from converter.converter_config import TOOLS
from converter.converter_config.system_prompt import SYSTEM_PROMPT
from typing import List, Tuple
import enchant
from enchant.checker import SpellChecker


def format_spell_check_error(source: str, spell_check_err_info: List[Tuple[str, str, str]]) -> str:
    """
    Format a readable error message for spell check.
    """
    error = [f"Spell Check error found in {source}"]
    for word, start, suggestions in spell_check_err_info:
        error.append(f"  • Misspelled '{word}'. Context: '{start}|{word}'. Suggestions: {suggestions}")
    return "\n".join(error)


def spell_check_in_system_prompt():
    checker = SpellChecker(lang="en_US", text=SYSTEM_PROMPT)
    spell_check_err_info = [
        (
            err.word, 
            checker.leading_context(10), 
            enchant.Dict("en_US").suggest(err.word)[:2]
        ) 
        for err in checker
    ]
    if spell_check_err_info:
        print(format_spell_check_error("SYSTEM_PROMPT", spell_check_err_info))


def spell_check_in_tools():
    for controller, tool_list in TOOLS.items():
        for tool in tool_list:
            checker = SpellChecker(lang="en_US", text=tool.ai_description)
            spell_check_err_info = [
                (
                    err.word, 
                    checker.leading_context(10), 
                    enchant.Dict("en_US").suggest(err.word)[:2]
                ) 
                for err in checker
            ]
            if spell_check_err_info:
                source = f"{controller}:{tool.function_name}"
                print(format_spell_check_error(source, spell_check_err_info))


def main():
    spell_check_in_system_prompt()
    spell_check_in_tools()
    print("✅ Successfully ran Spell Check on SYSTEM_PROMPT and tool descriptions.")


if __name__ == "__main__":
    main()
