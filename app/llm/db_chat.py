import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import OllamaLLM

def get_db_chat_agent():
    db_url = os.getenv("DB_URL", "postgresql://user:password@localhost:5432/hse_db")
    # In docker, this is host.docker.internal:11434
    ollama_url = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
    
    db = SQLDatabase.from_uri(db_url)
    llm = OllamaLLM(model="gemma3:4b", base_url=ollama_url, temperature=0)
    
    # We use create_sql_agent for natural DB interactions natively
    agent = create_sql_agent(
        llm=llm, 
        db=db, 
        verbose=True,
        max_iterations=40,         
        max_execution_time=120,
        agent_executor_kwargs={"handle_parsing_errors": True}
    )
    return agent

def ask_question(question: str):
    try:
        agent = get_db_chat_agent()
        response = agent.invoke({"input": question})
        return response.get("output", str(response))
    except Exception as e:
        error_msg = str(e)
        if "Connection refused" in error_msg or "[Errno 111]" in error_msg:
            return "❌ Ошибка: Ollama недоступна.\n\nУбедитесь, что:\n1. Ollama запущена локально (`ollama serve`).\n2. Модель (model_name) загружена (`ollama run model_name`).\n3. Docker имеет доступ к хосту (мы используем `host.docker.internal:11434`)."
        return f"❌ Ошибка LLM/БД: {error_msg}"
