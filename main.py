import os
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the model
model = ChatGroq(model="qwen-qwq-32b")
# Set server parameters for the stdio connection
# server_params = StdioServerParameters(
#     command="python",
#     # Ensure the full path to your script is correct
#     args=["tasks_mcp.py"],
# )

server_params = StdioServerParameters(
    command="python",
    # Ensure the full path to your script is correct
    args=["tasks_mcp.py"],
)

# Main asynchronous function
async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Load available tools from the MCP session
            tools = await load_mcp_tools(session)

            # Create the React-style agent with the model and tools
            agent = create_react_agent(model, tools)

            print("\n===== Interactive MCP Chat =====")
            print("Type 'exit' or 'quit' to end the conversation")
            print("Type 'clear' to clear conversation history")
            print("==================================\n")

            # Start interactive chat loop
            try:
                while True:
                    user_input = input("\nYou: ")

                    if user_input.lower() in ["exit", "quit"]:
                        print("Ending conversation...")
                        break
                    elif user_input.lower() == "clear":
                        print("\nConversation history cleared.")
                        continue

                    print("\nAssistant: ", end="", flush=True)

                    try:
                        response = await agent.ainvoke({"messages": user_input})
                        print(response['messages'][-1].content)
                    except Exception as e:
                        print(f"\nError during agent response: {e}")

            except Exception as e:
                print(f"\nUnexpected error: {e}")

# Entry point for async execution
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
