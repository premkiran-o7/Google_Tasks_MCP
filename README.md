```python

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

class QueryEvaluation(BaseModel):
    complexity: str = Field(..., description="SIMPLE or NOT_SIMPLE")



QUERY_COMPLEXITY_TEMPLATE = """\
You are an expert data assistant.

Classify the following user query as either SIMPLE or COMPLEX.

Definitions:
- SIMPLE: Can be answered with direct queries, basic filters, or simple visualizations (bar, line, pie charts).
- NOT_SIMPLE: Requires multi-step logic, derived metrics, advanced visualizations, or involves ambiguity.

Only return a JSON object with this format:
{{ "complexity": "SIMPLE" }} or {{ "complexity": "NOT_SIMPLE" }}

User Query: {query}
"""

import os
from dotenv import load_dotenv
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile", # Replace with your actual Groq API key
)


def evaluate_query_complexity(query: str):
    prompt = PromptTemplate.from_template(QUERY_COMPLEXITY_TEMPLATE)
chain: Runnable = prompt | llm.with_structured_output(QueryEvaluation)
    return chain.invoke({"query": query})


result = evaluate_query_complexity("Compare user engagement metrics over time and identify possible causes for spikes.")
print(result.complexity)


#NOT_SIMPLE
#SIMPLE  
```
