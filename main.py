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

def main():
    repo_path = "C:\\Users\\ggalicia77\\Documents\\Weekly Reports\\dprt-se-report\\" # change this
    file_path = os.path.join(repo_path, "report\\G80812_GALICIA_Gustavo\\202504-202603_P5G\\202510_GALICIA_Gustavo.md")

    # Step 1: git pull
    print(run_cmd(["git", "pull", "origin", "main"], cwd=repo_path))

    today = datetime.now()
    today_str = today.strftime("%Y/%m/%d")
    weekday_str = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][today.weekday()]

    # Step 2: read file
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 3: check if today's entry exists
    if f"# {today_str}" in content:
        print("Entry for today already exists. Nothing to do.")
        return

    # Step 4: get yesterday's plan
    y_plan = extract_yesterdays_plan(content)

    # Step 5: build new entry
    new_entry = []
    new_entry.append(f"# {today_str} ({weekday_str})")
    new_entry.append("## 開始報告 9:30")
    if y_plan:
        new_entry.extend(y_plan)
    new_entry.append("\n## 終了報告 18:15")
    new_entry.append("### 本日の実施業務\n")
    new_entry.append("\n### 今後の予定\n\n")
    new_entry.append("-----------------------------------------------------")

    new_entry_text = "\n".join(new_entry) + "\n\n\n"

    # Step 6: prepend new entry
    new_content = new_entry_text + content

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    # Step 7: git add, commit, push
    run_cmd(["git", "add", file_path], cwd=repo_path)
    run_cmd(["git", "commit", "-m", f"Added daily entry for {today_str}"], cwd=repo_path)
    print(run_cmd(["git", "push", "origin", "main"], cwd=repo_path))

if __name__ == "__main__":
    main()
