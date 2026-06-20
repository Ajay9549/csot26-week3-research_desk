
import os
import sys
import json
import glob as glob_module
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

WORKSPACE_ROOT = os.path.abspath(os.environ.get("WORKSPACE_ROOT", "."))
MAX_ITERATIONS = 10
MAX_READ_CHARS = 12_000

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = "nex-agi/nex-n2-pro:free"


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


TOOLS = []


class Agent:
    """Core agent: loop, tools, sessions. No UI."""

    def __init__(self, workspace=".", session_id=None):

        self.workspace = os.path.abspath(workspace)

        self.session_id = (
            session_id
            or "default"
        )

        self.messages = [
            {
                "role": "system",
                "content": build_system_prompt()
            }
        ]

    def chat(self, user_message: str) -> str:

        self.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        answer = self._run_loop()

        return answer

    def run_once(self, prompt: str) -> str:
        return self.chat(prompt)

    def _run_loop(self) -> str:

        response = client.chat.completions.create(
            model=MODEL,
            messages=self.messages
        )

        answer = response.choices[0].message.content

        self.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return answer

    def dispatch(self, tool_call) -> str:

        return json.dumps(
            {
                "status": "tool dispatch placeholder"
            }
        )

    def _emit(self, event: str, **data) -> None:
        pass


class REPLAgent(Agent):
    """Terminal REPL + one-shot CLI."""

    def run(self) -> None:
        print(f"Research Desk [{self.session_id}] — /quit to exit")
        while True:
            try:
                user_input = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not user_input or user_input in ("/quit", "/exit"):
                break
            print(self.chat(user_input))
            print()

    def _emit(self, event: str, **data) -> None:
        if event == "tool_call":
            print(f"  [tool] {data.get('name')}", file=sys.stderr)


def build_system_prompt() -> str:

    prompt = "You are Research Desk, a helpful research assistant."

    for path in (
        "AGENTS.md",
        ".agent/AGENTS.md"
    ):

        if os.path.exists(path):

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                prompt += "\n\n" + f.read()

            break

    return prompt


def main():
    agent = REPLAgent()
    if len(sys.argv) > 1:
        print(agent.run_once(" ".join(sys.argv[1:])))
        return
    agent.run()


if __name__ == "__main__":
    main()