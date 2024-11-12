from fastapi import FastAPI, Response
from langchain_ollama import OllamaLLM
from pydantic import BaseModel

# Initialize the language model
model = "llama3.2:3b"
llm = OllamaLLM(model=model, base_url="http://ollama-server:11434")

# FastAPI application instance
app = FastAPI(
    title="Ollama API",
    description="API using FastAPI to interact with the Ollama language model for Q&A.",
    version="1.0.0"
)

class Question(BaseModel):
    """Schema for a question sent to the LLM.

    Attributes:
        text (str): The question text to be processed by the LLM.
    """
    text: str

@app.post("/ask")
async def ask_question(question: Question) -> dict:
    """Send a question to the LLM and receive a response.

    Args:
        question (Question): The question text to be processed by the LLM.

    Returns:
        dict: A dictionary containing the LLM's response to the question.
    """
    response = llm.invoke(question.text)
    return {"response": response}
