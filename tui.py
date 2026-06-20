from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog

from agent import Agent


class TUIAgent(Agent):
    pass


class ResearchDeskApp(App):

    CSS = """
    Screen {
        layout: vertical;
    }

    RichLog {
        height: 1fr;
    }

    Input {
        dock: bottom;
    }
    """

    def __init__(self):
        super().__init__()
        self.agent = TUIAgent()

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id="chat")
        yield Input(placeholder="Ask something...")
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted):

        chat = self.query_one("#chat", RichLog)

        user_text = event.value

        chat.write(f"> {user_text}")

        answer = self.agent.chat(user_text)

        chat.write(answer)

        event.input.value = ""


if __name__ == "__main__":
    ResearchDeskApp().run()