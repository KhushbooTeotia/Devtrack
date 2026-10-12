
import json
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Reporter,
    Issue,
    CriticalIssue,
    LowPriorityIssue,
)


REPORTERS_FILE = Path(settings.BASE_DIR) / "reporters.json"
ISSUES_FILE = Path(settings.BASE_DIR) / "issues.json"


# Read records from a JSON file
def read_json(file_path):
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Save records to a JSON file
def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# Generate the next available ID
def next_id(records):
    return max(
        (record["id"] for record in records),
        default=0,
    ) + 1


# Read and validate the incoming JSON body
def get_payload(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("Invalid JSON body")

    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object")

    return data


# Use a supplied ID or generate one
def make_id(data, records):
    record_id = data.get("id")

    if record_id is None:
        return next_id(records)

    if (
        isinstance(record_id, bool)
        or not isinstance(record_id, int)
        or record_id < 1
    ):
        raise ValueError("ID must be a positive integer")

    if any(record["id"] == record_id for record in records):
        raise ValueError("ID already exists")

    return record_id


def bad_request(message):
    return JsonResponse({"error": message}, status=400)


# REPORTER API
@csrf_exempt
def reporters_view(request):
    try:
        if request.method == "POST":
            data = get_payload(request)
            reporters = read_json(REPORTERS_FILE)

            reporter = Reporter(
                id=make_id(data, reporters),
                name=data.get("name"),
                email=data.get("email"),
                team=data.get("team"),
            )

            reporter.validate()

            reporters.append(reporter.to_dict())
            write_json(REPORTERS_FILE, reporters)

            return JsonResponse(
                reporter.to_dict(),
                status=201,
            )

        elif request.method == "GET":
            reporters = read_json(REPORTERS_FILE)
            reporter_id = request.GET.get("id")

            if reporter_id is None:
                return JsonResponse(reporters, safe=False)

            try:
                reporter_id = int(reporter_id)
                if reporter_id < 1:
                    raise ValueError
            except ValueError:
                return bad_request(
                    "ID must be a positive integer"
                )

            for reporter in reporters:
                if reporter["id"] == reporter_id:
                    return JsonResponse(reporter, status=200)

            return JsonResponse(
                {"error": "Reporter not found"},
                status=404,
            )

        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    except ValueError as error:
        return bad_request(str(error))
    except (OSError, json.JSONDecodeError):
        return JsonResponse(
            {"error": "Unable to read or write reporter data"},
            status=500,
        )


# ISSUE API
@csrf_exempt
def issues_view(request):
    try:
        if request.method == "POST":
            data = get_payload(request)
            issues = read_json(ISSUES_FILE)
            reporters = read_json(REPORTERS_FILE)

            reporter_id = data.get("reporter_id")

            if (
                isinstance(reporter_id, bool)
                or not isinstance(reporter_id, int)
                or reporter_id < 1
            ):
                raise ValueError(
                    "reporter_id must be a positive integer"
                )

            reporter_exists = any(
                reporter["id"] == reporter_id
                for reporter in reporters
            )

            if not reporter_exists:
                return JsonResponse(
                    {"error": "Reporter not found"},
                    status=404,
                )

            issue_data = {
                "id": make_id(data, issues),
                "title": data.get("title"),
                "description": data.get("description", ""),
                "status": data.get("status"),
                "priority": data.get("priority"),
                "reporter_id": reporter_id,
                "created_at": None,
            }

            if issue_data["priority"] == "critical":
                issue = CriticalIssue(**issue_data)
            elif issue_data["priority"] == "low":
                issue = LowPriorityIssue(**issue_data)
            else:
                issue = Issue(**issue_data)

            issue.validate()

            response_data = issue.to_dict()
            response_data["message"] = issue.describe()

            issues.append(issue.to_dict())
            write_json(ISSUES_FILE, issues)

            return JsonResponse(response_data, status=201)

        elif request.method == "GET":
            issues = read_json(ISSUES_FILE)
            issue_id = request.GET.get("id")
            status_filter = request.GET.get("status")

            if issue_id is not None:
                try:
                    issue_id = int(issue_id)
                    if issue_id < 1:
                        raise ValueError
                except ValueError:
                    return bad_request(
                        "ID must be a positive integer"
                    )

                for issue in issues:
                    if issue["id"] == issue_id:
                        return JsonResponse(issue, status=200)

                return JsonResponse(
                    {"error": "Issue not found"},
                    status=404,
                )

            if status_filter is not None:
                if status_filter not in Issue.ALLOWED_STATUSES:
                    return bad_request("Invalid status")

                issues = [
                    issue for issue in issues
                    if issue["status"] == status_filter
                ]

            return JsonResponse(
                issues,
                safe=False,
                status=200,
            )

        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    except ValueError as error:
        return bad_request(str(error))
    except (OSError, json.JSONDecodeError):
        return JsonResponse(
            {"error": "Unable to read or write issue data"},
            status=500,
        )