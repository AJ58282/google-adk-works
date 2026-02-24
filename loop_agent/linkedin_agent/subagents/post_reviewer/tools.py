from typing import Any, Dict
from google.adk.tools.tool_context import ToolContext


def count_char(text: str, tool_context: ToolContext) -> Dict[str, Any]:
    char_count = len(text)

    min_len = 1000
    max_len = 2000

    if char_count < min_len:
        status = "fail"
        message = "Post is too short."
    elif char_count > max_len:
        status = "fail"
        message = "Post is too long."
    else:
        status = "pass"
        message = "Post length is valid."

    tool_context.state["status"] = status
    tool_context.state["char_count"] = char_count

    return {
        "status": status,
        "char_count": char_count,
        "message": message,
    }


def exit_loop(tool_context: ToolContext) -> Dict[str, Any]:
    tool_context.actions.escalate = True
    return {"loop_terminated": True}
