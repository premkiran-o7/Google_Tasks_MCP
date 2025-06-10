from mcp.server.fastmcp import FastMCP
import services
from datetime import datetime, timezone

# Initialize FastMCP server
mcp = FastMCP("tasks_server")


@mcp.tool()
async def list_tasklists(max_results: int = 100) -> list:
    """
    Retrieve all task lists for the authenticated user.
    Task lists are the category of tasks grouped together.

    Args:
        max_results (int, optional): Maximum number of task lists to return. Defaults to 100.

    Returns:
        list: A list of task list objects.
    """
    return await services.list_tasklists(max_results=max_results)



@mcp.tool()
async def get_tasklist(tasklist_id: str) -> dict:
    """
    Retrieve a specific task list by its ID.
    Task lists are the category of tasks grouped together.

    Args:
        tasklist_id (str): The ID of the task list to retrieve.

    Returns:
        dict: The task list object.
    """
    return await services.get_tasklist(tasklist_id=tasklist_id)



@mcp.tool()
async def create_tasklist(title: str) -> dict:
    """
    Create a new task list.
    Task lists are the category of tasks grouped together.

    Args:
        title (str): The title of the new task list.

    Returns:
        dict: The created task list object.
    """
    return await services.insert_tasklist(title=title)


@mcp.tool()
async def update_tasklist(tasklist_id: str, title: str) -> dict:
    """
    Update the title of an existing task list.
    Task lists are the category of tasks grouped together.

    Args:
        tasklist_id (str): The ID of the task list to update.
        title (str): The new title for the task list.

    Returns:
        dict: The updated task list object.
    """
    return await services.update_tasklist(tasklist_id=tasklist_id, title=title)


@mcp.tool()
async def mark_task_completed(tasklist_id: str, task_id: str) -> dict:
    """
    Mark a specific task as completed.

    Args:
        tasklist_id (str): The ID of the task list.
        task_id (str): The ID of the task to mark as completed.

    Returns:
        dict: The updated task object with status set to 'completed'.
    """
    completed_time = datetime.now(timezone.utc).isoformat()
    return await services.update_task(
        tasklist_id=tasklist_id,
        task_id=task_id,
        status="completed",
        completed=completed_time
    )


@mcp.tool()
async def delete_tasklist(tasklist_id: str) -> str:
    """
    Delete a task list by its ID.
    Task lists are the category of tasks grouped together.

    Args:
        tasklist_id (str): The ID of the task list to delete.

    Returns:
        str: Confirmation message upon successful deletion.
    """
    return await services.delete_tasklist(tasklist_id=tasklist_id)



@mcp.tool()
async def list_tasks(tasklist_id: str, max_results: int = 100) -> list:
    """
    Retrieve all tasks from a specified task list.
    Task lists are the category of tasks grouped together.

    Args:
        tasklist_id (str): The ID of the task list.
        max_results (int, optional): Maximum number of tasks to return. Defaults to 100.

    Returns:
        list: A list of task objects.
    """
    return await services.list_tasks(tasklist_id=tasklist_id, max_results=max_results)



@mcp.tool()
async def get_task(tasklist_id: str, task_id: str) -> dict:
    """
    Retrieve a specific task by its ID from a task list.
    Task lists are the category of tasks grouped together.

    Args:
        tasklist_id (str): The ID of the task list.
        task_id (str): The ID of the task to retrieve.

    Returns:
        dict: The task object.
    """
    return await services.get_task(tasklist_id=tasklist_id, task_id=task_id)



@mcp.tool()
async def create_task(
    tasklist_id: str,
    title: str,
    notes: str | None = None,
    due: str | None = None
) -> dict:
    """
    Create a new task in the specified task list.
    Task lists are the category of tasks grouped together.

    Args:
        tasklist_id (str): The ID of the task list.
        title (str): The title of the task.
        notes (str, optional): Additional notes for the task.
        due (str, optional): Due date in RFC3339 timestamp format.

    Returns:
        dict: The created task object.
    """
    return await services.insert_task(tasklist_id=tasklist_id, title=title, notes=notes, due=due)




@mcp.tool()
async def update_task(
    tasklist_id: str,
    task_id: str,
    title: str | None = None,
    notes: str | None = None,
    due: str | None = None,
    status: str | None = None
) -> dict:
    """
    Update an existing task in the specified task list.
    Task lists are the category of tasks grouped together.

    Args:
        tasklist_id (str): The ID of the task list.
        task_id (str): The ID of the task to update.
        title (str, optional): The new title of the task.
        notes (str, optional): The new notes for the task.
        due (str, optional): New due date in RFC3339 timestamp format.
        status (str, optional): The new status of the task ('needsAction' or 'completed').Default is needsAction.

    Returns:
        dict: The updated task object.
    """
    return await services.update_task(
        tasklist_id=tasklist_id,
        task_id=task_id,
        title=title,
        notes=notes,
        due=due,
        status=status
    )



@mcp.tool()
async def delete_task(tasklist_id: str, task_id: str) -> str:
    """
    Delete a task from the specified task list.
    Task lists are the category of tasks grouped together.

    Args:
        tasklist_id (str): The ID of the task list.
        task_id (str): The ID of the task to delete.

    Returns:
        str: Confirmation message upon successful deletion.
    """
    return await services.delete_task(tasklist_id=tasklist_id, task_id=task_id)


@mcp.tool()
async def clear_completed_tasks(tasklist_id: str) -> str:
    """
    Clear all completed tasks from the specified task list.
    Task lists are the category of tasks grouped together.

    Args:
        tasklist_id (str): The ID of the task list.

    Returns:
        str: Confirmation message upon successful clearance.
    """
    return await services.clear_completed_tasks(tasklist_id=tasklist_id)



@mcp.tool()
async def move_task(
    tasklist_id: str,
    task_id: str,
    parent: str | None = None,
    previous: str | None = None
) -> dict:
    """
    Move a task to a new position within the task list.
    Task lists are the category of tasks grouped together.

    Args:
        tasklist_id (str): The ID of the task list.
        task_id (str): The ID of the task to move.
        parent (str, optional): The new parent task ID.
        previous (str, optional): The task ID to insert the task after.

    Returns:
        dict: The moved task object.
    """
    return await services.move_task(
        tasklist_id=tasklist_id,
        task_id=task_id,
        parent=parent,
        previous=previous
    )


if __name__ == "__main__":
    # Run MCP server
    mcp.run(transport="stdio")
