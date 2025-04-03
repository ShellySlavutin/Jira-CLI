Jira CLI Tool
This Python-based Command Line Interface (CLI) allows you to interact with Jira to perform the following operations:

Setup your Jira account by configuring the email, domain, and API token.

Fetch issue details from a specific Jira project.

Create new issues in a specified Jira project.

Requirements
Python 3.x
requests library for making HTTP requests.


The script first allows you to set up your Jira account by entering your email, domain, and API token.

Steps:
Enter your Jira email (e.g., your-email@example.com).

Enter your Jira domain (e.g., mycompany for the URL mycompany.atlassian.net).

Enter your Jira API token (which can be generated from Jira's API token page).

Once setup is complete, the CLI will check the credentials and display whether the setup was successful or failed.

Features
Get Issue
Allows you to fetch issue details from a specified project.
You will be prompted to provide a project name and issue type (e.g., Task, Bug, Story).
It retrieves and displays the list of issues of the specified type.

Create Issue
Allows you to create a new issue in a specified project.
You will be prompted for a project name, issue type, and issue summary.
Available issue types are fetched dynamically from the Jira project metadata.

After selecting the issue type and providing a summary, an issue will be created in Jira.

Code Breakdown
setup()
Prompts the user to enter their Jira credentials (email, domain, and API token).
Verifies the credentials by making a request to the Jira API.

get_issue()
Fetches all issues from a specified project based on the issue type entered by the user.
Uses Jira's JQL (Jira Query Language) to search for issues in the specified project and type.

create_issue()
Prompts the user to enter a project name, issue type, and summary.
Fetches available issue types for the project from Jira's metadata API.
Creates a new issue in Jira with the provided details.

switch_case()
A simple function to map user input to the corresponding function (either get_issue() or create_issue()).

get_input()
Prompts the user to select an operation (Get Issue, Create Issue, or Exit).

main()
The main function that initializes the setup and handles the menu-based selection of operations.

Usage
Run the script:

Configure your Jira account.

Fetch an issue by entering a project name and issue type.

Create a new issue by providing the necessary details.


Conclusion
This simple Jira CLI tool allows users to interact with Jira, perform common tasks such as fetching issues or creating new issues directly from the command line. It integrates with Jira's REST API to perform actions dynamically.

If you have any questions or need further assistance, feel free to reach out!
