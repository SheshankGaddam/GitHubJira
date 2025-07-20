# 🔗 GitHub–Jira Webhook Integration using Flask & AWS EC2

---
## 📌 Project Overview
This project demonstrates an end-to-end automation between **GitHub** and **Atlassian Jira Cloud** using a custom **Flask API** hosted on an **AWS EC2 instance**. It listens to GitHub webhook events and creates or updates corresponding issues in Jira.

### 🔁 Workflow:
- 🔧 When a **GitHub issue is created**, a **Jira issue** is created with the same title as the summary.
- 💬 When a **comment is added** on the GitHub issue, it is **posted to the corresponding Jira issue**.

---

## ⚙️ Technologies Used
- 🐍 Python 3
- 🚀 Flask (REST API)
- ☁️ AWS EC2 (Ubuntu)
- 🔐 Atlassian Jira Cloud REST API
- 🔗 GitHub Webhooks
- 🔒 OAuth & Basic Auth
- 🌐 JSON-based request/response handling

---

## 📁 Folder Structure

.
├── github_Jira.py
└── README.md
---
## 🔑 Prerequisites

Before running this project, you must create an **API token** in Jira. Here's how:

1. Go to [https://id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens)
2. Click **Create API Token**
3. Enter a label (e.g., *GitHub-Jira Integration*) and click **Create**
4. Copy the token shown (you won’t see it again!)
5. Use your Atlassian account email + this token as credentials for all Jira API calls in the Python script

---
## ✅ Endpoints

| Endpoint       | Triggered By                  | Description                          |
|----------------|-------------------------------|--------------------------------------|
| `/createJIRA`  | GitHub "Issues" webhook       | Creates a Jira ticket from an issue  |
| `/addComment`  | GitHub "Issue comment" webhook| Adds comment to the Jira issue       |

---

## 🚀 Hosting & Setup Instructions

### Step-by-Step Guide:

1. **Launch an EC2 Ubuntu instance on AWS**
2. Connect to it using SSH:
   ```bash
   ssh -i <your-key.pem> ubuntu@<your-ec2-ip>
3. Clone this repo into your EC2 instance:
4. git clone <your-repo-url> Repo URL
5. cd <repo-folder> Repo Folder
6. Create a virtual environment and activate it:
7. python3 -m venv myenv
8. source myenv/bin/activate
9. Install all required dependencies (python and flask)
10. Run the Flask API:
    python3 github_Jira.py

11. Update EC2 Security Group to allow inbound traffic on port 5000
12. Configure GitHub Webhooks for your repository:
    - Payload URL: http://<your-ec2-ip>:5000/createJIRA
    - Content type: application/json
    - Events:
      - Issues → for /createJIRA
      - Issue comment → for /addComment

📊 Context Diagram
<img width="1024" height="970" alt="GithubJira_Integration" src="https://github.com/user-attachments/assets/abdacf3e-c746-4c77-8310-0aceae72bfac" />

🛡️ Error Handling
Handles missing or empty payloads gracefully

Validates presence of required fields (title, comment)

Logs all failed API responses from Jira with context

📌 To-Do / Enhancements
 Add token verification for webhook security

 Support multiple GitHub → Jira project mappings

 GitHub label → Jira label syncing

👨‍💻 Author
Sai Sheshank Gaddam
📧 gsaisheshank@gmail.com
🔗 https://www.linkedin.com/in/sheshank-gaddam-a32a49168/
