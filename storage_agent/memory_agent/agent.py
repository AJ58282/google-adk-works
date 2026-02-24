from google.adk.agents import Agent
from google.adk.tools import ToolContext


def add_reminder(text: str, tool_context: ToolContext):
    reminders = tool_context.state.get("reminders", [])

    reminders.append(text)
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "reminder": text,
        "total_reminders": len(reminders),
    }


def view_reminders(tool_context: ToolContext):
    reminders = tool_context.state.get("reminders", [])

    return {
        "action": "view_reminders",
        "reminders": reminders,
        "count": len(reminders),
    }


def update_reminder(index: int, update_text: str, tool_context: ToolContext):
    reminders = tool_context.state.get("reminders", [])

    if index < 0 or index >= len(reminders):
        return {
            "action": "update_reminder",
            "status": "error",
            "message": "Invalid reminder index.",
        }

    old_value = reminders[index]
    reminders[index] = update_text
    tool_context.state["reminders"] = reminders

    return {
        "action": "update_reminder",
        "status": "success",
        "old_value": old_value,
        "updated_value": update_text,
        "index": index,
    }


def delete_reminder(index: int, tool_context: ToolContext):
    reminders = tool_context.state.get("reminders", [])

    if index < 0 or index >= len(reminders):
        return {
            "action": "delete_reminder",
            "status": "error",
            "message": "Invalid reminder index.",
        }

    removed = reminders.pop(index)
    tool_context.state["reminders"] = reminders

    return {
        "action": "delete_reminder",
        "status": "success",
        "removed": removed,
        "remaining_count": len(reminders),
    }


def update_user_name(name: str, tool_context: ToolContext):
    tool_context.state["user_name"] = name

    return {
        "action": "update_user_name",
        "status": "success",
        "new_name": name,
    }

memory_agent=Agent(
    name="memory_agent",
    model="gemini-2.0-pro",
    description="Smart reminder agent with persistent memory",
    instruction="""
    You are a friendly and reliable reminder assistant that remembers users across conversations using persistent session state.

    The user's information is stored in session state:

    User's name: {user_name}

    Reminders: {reminders}

    You are responsible for helping the user manage their reminders efficiently and clearly.

    You can assist with the following capabilities:

    Add new reminders

    View existing reminders

    Update an existing reminder

    Delete a reminder

    Update the user’s name

    Always use the appropriate tool whenever modifying session state.
    Never manually edit reminders in your response — state changes must happen through tools.

    When interacting with the user:

    Always be polite and conversational.

    Address the user by their stored name whenever available.

    If the user's name is missing or empty, ask for their name and use the update_user_name tool to store it.

    When adding, updating, or deleting reminders, confirm the action clearly.

    When listing reminders, present them in a clean numbered format.

    If there are no reminders stored, inform the user clearly instead of showing an empty list.

    REMINDER MANAGEMENT GUIDELINES

    When adding a reminder, append it to the reminders list.

    When updating a reminder, identify it by its index or description before modifying.

    When deleting a reminder, confirm which reminder is being removed.

    Always ensure the reminders list remains structured as a list of strings.

    Never overwrite the entire reminders list unless explicitly instructed to clear all reminders.

    Maintain consistency, accuracy, and friendliness at all times. """ ,
    
    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name,
    ],    
)
