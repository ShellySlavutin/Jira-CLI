# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

template_url = "https://%s.atlassian.net/rest/api/2/project"

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps( {
  "assigneeType": "PROJECT_LEAD",
  "avatarId": 10200,
  "categoryId": 10120,
  "description": "Cloud migration initiative",
  "issueSecurityScheme": 10001,
  "key": "EX",
  "leadAccountId": "5b10a0effa615349cb016cd8",
  "name": "Example",
  "notificationScheme": 10021,
  "permissionScheme": 10011,
  "projectTemplateKey": "com.atlassian.jira-core-project-templates:jira-core-simplified-process-control",
  "projectTypeKey": "business",
  "url": "http://atlassian.com"
} )



def setup():
    print("Hello! you have chosen the setup option\n"
          "Here we will configure you to your Jira account\n")
    userEmail = input("Please enter your email, for example : example@gmail.com ")  # shelly.slavutin@gmail.com
    userDomain = input("Please enter your domain, for example : mydomainname ")  # shellyslavutin
    userAPItoken = input("Please enter your API token ")  # ATATT3xFfGF02PcgYEg6FjivznPNLnBkScUz0dg2_oH48CGrYNHyQV-ECT_wWkrtpq7p-TYh4D8VE_kOjHombKcjlSlTXqpc7EZHSkciVHtqMjH3iUBiy4feba8K7OpbkcRFtfik8GeKpsXqziSvjVza4xw7-yz-rOJOS6h7CIb5em1_O0Zp9Jg=9459A319

    global url
    url = template_url % userDomain

    global auth
    auth = HTTPBasicAuth(userEmail, userAPItoken)

    print("checking validity of the setup...")
    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code >= 400:
        print("setup failed!")
        print("Status Code:", response.status_code)
    else:
        print("setup successful!")


def get_issue():
    print("Hello! you have chosen the get issue option\n")
    userProject = input("Please enter your project name ")
    projectKey = None
    projectID = None

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            if project['name'] == userProject:
                projectKey = project['key']
                projectID = project['id']
        if projectKey == None or projectID == None:
            print("Project does not exist!")
        else:
            print("The project has been found!")
            issueName = input("Enter issue name ")
            issue_url = url + "/" + projectID + "/" + issueName
            response = requests.get(url, headers=headers, auth=auth)
            print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    else:
        print(f"Failed to fetch projects: {response.status_code}")


def create_issue():
    print("Hello! you have chosen the create issue option\n")
    userProject = input("Please enter your project name ")
    projectKey = None
    projectID = None

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            if project['name'] == userProject:
                projectKey = project['key']
                projectID = project['id']
        if projectKey == None or projectID == None:
            print("Project does not exist!")
        else:
            print("The project has been found!")
            issueName = input("Enter issue name ")
            issueSummary = input("Enter issue summary ")

            payload = json.dumps(
            {
              "fields": {
                "project": { "key": projectKey},
                "summary": issueSummary,
                "issuetype": { "name": issueName}
              }
            } )

            issue_url = url + "/issue"
            response = requests.post(url, date=payload, headers=headers, auth=auth)
    else:
        print(f"Failed to fetch projects: {response.status_code}")


def switch_case(case):
    """
    switch case for the functions
    :param case: the user choice
    :return: the function
    """
    cases = {
        1: setup,
        2: get_issue,
        3: create_issue,
    }
    return cases.get(case)


def get_input():
    """
    gets the user choice
    :return: the user's choice
    """
    request_number = 0
    while True:
        # The loops keeps executing until the value entered is an integer
        try:
            request_number = int(input("""Please select sniffing state:
1: setup
2: get issue,
3: create issue,
Or select 0 to Exit: """))
            if request_number < 0 or request_number > 4:
                continue
            break
        except Exception as e:
            print("Error: ", e)
            print("Please try again")
            continue

    return request_number


def main():
    choice = -1
    print("Welcome to Jira CLI!")
    while choice != 0:

        choice = get_input()

        # exit the loop
        if choice == 0:
            exit()

        # get the correct function according to the user's choice
        selected_case = switch_case(choice)
        if selected_case:
            selected_case()


if __name__ == "__main__":
    main()
