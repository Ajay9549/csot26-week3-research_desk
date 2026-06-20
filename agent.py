
import os
import sys
import json
import glob as glob_module
from build1_sessions import (
    create_session,
    save_session,
    load_session,
)
from openai import OpenAI
from dotenv import load_dotenv
from tools.files import (
    read_file,
    write_file,
    edit_file,
    list_files,
)

from tools.web import (
    web_search,
    web_fetch,
)

from tools.papers import (
    paper_search,
    read_paper,
)

load_dotenv()

WORKSPACE_ROOT = os.path.abspath(os.environ.get("WORKSPACE_ROOT", "."))
MAX_ITERATIONS = 10
MAX_READ_CHARS = 12_000

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = "nex-agi/nex-n2-pro:free"
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_fetch",
            "description": "Fetch webpage content",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "paper_search",
            "description": "Search academic papers",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
]
class Agent:
    """Core agent: loop, tools, sessions. No UI."""

    def __init__(self, workspace=".", session_id=None):

        self.workspace = os.path.abspath(workspace)

        if session_id:
            self.session_id = session_id

            try:
                session = load_session(session_id)
                self.messages = session["messages"]

            except Exception:
                self.messages = [
                    {
                        "role": "system",
                        "content": build_system_prompt()
                    }
                ]

        else:
            self.session_id = create_session()

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

        save_session(
            self.session_id,
            self.messages,
            title="Research Session"
        )

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

        name = tool_call["name"]
        args = tool_call["arguments"]

        if name == "web_search":
            return json.dumps(
                web_search(args["query"])
            )

        if name == "web_fetch":
            return json.dumps(
                web_fetch(args["url"])
            )

        if name == "paper_search":
            return json.dumps(
                paper_search(args["query"])
            )

        if name == "read_paper":
            return json.dumps(
                read_paper(args["arxiv_id"])
            )

        if name == "read_file":
            return json.dumps(
                read_file(**args)
            )

        if name == "write_file":
            return json.dumps(
                write_file(**args)
            )

        if name == "edit_file":
            return json.dumps(
                edit_file(**args)
            )

        if name == "list_files":
            return json.dumps(
                list_files(**args)
            )

        return json.dumps(
            {
                "error": f"Unknown tool: {name}"
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

    if "--tui" in sys.argv:
        from tui import ResearchDeskApp
        ResearchDeskApp().run()
        return

    session_id = None

    if "--session" in sys.argv:

        idx = sys.argv.index("--session")

        if idx + 1 < len(sys.argv):
            session_id = sys.argv[idx + 1]

            del sys.argv[idx:idx + 2]

    agent = REPLAgent(
        session_id=session_id
    )

    if len(sys.argv) > 1:

        print(
            agent.run_once(
                " ".join(sys.argv[1:])
            )
        )

        return

    agent.run()


if __name__ == "__main__":
    main()
    