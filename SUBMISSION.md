# Week 2 Submission

For this project, I built a research agent that can search the web, read web pages, and discover academic research papers. The goal was to combine different tools into a single agent that can collect information and provide useful answers to user questions.

The project uses OpenRouter as the language model provider. For web search, I used the Serper API. To read webpage content, I used Trafilatura, which extracts clean text from websites. I also integrated AlphaXiv MCP to search for research papers and explore academic content.

The agent follows a simple loop. First, it receives a user query. Then it searches the web or research sources when needed, collects information, and sends the relevant content to the language model. Finally, the model generates a response based on the gathered information.

One important design decision was limiting the amount of webpage text sent to the model. Many webpages contain a large amount of content, which can increase token usage and slow down responses. By sending only the most relevant portion of the text, the agent remains faster and more efficient.

The most challenging part of this project was integrating AlphaXiv MCP. Initially, I received authentication and OAuth-related errors. After studying the documentation and completing the OAuth login flow, I was able to connect successfully and use the `discover_papers` tool to retrieve research papers.

During development, I learned how tool calling works, how an agent loop is implemented, how MCP servers can provide external tools, and how to build a responsive terminal interface using Textual.

If I had more time, I would improve the agent so that it automatically decides which tool to use for different types of questions. I would also add better error handling, support for more research sources, and a more advanced TUI that shows tool activity in real time.
