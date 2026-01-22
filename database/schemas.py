def todo_serial(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
        "completed": todo["completed"],
        "is_deleted": todo.get("is_deleted", False),
        "created_at": todo.get("created_at"),
        "update_at": todo.get("update_at")
    }


def list_todos(todos) -> list:
    return [todo_serial(todo) for todo in todos]