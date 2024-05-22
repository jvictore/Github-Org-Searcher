import argparse
import requests
import time


def fetch_all_repos(token, org_name, delay_time):
    # Initial configuration to access the GitHub API
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{org_name}/repos?page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error accessing page {page} data: {response.status_code}")
            break
        else:
            print(f"Page {page} accessed successfully")
        data = response.json()
        if not data:
            break
        for repo in data:
            repos.append(repo["name"])
        page += 1
        time.sleep(delay_time)  # 6-second pause between requests to avoid rate limiting

    # Save the repository names to a file
    filename = f"{org_name}_repos.txt"
    save_to_file(repos, filename)
    print(f"All repositories have been saved to '{filename}'")
    print("________________________________________________")

    return


def save_to_file(repos, filename):
    with open(filename, "w") as file:
        for repo in repos:
            file.write(repo + "\n")


def search_string_in_repos(token, org_name, filename, string_to_search, delay_time):
    # Initial configuration to access the GitHub API
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Reading repository names from the file
    with open(filename, "r") as file:
        all_repos = [line.strip() for line in file]

    found_repos = []
    error_repos = []

    # Search for the string in each repository
    for repo_name in all_repos:
        search_url = f"https://api.github.com/search/code?q={string_to_search}+in:file+repo:{org_name}/{repo_name}"
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            print(f"Search done in {repo_name}...")
            data = response.json()
            if data["total_count"] > 0:
                found_repos.append(repo_name)
        else:
            print(f"Error searching in {repo_name}: {response.status_code}")
            error_repos.append(repo_name)

        time.sleep(delay_time)  # 6 seconds pause between requests

    # Saving found results to a file
    with open("repos_containing_string.txt", "w") as file:
        for repo in found_repos:
            file.write(repo + "\n")

    # Saving error results to a file
    with open("repos_with_error_to_access.txt", "w") as file:
        for repo in error_repos:
            file.write(repo + "\n")

    print(f"Total repositories containing '{string_to_search}': {len(found_repos)}")

    return


def main():
    parser = argparse.ArgumentParser(
        description="Search for some string in GitHub repositories."
    )
    parser.add_argument(
        "-t", "--token", required=True, help="Your GitHub access token."
    )
    parser.add_argument(
        "-o", "--org_name", required=True, help="GitHub organization name."
    )
    parser.add_argument(
        "-f",
        "--filename",
        help="Output filename for the list of all repositories of the company.",
        default="org_repos.txt",
    )
    parser.add_argument(
        "-s",
        "--string_to_search",
        required=True,
        help="String to search in the repositories.",
    )
    parser.add_argument(
        "-d",
        "--delay_time",
        help="Delay time between requests. Be careful with this value, because Github API have rate limits.",
        type=int,
        default=6,
    )
    parser.add_argument(
        "-m",
        "--mode",
        help="Mode of the program. Can be 'only_list_all_repos', 'search_in_current_list' or 'both'.",
        default="both",
        choices=["only_list_all_repos", "search_in_current_list", "both"],
    )

    args = parser.parse_args()

    access_token = args.token
    org_name = args.org_name
    filename = args.filename
    string_to_search = args.string_to_search
    delay_time = args.delay_time
    mode = args.mode

    if mode == "only_list_all_repos" or mode == "both":
        # Call the function to retrieve all repositories and save them to a file
        fetch_all_repos(access_token, org_name, delay_time)

    if mode == "search_in_current_list" or mode == "both":
        # Call the function to do the search in the repositories
        search_string_in_repos(
            access_token, org_name, filename, string_to_search, delay_time
        )


if __name__ == "__main__":
    main()
