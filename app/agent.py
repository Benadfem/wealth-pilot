import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)


# Adding the first tool to the agent
@tool
def get_all_transactions(query: str) -> str:
    """Get all transactions from the database. 
    Use this to analyse spending patterns."""
    from app.database import SessionLocal
    from app import models
    db = SessionLocal()
    transactions = db.query(models.Transaction).all()
    db.close()
    if not transactions:
        return "No transactions found."
    result = ""
    for t in transactions:
        result += f"ID:{t.id} Amount:{t.amount} Category:{t.category} Date:{t.date} Description:{t.description}\n"
    return result


# a tool to determine the spending 
@tool
def get_spending_by_category(category: str) -> str:
    """Get total spending for a specific category.
    Use this to analyse spending in food, transport, 
    bills or any other category."""
    from app.database import SessionLocal
    from app import models
    db = SessionLocal()
    transactions = db.query(models.Transaction).filter(
        models.Transaction.category == category
    ).all()
    db.close()
    if not transactions:
        return f"No transactions found for category: {category}"
    total = sum(t.amount for t in transactions)
    result = f"Category: {category}\n"
    result += f"Total spent: {total}\n"
    result += f"Number of transactions: {len(transactions)}\n"
    return result



# adding the agentic code
tools = [get_all_transactions, get_spending_by_category]

agent = create_react_agent(llm, tools)

def run_agent(question: str) -> str:
    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    return result["messages"][-1].content