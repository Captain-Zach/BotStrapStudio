
import os
import asyncio
import websockets
from dotenv import load_dotenv

# Import llama-cpp-python
from llama_cpp import Llama

# Load environment variables from .env file in the same directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


# Use environment variable for server URI, fallback to default
SERVER_URI = os.getenv("BOTSTRAP_SERVER_URI", "ws://localhost:8080/ws")

# Use environment variable for model path, fallback to default
MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", "./gemma-3b-e2b.Q4_K_M.gguf")

# Initialize Llama model (for test query)
llm = Llama(model_path=MODEL_PATH)

async def send_llm_query(query: str):
    async with websockets.connect(SERVER_URI) as websocket:
        await websocket.send(query)
        response = await websocket.recv()
        print(f"Server response: {response}")


# Test Llama.cpp with a sample query
def test_llama():
    print("Running test query on local Llama.cpp model...")
    output = llm("What is the capital of France?", max_tokens=32)
    print("Llama.cpp output:", output["choices"][0]["text"].strip())

if __name__ == "__main__":
    # Run a test query on the local Llama.cpp model
    test_llama()
    # Then run the websocket client as before
    query = input("Enter your LLM query: ")
    asyncio.run(send_llm_query(query))
