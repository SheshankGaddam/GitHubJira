from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__)

# JIRA config (you may use env vars in production)
JIRA_URL = "https://gsaisheshank.atlassian.net"
API_TOKEN = ""
EMAIL = "yourConfiguredEmail@gmail.com"
PROJECT_KEY = "SGIT"
ISSUE_TYPE_ID = "10016"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


# ========== 1️⃣ Create JIRA from GitHub Issue ==========
@app.route("/createJIRA", methods=["POST"])
def create_jira():
    try:
        data = request.get_json()

        issue_title = data.get("issue", {}).get("title")
        if not issue_title:
            return jsonify({"error": "Missing GitHub issue title"}), 400

        payload = {
            "fields": {
                "project": {
                    "key": PROJECT_KEY
                },
                "summary": issue_title,
                "issuetype": {
                    "id": ISSUE_TYPE_ID
                },
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Created from GitHub issue webhook"
                                }
                            ]
                        }
                    ]
                }
            }
        }

        response = requests.post(
            f"{JIRA_URL}/rest/api/3/issue",
            headers=headers,
            auth=auth,
            data=json.dumps(payload)
        )

        if response.status_code >= 400:
            return jsonify({"error": "Failed to create JIRA", "details": response.text}), response.status_code

        return jsonify({"message": "JIRA issue created", "response": response.json()}), 201

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500


# ========== 2️⃣ Add Comment to JIRA ==========
@app.route("/addComment", methods=["POST"])
def add_comment():
    try:
        data = request.get_json()

        issue_title = data.get("issue", {}).get("title")
        comment_body = data.get("comment", {}).get("body")

        if not issue_title:
            return jsonify({"error": "Missing GitHub issue title"}), 400

        if not comment_body:
            return jsonify({"message": "No comment to post, skipping JIRA comment"}), 204

        # Search JIRA issue by summary (GitHub title)
        jql = f'summary ~ "{issue_title}" ORDER BY created DESC'
        search_response = requests.get(
            f"{JIRA_URL}/rest/api/3/search?jql={jql}",
            headers=headers,
            auth=auth
        )

        if search_response.status_code != 200:
            return jsonify({"error": "Failed to search JIRA issue", "details": search_response.text}), 500

        issues = search_response.json().get("issues", [])
        if not issues:
            return jsonify({"error": "No matching JIRA issue found"}), 404

        issue_key = issues[0]["key"]

        comment_payload = {
            "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment_body
                        }
                    ]
                }
            ]
        }
    }

        comment_response = requests.post(
            f"{JIRA_URL}/rest/api/3/issue/{issue_key}/comment",
            headers=headers,
            auth=auth,
            data=json.dumps(comment_payload)
        )

        if comment_response.status_code >= 400:
            return jsonify({"error": "Failed to add comment to JIRA", "details": comment_response.text}), comment_response.status_code

        return jsonify({"message": f"Comment added to JIRA issue {issue_key}"}), 200

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)

