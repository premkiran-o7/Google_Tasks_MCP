import os.path
from datetime import datetime, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



class TaskService:
    def __init__(self):
        self.__task_service = None
        self.__scope = ["https://www.googleapis.com/auth/tasks"]

    def __call__(self):
        """ Returns a Tasks service object"""

        if self.__task_service is None:

            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", self.__scope)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.__scope
                )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())

            try:
                self.__task_service = build("tasks", "v1", credentials=creds)

            except Exception:
                print("Tasks service could not be made")


        return self.__task_service


tasks_service = TaskService()


async def list_tasklists(max_results: int = 100) -> list:
    """
    Retrieves all task lists for the authenticated user.

    Args:
        max_results (int, optional): Maximum number of task lists to return. Defaults to 100.

    Returns:
        list: A list of task list objects.
    """
    service = tasks_service()
    try:
        results = service.tasklists().list(maxResults=max_results).execute()
        return results.get("items", [])
    except Exception as e:
        return f"Error listing task lists: {e}"


async def get_tasklist(tasklist_id: str) -> dict:
    """
    Retrieves a specific task list by its ID.

    Args:
        tasklist_id (str): The ID of the task list to retrieve.

    Returns:
        dict: The task list object.
    """
    service = tasks_service()
    try:
        return service.tasklists().get(tasklist=tasklist_id).execute()
    except Exception as e:
        return f"Error retrieving task list: {e}"


async def insert_tasklist(title: str) -> dict:
    """
    Creates a new task list.

    Args:
        title (str): The title of the new task list.

    Returns:
        dict: The created task list object.
    """
    service = tasks_service()
    try:
        tasklist = {"title": title}
        return service.tasklists().insert(body=tasklist).execute()
    except Exception as e:
        return f"Error creating task list: {e}"



async def update_tasklist(tasklist_id: str, title: str) -> dict:
    """
    Updates the title of an existing task list.

    Args:
        tasklist_id (str): The ID of the task list to update.
        title (str): The new title for the task list.

    Returns:
        dict: The updated task list object.
    """
    service = tasks_service()
    try:
        tasklist = {"title": title}
        return service.tasklists().update(tasklist=tasklist_id, body=tasklist).execute()
    except Exception as e:
        return f"Error updating task list: {e}"


async def delete_tasklist(tasklist_id: str) -> str:
    """
    Deletes a task list by its ID.

    Args:
        tasklist_id (str): The ID of the task list to delete.

    Returns:
        str: Confirmation message upon successful deletion.
    """
    service = tasks_service()
    try:
        service.tasklists().delete(tasklist=tasklist_id).execute()
        return f"Task list {tasklist_id} deleted successfully."
    except Exception as e:
        return f"Error deleting task list: {e}"



### Task operations


async def list_tasks(tasklist_id: str, max_results: int = 100) -> list:
    """
    Retrieves all tasks from a specified task list.

    Args:
        tasklist_id (str): The ID of the task list.
        max_results (int, optional): Maximum number of tasks to return. Defaults to 100.

    Returns:
        list: A list of task objects.
    """
    service = tasks_service()
    try:
        results = service.tasks().list(tasklist=tasklist_id, maxResults=max_results).execute()
        return results.get("items", [])
    except Exception as e:
        return f"Error listing tasks: {e}"



async def get_task(tasklist_id: str, task_id: str) -> dict:
    """
    Retrieves a specific task by its ID from a task list.

    Args:
        tasklist_id (str): The ID of the task list.
        task_id (str): The ID of the task to retrieve.

    Returns:
        dict: The task object.
    """
    service = tasks_service()
    try:
        return service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
    except Exception as e:
        return f"Error retrieving task: {e}"



async def insert_task(tasklist_id: str, title: str, notes: str = None, due: str = None) -> dict:
    """
    Creates a new task in a specified task list.

    Args:
        tasklist_id (str): The ID of the task list.
        title (str): The title of the new task.
        notes (str, optional): Additional notes for the task.
        due (str, optional): Due date in RFC3339 timestamp format.

    Returns:
        dict: The created task object.
    """
    service = tasks_service()
    try:
        task = {"title": title}
        if notes:
            task["notes"] = notes
        if due:
            task["due"] = due
        return service.tasks().insert(tasklist=tasklist_id, body=task).execute()
    except Exception as e:
        return f"Error creating task: {e}"




async def update_task(
    tasklist_id: str,
    task_id: str,
    title: str = None,
    notes: str = None,
    due: str = None,
    status: str = None,
    completed: str = None
) -> dict:
    """
    Updates an existing task in a task list.

    Args:
        tasklist_id (str): The ID of the task list.
        task_id (str): The ID of the task to update.
        title (str, optional): New title for the task.
        notes (str, optional): New notes for the task.
        due (str, optional): New due date in RFC3339 timestamp format.
        status (str, optional): New status for the task ('needsAction' or 'completed').
        completed (str, optional): Completion date in RFC3339 timestamp format.

    Returns:
        dict: The updated task object.
    """
    service = tasks_service()
    try:
        task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
        if title:
            task["title"] = title
        if notes:
            task["notes"] = notes
        if due:
            task["due"] = due
        if status:
            task["status"] = status
        if completed:
            task["completed"] = completed
        return service.tasks().update(tasklist=tasklist_id, task=task_id, body=task).execute()
    except Exception as e:
        return f"Error updating task: {e}"




async def delete_task(tasklist_id: str, task_id: str) -> str:
    """
    Deletes a task from a task list.

    Args:
        tasklist_id (str): The ID of the task list.
        task_id (str): The ID of the task to delete.

    Returns:
        str: Confirmation message upon successful deletion.
    """
    service = tasks_service()
    try:
        service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()
        return f"Task {task_id} deleted successfully from task list {tasklist_id}."
    except Exception as e:
        return f"Error deleting task: {e}"


async def clear_completed_tasks(tasklist_id: str) -> str:
    """
    Clears all completed tasks from the specified task list.

    Args:
        tasklist_id (str): The ID of the task list.

    Returns:
        str: Confirmation message upon successful clearance.
    """
    service = tasks_service()
    try:
        service.tasks().clear(tasklist=tasklist_id).execute()
        return f"Completed tasks cleared from list {tasklist_id}."
    except Exception as e:
        return f"Error clearing completed tasks: {e}"



async def move_task(tasklist_id: str, task_id: str, parent: str = None, previous: str = None) -> dict:
    """
    Moves a task to a new position within the task list.

    Args:
        tasklist_id (str): The ID of the task list.
        task_id (str): The ID of the task to move.
        parent (str, optional): The new parent task ID.
        previous (str, optional): The task ID to insert the task after.

    Returns:
        dict: The moved task object.
    """
    service = tasks_service()
    try:
        return service.tasks().move(tasklist=tasklist_id, task=task_id, parent=parent, previous=previous).execute()
    except Exception as e:
        return f"Error moving task: {e}"
