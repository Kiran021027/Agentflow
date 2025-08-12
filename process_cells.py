import json

def create_llm_prompt_from_json(json_string):
    """
    Parses a JSON string and formats a list of cells into a single string for an LLM prompt.

    Args:
        json_string (str): A JSON string containing a list of cells.

    Returns:
        str: A formatted string combining all cells.
    """
    try:
        data = json.loads(json_string)
        # Handle both a list of cells, or an object with a "cells" key
        if isinstance(data, list):
            cells = data
        else:
            cells = data.get('cells', [])
    except json.JSONDecodeError:
        return "Error: Invalid JSON format."

    prompt_parts = []
    for cell in cells:
        cell_id = cell.get('cell_id', 'N/A')
        source = cell.get('source', [])
        # The source is a list of strings, join them. They should already have newlines if they are lines of code.
        source_code = "".join(source)

        formatted_cell = (
            f"---\n"
            f"Cell ID: {cell_id}\n"
            f"Code:\n{source_code}"
            f"\n---"
        )
        prompt_parts.append(formatted_cell)

    return "\n\n".join(prompt_parts)


if __name__ == '__main__':
    # Example usage:
    sample_json_string = """
    {
        "cells": [
            {
                "cell_id": "cell-1",
                "source": [
                    "def hello_world():\\n",
                    "    print(\\"Hello, World!\\")"
                ]
            },
            {
                "cell_id": "cell-2",
                "source": [
                    "hello_world()"
                ]
            }
        ]
    }
    """

    formatted_prompt = create_llm_prompt_from_json(sample_json_string)
    print(formatted_prompt)

    # Test case
    expected_output = """---
Cell ID: cell-1
Code:
def hello_world():
    print("Hello, World!")
---

---
Cell ID: cell-2
Code:
hello_world()
---"""

    # To make the test robust against small whitespace differences
    # We compare by removing all whitespace characters
    assert "".join(formatted_prompt.split()) == "".join(expected_output.split())

    print("\\n\\nTest passed!")

    print("\\n--- Testing raw list input ---")
    # Test case for raw list input
    sample_json_list_string = """
    [
        {
            "cell_id": "list-cell-1",
            "source": ["print('hello from list')"]
        }
    ]
    """

    formatted_prompt_from_list = create_llm_prompt_from_json(sample_json_list_string)
    print(formatted_prompt_from_list)

    expected_list_output = """---
Cell ID: list-cell-1
Code:
print('hello from list')
---"""

    assert "".join(formatted_prompt_from_list.split()) == "".join(expected_list_output.split())
    print("\\nTest for raw list passed!")
