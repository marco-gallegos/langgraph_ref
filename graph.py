""" Lang grapph create a graph (node joins) to put steps into.
with llm or not.

needs a start and a end.
"""

# 1 - imports and llm if neede

# You may need to install these first:
# uv add langgraph langchain langchain-openai

# NOTE: all about lang chain is not required by langgraph just is here because is common.

import os
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START

# Set your API key
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Initialize the language model we'll use for all nodes
# llm = ChatOpenAI(model="gpt-4o")

## mock llm ignore this code is just ai trying to fit the response 
class fakeLLM:
    def invoke(self, prompt):
        class Response:
            def __init__(self, content):
                self.content = content
        # Mock response based on the prompt
        if "improve this text writing and translate it to english" in prompt:
            return Response("This is a refined and translated version of the input text.")
        elif "you are a software engineer and you need to create a accurated prompt" in prompt:
            return Response("Write a clear and concise prompt that can be used to generate code changes based on the provided transcription.")
        else:
            return Response("Default response for unrecognized prompts.")

    
llm = fakeLLM()

# 2 - define state 
# NOTE: state is shared by graph nodes


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        rawText (str): The original input text provided by the user.
        refinedText (str): The refined version of the input text.
        outputText (str): The final output text after processing.
    """
    rawText: str
    refinedText: str
    outputText: str


# 3 - Define Nodes
# NOTE:a node need to return state changes, and can use the state to do its job. also can use llm or whatever it needs.

def node1(state: GraphState) -> dict:
    """
    Clean the text.
    """
    raw_text = state['rawText']
    prompt = f"improve this text writing and translate it to english: '{raw_text}'."
    
    out_string = llm.invoke(prompt).content
    print(f"defined text:\n{out_string}")
    
    return {"refinedText": out_string}

def node2(state: GraphState) -> dict:
    """
    Create a output to use as cursor prompt.
    """
    refined_text = state['refinedText']
    prompt = f"you are a software engineer and you need to create a accurated prompt to use it on any code agent and generate a change based on this STT transcription: '{refined_text}'. Write a clear and concise prompt that can be used to generate code changes based on the provided transcription."
    
    prompt_results = llm.invoke(prompt).content

    return {"outputText": prompt_results}


# 4 - Build Graph flow
# NOTE: you can use the state to decide the flow, and also can use the llm

# Initialize the graph
workflow = StateGraph(GraphState)

# Add the nodes
workflow.add_node("node1", node1)
workflow.add_node("node2", node2)

# Define the edges for the linear flow
workflow.add_edge(START, "node1")
workflow.add_edge("node1", "node2")
workflow.add_edge("node2", END)

# Compile the graph into a runnable app
graph = workflow.compile()


# 5 - Run the graph or import it

