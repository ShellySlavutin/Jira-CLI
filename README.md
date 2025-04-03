# README

## Jira CLI Tool

This Python-based Command Line Interface (CLI) allows you to interact with Jira to perform the following operations:

- Setup your Jira account by configuring the email, domain, and API token.
- Fetch issue details from a specific Jira project.
- Create new issues in a specified Jira project.

### Requirements

- Python 3.x
- `requests` library for making HTTP requests.

To install the necessary Python package, use:

```bash
pip install requests
```

### Setup Jira CLI

The script first allows you to set up your Jira account by entering your email, domain, and API token.

#### Steps:

1. Enter your **Jira email** (e.g., `your-email@example.com`).
2. Enter your **Jira domain** (e.g., `mycompany` for the URL `mycompany.atlassian.net`).
3. Enter your **Jira API token** (which can be generated from Jira's API token page).

Once setup is complete, the CLI will check the credentials and display whether the setup was successful or failed.

### Features

1. **Get Issue**
   - Allows you to fetch issue details from a specified project.
   - You will be prompted to provide a project name and issue type (e.g., Task, Bug, Story).
   - It retrieves and displays the list of issues of the specified type.

2. **Create Issue**
   - Allows you to create a new issue in a specified project.
   - You will be prompted for a project name, issue type, and issue summary.
   - Available issue types are fetched dynamically from the Jira project metadata.
   - After selecting the issue type and providing a summary, an issue will be created in Jira.

### Code Breakdown

#### `setup()`
- Prompts the user to enter their Jira credentials (email, domain, and API token).
- Verifies the credentials by making a request to the Jira API.

#### `get_issue()`
- Fetches all issues from a specified project based on the issue type entered by the user.
- Uses Jira's **JQL (Jira Query Language)** to search for issues in the specified project and type.

#### `create_issue()`
- Prompts the user to enter a project name, issue type, and summary.
- Fetches available issue types for the project from Jira's metadata API.
- Creates a new issue in Jira with the provided details.

#### `switch_case()`
- A simple function to map user input to the corresponding function (either `get_issue()` or `create_issue()`).

#### `get_input()`
- Prompts the user to select an operation (Get Issue, Create Issue, or Exit).

#### `main()`
- The main function that initializes the setup and handles the menu-based selection of operations.

### Usage

1. Run the script:

```bash
python jira_cli.py
```

2. Follow the prompts to:
   - **Configure** your Jira account.
   - **Fetch an issue** by entering a project name and issue type.
   - **Create a new issue** by providing the necessary details.

### Example Interaction

```bash
Welcome to Jira CLI!
Hello! let's configure your Jira account!
Please enter your email (e.g., example@gmail.com): your-email@example.com
Please enter your domain (e.g., mydomainname): mycompany
Please enter your API token: your-api-token

Checking validity of the setup...
Setup successful!

Please select an option:
1: Get Issue
2: Create Issue
0: Exit
```

### Error Handling

The script will notify you if:
- Your credentials are incorrect.
- The project name does not exist.
- The issue creation or fetching process fails.

### Assumptions and Limitations
API Access: The script assumes you have valid Jira credentials (email and API token) and the correct permissions to access the Jira projects and issues.

Project Access: The user must know the project name and issue types beforehand. The script does not validate the availability of the project until the user provides this input.

Issue Type Support: The script supports basic issue types such as Bug, Task, Story, and Epic, but if your Jira setup has custom issue types, they may not be included in the available options unless they are explicitly fetched via Jira metadata.

Limited Error Handling: While basic error handling for failed requests and invalid inputs is in place, more complex error scenarios (e.g., network issues, timeouts, permission errors) might not be fully addressed.

### Conclusion

This simple Jira CLI tool allows users to interact with Jira, perform common tasks such as fetching issues or creating new issues directly from the command line. It integrates with Jira's REST API to perform actions dynamically.

If you have any questions or need further assistance, feel free to reach out!
