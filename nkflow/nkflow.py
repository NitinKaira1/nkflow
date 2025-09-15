import re
import subprocess
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Memory store
_store = {}
def _get_memory(session_id: str):
    if session_id not in _store:
        _store[session_id] = ChatMessageHistory()
    return _store[session_id]

# Prompt template (shared across models)
_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a coding assistant. Always return ONLY code, wrapped in triple backticks. "
               "If the code is too long, split it into multiple parts labeled 'PART X/Y'."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Regex to extract code blocks + language type
def _extract_code(text: str):
    matches = re.findall(r"```(\w*)\n(.*?)```", text, re.DOTALL)
    return [(lang.strip(), code.strip()) for lang, code in matches]

# Main function (agnostic to LLM)
def run(task: str, filename: str, auto_run: bool, llm, session_id="single_run"):
    """Generate code using the provided LLM, save it to filename, and optionally run it."""

    # Build chain with user-supplied LLM
    chain = RunnableWithMessageHistory(
        _prompt | llm,
        _get_memory,
        input_messages_key="input",
        history_messages_key="history",
    )

    # Query LLM
    response = chain.invoke(
        {"input": f"Task: {task}"},
        config={"configurable": {"session_id": session_id}}
    )

    content = response.content
    code_blocks = _extract_code(content)

    if not code_blocks:
        print("# No code detected")
        return

    full_code = "\n\n".join(code for _, code in code_blocks)
    lang = code_blocks[0][0].lower() if code_blocks else ""

    # Save code
    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_code)
    print(f"✅ Code saved as {filename}")

    # Optionally run
    if auto_run:
        if filename.endswith(".py"):
            print(f"🚀 Running {filename}...\n")
            subprocess.run(["python", filename], check=False)
