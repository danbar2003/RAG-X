import os
import re
import mimetypes


def extract_symbols_from_directory(directory_path):
    """
    Extracts all symbols (variables, functions, and classes) from Python source files in the given directory.

    :param directory_path: The path of the project directory to scan for source files.
    :return: A list of dictionaries, each containing the symbol's name, type, file path, and code snippet.
    """
    symbols = []

    # Walk through the directory to find Python files
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_text_file(file_path) and file.endswith(".py"):
                symbols += extract_symbols_from_file(file_path)

    return symbols


def is_text_file(file_path):
    """
    Checks if a file is a textual file using mimetypes.
    :param file_path: The file to check.
    :return: True if the file is a text file, False otherwise.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("text")


def extract_symbols_from_file(file_path):
    """
    Extracts symbols (functions, classes, variables, imports) from a single Python file using regex.

    :param file_path: The source file path.
    :return: List of dictionaries with symbol information.
    """
    symbols = []
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    # Define regex patterns to match different symbols in Python

    # Match function definitions
    function_pattern = r"^\s*def\s+(\w+)\s*\(.*\):"
    # Match class definitions
    class_pattern = r"^\s*(class)\s+(\w+)\s*\(.*\):"
    # Match variable declarations (ignores assignment, just captures variable names)
    variable_pattern = r"^\s*(\w+)\s*="
    # Match import statements (including `import ...` and `from ... import ...`)
    import_pattern = r"^\s*(import\s+\w+|\s*from\s+\w+\s+import\s+\w+)"

    # Extract function names
    functions = re.findall(function_pattern, code, re.MULTILINE)
    for func in functions:
        symbols.append(
            {
                "name": func,
                "type": "function",
                "file_path": file_path,
                "snippet": get_code_snippet(file_path, func),
            }
        )

    # Extract class names
    classes = re.findall(class_pattern, code, re.MULTILINE)
    for _, cls in classes:
        symbols.append(
            {
                "name": cls,
                "type": "class",
                "file_path": file_path,
                "snippet": get_code_snippet(file_path, cls),
            }
        )

    # Extract variable names
    variables = re.findall(variable_pattern, code, re.MULTILINE)
    for var in variables:
        symbols.append(
            {
                "name": var,
                "type": "variable",
                "file_path": file_path,
                "snippet": get_code_snippet(file_path, var),
            }
        )

    # Extract import statements
    imports = re.findall(import_pattern, code, re.MULTILINE)
    for imp in imports:
        symbols.append(
            {
                "name": imp,
                "type": "import",
                "file_path": file_path,
                "snippet": get_code_snippet(file_path, imp),
            }
        )

    return symbols


def get_code_snippet(file_path, symbol_name, context_lines=3):
    """
    Extracts a small code snippet around the given symbol.

    :param file_path: The file from which the code should be extracted.
    :param symbol_name: The symbol name (function, class, variable).
    :param context_lines: Number of lines before and after the symbol to include in the snippet.
    :return: A small code snippet as a string.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Search for the line where the symbol is defined
    start_line = None
    for i, line in enumerate(lines):
        if re.search(
            rf"\b{re.escape(symbol_name)}\b", line
        ):  # Safely find the symbol by name
            start_line = i
            break

    if start_line is None:
        return ""

    # Get a snippet around the symbol (context_lines before and after)
    start = max(start_line - context_lines, 0)
    end = min(start_line + context_lines + 1, len(lines))

    snippet = "".join(lines[start:end]).strip()

    return snippet
