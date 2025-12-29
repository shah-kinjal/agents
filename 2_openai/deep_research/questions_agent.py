from pydantic import BaseModel, Field
from agents import Agent

HOW_MANY_QUESTION = 3

INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of clerifying questions to improve the research. \
 Output {HOW_MANY_QUESTION} questions to ask."


class QuestionItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this question is important to the query.")
    query: str = Field(description="The question to ask.")


class Questions(BaseModel):
    questions: list[QuestionItem] = Field(description="A list of clarifying questions to ask for clarification on the query")
    
question_agent = Agent(
    name="QuestionAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=Questions,
)