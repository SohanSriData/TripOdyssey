from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from prompt_library.prompt import REVIEW_PROMPT
from utils.save_to_doc import save_document
from logger import get_logger
import os
import re

logger = get_logger()


def clean_agent_output(text: str) -> str:
    # Remove stray markdown backticks and empty anchor links from generated content.
    cleaned = re.sub(r"`+", "", text)
    cleaned = re.sub(r"\[\]\([^\)]+\)", "", cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    return cleaned.strip()


app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")

async def query_travel_agent(query: QueryRequest):
    try:
        logger.info("Received query: %s", query.question)
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
        
        logger.info("Saved graph image to %s/my_graph.png", os.getcwd())

        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        final_output = clean_agent_output(final_output)

        # Second pass review and revision to improve the final answer
        review_text = graph.review_plan(final_output)
        review_text = clean_agent_output(review_text)
        revised_output = graph.revise_plan(final_output, review_text)
        final_answer = clean_agent_output(revised_output)

        saved_file = save_document(final_answer)
        logger.info("Saved travel plan to: %s", saved_file)
        
        return {"answer": final_answer, "saved_file": saved_file}
    except Exception as e:
        logger.error("Query failed: %s", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})


