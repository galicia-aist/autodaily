import subprocess
import os
from datetime import datetime
import re


def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return result.stdout.strip()

def extract_yesterdays_plan(content):
    """Extract the last '### 今後の予定' section before today's date."""
    sections = re.split(r"^# \d{4}/\d{2}/\d{2}", content, flags=re.M)
    if len(sections) < 2:
        return []

    last_section = sections[1] if len(sections) == 2 else sections[1]
    # Find "### 今後の予定"
    match = re.search(r"### 今後の予定\s*\n(.*?)(\n###|\Z)", last_section, flags=re.S)
    if match:
        tasks = match.group(1).splitlines()
        tasks = [line for line in tasks if line.lstrip().startswith("*")]
        return tasks
    return []

def get_or_create_report_file(user: str, contract: str, repo_path: str) -> str:
    """
    Returns the path to the current month's report file.
    If it doesn't exist, creates it with a header.
    """
    # --- Get current year and month (YYYYMM) ---
    current_ym = datetime.now().strftime("%Y%m")

    # --- Extract last name from username for file naming ---
    user_lastname = user.split("_")[1]
    user_firstname = user.split("_")[2]

    # --- Build full file path ---
    file_dir = os.path.join(repo_path, "report", user, contract)
    os.makedirs(file_dir, exist_ok=True)  # create folders if missing

    file_name = f"{current_ym}_{user_lastname}_{user_firstname}.md"
    file_path = os.path.join(file_dir, file_name)

    # --- Create the file if it doesn't exist ---
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {current_ym} Report for {user_lastname}\n")
        print(f"Created new file: {file_path}")
    else:
        print(f"File already exists: {file_path}")

    return file_path