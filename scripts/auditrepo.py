import os
import re

# Paths to check
repo_path = "./"  # adjust if needed

def find_hardcoded_secrets(path):
    secret_patterns = [
        r'API_KEY\s*=\s*["\'].*["\']',
        r'PASSWORD\s*=\s*["\'].*["\']',
        r'PRIVATE_KEY\s*=\s*["\'].*["\']',
        r'TOKEN\s*=\s*["\'].*["\']',
    ]
    findings = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".env", ".json")):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for pattern in secret_patterns:
                        if re.search(pattern, content):
                            findings.append((filepath, pattern))
    return findings

def main():
    print("Starting repo audit...")
    secrets = find_hardcoded_secrets(repo_path)
    if secrets:
        print("Found potential hardcoded secrets:")
        for filepath, pattern in secrets:
            print(f" - {filepath} matches {pattern}")
    else:
        print("No hardcoded secrets found.")

if __name__ == "__main__":
    main()
