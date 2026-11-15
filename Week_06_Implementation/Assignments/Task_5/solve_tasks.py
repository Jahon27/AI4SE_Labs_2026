import ast
import json
import os
import re
import shutil
import sys
import textwrap
from pathlib import Path


TASK_5_FOLDER = Path(__file__).parent
ROOT_FOLDER = TASK_5_FOLDER.parents[2]
REPOSITORY_FOLDER = ROOT_FOLDER / "AI4SE_Playground"
TASKS_FILE = TASK_5_FOLDER.parent / "missing_code.json"
EMBEDDINGS_FILE = TASK_5_FOLDER.parent / "Task_3" / "chunk_embeddings.json"
BACKUP_FOLDER = TASK_5_FOLDER / "source_backups"
MODEL_NAME = "jinaai/jina-embeddings-v2-base-code"
LLM_MODEL = "gpt-6-luna"

sys.path.insert(0, str(TASK_5_FOLDER.parent / "Task_3"))
sys.path.insert(0, str(TASK_5_FOLDER.parent / "Task_4"))
from embed_chunks import load_model
from match_embeddings import match_embeddings


def load_environment():
    environment_file = ROOT_FOLDER / ".env"
    if not environment_file.is_file():
        raise FileNotFoundError(f"Environment file not found: {environment_file}")

    for line in environment_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            name, value = line.split("=", 1)
            os.environ.setdefault(name.strip(), value.strip().strip("\"'"))

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required in .env")


def load_tasks():
    return json.loads(TASKS_FILE.read_text(encoding="utf-8"))


def get_method_node(source, class_name, method_name):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if child.name == method_name:
                        return child
    raise LookupError(f"Method not found: {class_name}.{method_name}")


def method_context(source, node):
    lines = source.splitlines()
    start = max(0, node.lineno - 4)
    end = min(len(lines), node.end_lineno + 4)
    return "\n".join(lines[start:end])


def test_context(task):
    test_file = REPOSITORY_FOLDER / "playground" / "tests" / (
        f"test_{Path(task['file']).stem}.py"
    )
    if test_file.is_file():
        return test_file.read_text(encoding="utf-8")
    return "No matching test file was found."


def build_prompt(task, source, node, matches):
    context = "\n\n".join(
        f"FILE: {match['file_path']}\n{match['content']}" for match in matches
    )
    return f"""Implement one missing Python method using the repository context.

Target file: {task['file']}
Target class: {task['class']}
Target method: {task['method']}
Task description: {task['docstring']}

Existing method context:
{method_context(source, node)}

Relevant unit tests:
{test_context(task)}

Treat the unit tests as authoritative behavioral requirements, including cases
where they are more specific than the method docstring.

Retrieved repository chunks:
{context}

Return only the method body code, without Markdown fences and without the method
signature. Do not include indentation for the method body. Preserve the existing
class design and use only names supported by the target file.
"""


def extract_code(response):
    code = response.strip()
    fenced = re.search(r"```(?:python)?\s*(.*?)```", code, re.DOTALL)
    if fenced:
        code = fenced.group(1).strip()
    return code


def validate_body(code):
    code = textwrap.dedent(code).strip()
    ast.parse(f"def generated_method():\n" + "\n".join(
        f"    {line}" if line else "" for line in code.splitlines()
    ))


def replace_method_body(path, class_name, method_name, body):
    source = path.read_text(encoding="utf-8")
    node = get_method_node(source, class_name, method_name)
    lines = source.splitlines(keepends=True)
    method_indent = " " * node.col_offset
    body = textwrap.dedent(body).strip()
    replacement = [
        f"{method_indent}    {line}\n" if line else "\n"
        for line in body.splitlines()
    ]
    body_start = node.body[0].lineno - 1
    body_end = node.end_lineno
    lines[body_start:body_end] = replacement
    updated_source = "".join(lines)
    ast.parse(updated_source)
    path.write_text(updated_source, encoding="utf-8")


def create_backup(path):
    BACKUP_FOLDER.mkdir(exist_ok=True)
    destination = BACKUP_FOLDER / path.relative_to(REPOSITORY_FOLDER)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        shutil.copy2(path, destination)


def solve_task(task, model, llm):
    path = REPOSITORY_FOLDER / task["file"]
    source = path.read_text(encoding="utf-8")
    node = get_method_node(source, task["class"], task["method"])
    query_embedding = model.encode(task["docstring"]).tolist()
    matches = match_embeddings(query_embedding, 5)
    prompt = build_prompt(task, source, node, matches)
    response = llm.invoke(prompt)
    body = extract_code(response.content)
    validate_body(body)
    create_backup(path)
    replace_method_body(path, task["class"], task["method"], body)
    return len(matches)


def main():
    load_environment()
    from langchain_openai import ChatOpenAI

    embedding_model = load_model()
    llm = ChatOpenAI(model=LLM_MODEL)
    tasks = load_tasks()
    successful = 0
    failures = []

    for task in tasks:
        try:
            matches = solve_task(task, embedding_model, llm)
            successful += 1
            print(
                f"SUCCESS {task['file']}::{task['class']}.{task['method']} "
                f"(retrieved {matches} chunks)"
            )
        except Exception as error:
            failures.append((task, error))
            print(
                f"FAILED {task['file']}::{task['class']}.{task['method']}: "
                f"{type(error).__name__}: {error}"
            )

    print(f"Completed {successful}/{len(tasks)} tasks.")
    if failures:
        print(f"Failures: {len(failures)}")


if __name__ == "__main__":
    main()
