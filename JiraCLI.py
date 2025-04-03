import requests
from requests.auth import HTTPBasicAuth
import json

# Template URL for project-related requests
template_url = "https://%s.atlassian.net/rest/api/2/project"

# Headers for the API requests
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def setup():
    """
    Setup function to configure the Jira instance with the user's credentials
    """
    print("Hello! let's configure your Jira account!")

    # Get user input for email, domain, and API token
    userEmail = input("Please enter your email (e.g., example@gmail.com): ")

    global userDomain
    userDomain = input("Please enter your domain (e.g., mydomainname): ")

    userAPItoken = input("Please enter your API token: ")

    # Update global URL and authentication
    global url
    url = template_url % userDomain
    global auth
    auth = HTTPBasicAuth(userEmail, userAPItoken)

    print("Checking validity of the setup...")

    # Test the authentication by making a simple GET request
    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code >= 400:
        print("Setup failed!\n")
        return False
    elif response is None:
        print("Setup failed!\n")
        return False
    else:
        print("Setup successful!\n")
        return True


def get_issue():
    """
    Function to fetch details of an issue from a specific project
    """
    print("You have chosen the 'Get Issue' option.\n")

    # Get project name from the user
    userProject = input("Please enter your project name: ")
    projectKey, projectID = None, None

    # Fetch project details
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            if project['name'] == userProject:
                projectKey = project['key']
                projectID = project['id']

        if not projectKey or not projectID:
            print("Project does not exist!")
        else:
            print("The project has been found!")
            issueType = input("Enter issue type (e.g., Bug, Task, Story): ")

            # JQL query to search for issues in a specific project and type
            search_url = f"https://{userDomain}.atlassian.net/rest/api/2/search"
            jql_query = f'project = "{projectKey}" AND issuetype = "{issueType}"'

            # Define the payload for the search request
            payload = {
                "jql": jql_query,
                "fields": ["summary", "status", "key"],  # Specify which fields to retrieve
                "maxResults": 10  # Adjust the number of results
            }

            # Make the search request
            try:
                response = requests.get(search_url, headers=headers, auth=auth, params=payload)

                if response.status_code == 200:
                    issues = response.json().get("issues", [])
                    if issues:
                        print(f"Found {len(issues)} issue(s) of type '{issueType}' in project '{userProject}':")
                        for issue in issues:
                            print(f"Issue Key: {issue['key']}, Summary: {issue['fields']['summary']}, Status: {issue['fields']['status']['name']}")
                    else:
                        print(f"No issues found of type '{issueType}' in project '{userProject}'.")

                else:
                    print(f"Failed to fetch issues: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}. Please try again.\n")
    else:
        print(f"Failed to fetch projects: {response.status_code}, {response.text}")


def create_issue():
    """
    Function to create a new issue in a specified project
    """
    print("You have chosen the 'Create Issue' option.\n")

    # Get project name from the user
    userProject = input("Please enter your project name: ")
    projectKey, projectID = None, None

    # Fetch project details
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            if project['name'] == userProject:
                projectKey = project['key']
                projectID = project['id']

        if not projectKey or not projectID:
            print("Project does not exist!")
            return

        print("The project has been found!")

        # Fetch available issue types using Jira's create metadata API
        metadata_url = f"https://{userDomain}.atlassian.net/rest/api/2/issue/createmeta?projectKeys={projectKey}"
        metadata_response = requests.get(metadata_url, headers=headers, auth=auth)

        if metadata_response.status_code == 200:
            metadata = metadata_response.json()
            available_issue_types = metadata['projects'][0]['issuetypes']
            print("Available issue types:")

            default_issue_type = 'Bug'
            for i, issue_type in enumerate(available_issue_types, 1):
                print(f"{i}: {issue_type['name']}")
                if i == 1 :
                    default_issue_type = issue_type['name']  # Use on of the outputs of the metadata as a default

            try:
                # Let the user select an issue type
                issueTypeChoice = int(input("Enter the number corresponding to the issue type: "))
                issueType = available_issue_types[issueTypeChoice - 1]['name']
            except (ValueError, IndexError):
                print("Invalid selection! using default.")
                issueType = default_issue_type

            # Get issue summary
            issueSummary = input("Enter issue summary: ")

            # Prepare the payload for the new issue creation
            payload = json.dumps({
                "fields": {
                    "project": {"key": projectKey},
                    "summary": issueSummary,
                    "issuetype": {"name": issueType}
                }
            })

            # Issue creation endpoint
            issue_url = f"https://{userDomain}.atlassian.net/rest/api/2/issue"
            response = requests.post(issue_url, data=payload, headers=headers, auth=auth)

            # Handle response
            if response.status_code == 201:
                issue_data = response.json()
                print(f"Issue created successfully! Issue Key: {issue_data['key']}")
            else:
                print(f"Failed to create issue: {response.status_code}")
                try:
                    print(response.json())
                except requests.exceptions.JSONDecodeError:
                    print("Response is not JSON:", response.text)
        else:
            print(f"Failed to fetch metadata for the project: {metadata_response.status_code}")
    else:
        print(f"Failed to fetch projects: {response.status_code}")


def switch_case(case):
    """
    Switch case for handling user options.
    :param case: User's choice
    :return: Corresponding function
    """
    cases = {
        1: get_issue,
        2: create_issue,
    }
    return cases.get(case)


def get_input():
    """
    Get the user's choice for which operation to perform.
    :return: User's choice
    """
    request_number = 0
    while True:
        try:
            request_number = int(input("""Please select an option:
1: Get Issue
2: Create Issue
0: Exit\n"""))
            if 0 <= request_number <= 2:
                break
        except Exception as e:
            print("Error:", e)
            print("Please try again.")
    return request_number


def main():
    """
    Main function to drive the menu-based operations.
    """
    choice = -1
    print("Welcome to Jira CLI!")
    status = setup()
    while status == False:
        status = setup()
    while choice != 0:
        choice = get_input()

        # Exit the program if the user selects 0
        if choice == 0:
            print("Exiting... Goodbye!")
            exit()

        # Execute the corresponding function based on user's choice
        selected_case = switch_case(choice)
        if selected_case:
            selected_case()


if __name__ == "__main__":
    main()
