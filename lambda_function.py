import json

from container import container


def lambda_handler(event: dict, context) -> dict:
    http_method = event["httpMethod"]
    path = event["path"]

    if path == "/todos" and http_method == "POST":
        response = container.todo_controller.create_todo(event)
    elif path.startswith("/todos/") and http_method == "GET":
        response = container.todo_controller.get_todo(event)
    elif path.startswith("/todos/") and http_method == "PUT":
        response = container.todo_controller.update_todo(event)
    elif path.startswith("/todos/") and http_method == "DELETE":
        response = container.todo_controller.delete_todo(event)
    else:
        response = {"statusCode": 404, "body": {"message": "Not Found"}}

    return {
        "statusCode": response["statusCode"],
        "body": json.dumps(response["body"]),
    }
