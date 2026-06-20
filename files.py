
import os
import glob as glob_module

WORKSPACE_ROOT = os.path.abspath(os.environ.get("WORKSPACE_ROOT", "."))
# --- File tools ---

def resolve_path(path: str) -> str:
    return os.path.abspath(os.path.join(WORKSPACE_ROOT, path))


def read_file(path: str, start_line: int = 1, read_lines: int = 200) -> dict:
    full_path = resolve_path(path)

    with open(full_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    end = start_line - 1 + read_lines

    return {
        "content": "".join(lines[start_line - 1:end])
    }


def write_file(path: str, content: str) -> dict:
    full_path = resolve_path(path)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {"status": "success"}


def edit_file(
    path: str,
    operation: str,
    start_line: int,
    end_line: int | None = None,
    content: str | None = None,
) -> dict:

    full_path = resolve_path(path)

    with open(full_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if operation == "replace":
        lines[start_line - 1:end_line] = [content + "\n"]

    with open(full_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return {"status": "success"}


def list_files(path: str = ".", pattern: str = "*") -> dict:
    full_path = resolve_path(path)

    files = glob_module.glob(
        os.path.join(full_path, pattern)
    )

    return {"files": files}
