from .helper import build_tree, tree_to_string, build_file_content_dict, get_github_files, get_file_content, parse_github_url, build_tree_from_github_files

def get_local_file_and_content(folder_path):
    tree = build_tree(folder_path)
    file_content_dict = build_file_content_dict(folder_path)
    folder_structure = tree_to_string(tree)

    print(file_content_dict)
    return folder_structure, file_content_dict

def get_github_file_and_content(repo_url):
    owner, repo, branch = parse_github_url(repo_url)
    if not owner or not repo:
        raise ValueError("Both 'owner' and 'repo' are required.")

    files = get_github_files(owner, repo, branch)

    if not files:
        raise ValueError("Files couldn't found.")

    result = {}

    for file in files:
        file_path = file['path']
        file_sha = file['sha']
        content = get_file_content(owner, repo, file_sha)

        if content is not None:
            result[file_path] = content

    if not result:
        raise ValueError("Unable to fetch file contents.")

    tree = build_tree_from_github_files(files, repo)
    folder_structure = tree_to_string(tree)

    return folder_structure, result


