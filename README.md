
## Usage Instructions

This script allows you to search for a specific string in the company GitHub repositories. It can list all repositories of an organization, perform searches in the listed repositories, or both.

### Requirements

- Python 3.x

### Installation

1. Clone the repository or download the code.
2. Install the necessary dependencies.

### Usage

To run the script, use the command:

```sh
python searcher.py [options]
```

### Options

- `-h, --help`: Shows the help message and exit.
- `-t, --token`: (Required) Your GitHub access token.
- `-o, --org_name`: (Required) GitHub organization name.
- `-f, --filename`: Output filename for the list of all repositories of the company. (Default: `org_repos.txt`)
- `-s, --string_to_search`: (Required) String to search for in the repositories.
- `-d, --delay_time`: Delay time between requests. Be careful with this value because the GitHub API has rate limits. (Default: `6`)
- `-m, --mode`: Mode of the program. Can be `only_list_all_repos`, `search_in_current_list`, or `both`. (Default: `both`, choices: `only_list_all_repos`, `search_in_current_list`, `both`)

### Usage Examples

1. List all repositories and search for the string "Hello" in the repositories:
    ```sh
    python searcher.py -t your-access-token -s Hello
    ```

2. List all repositories without searching for the string:
    ```sh
    python searcher.py -t your-access-token -s Hello -m only_list_all_repos
    ```

3. Search for the string "Hello" in the current list of repositories:
    ```sh
    python searcher.py -t your-access-token -s Hello -m search_in_current_list
    ```

4. Specify the delay time between requests:
    ```sh
    python searcher.py -t your-access-token -s Hello -d 10
    ```

5. Use a custom filename for the repository list:
    ```sh
    python searcher.py -t your-access-token -s Hello -f custom_repos_list.txt
    ```

### Notes

- Make sure not to share your GitHub access token publicly.
- Adjust the delay time between requests (`--delay_time`) according to the GitHub API rate limits.
- Some times you'll get request errors (e.g. `403` status code), those errored repositories will be added to a separate file. You can add this list to the `org_repos.txt` file to be the new input, then you can try to run the script again using the `search_in_current_list` option mode.