def generate_readme():
    print("📝 Ultimate README.md Generator\n")

    # Basic Info
    title = input("Project Title: ")
    description = input("Short Description: ")
    github_user = input("GitHub Username (for badges): ")
    repo_name = input("Repository Name (for badges): ")
    github_link = input("GitHub Repo URL: ")

    # Features
    features = input("List key features (comma-separated): ").split(',')

    # Setup & Usage
    install_cmd = input("Installation Command (e.g., npm install): ")
    usage_cmd = input("Usage Command (e.g., npm start): ")

    # Docker (Optional)
    docker_support = input("Does your project use Docker? (y/n): ").lower()
    docker_cmd = ""
    if docker_support == "y":
        docker_cmd = input("Docker run/build command (e.g., docker-compose up): ")

    # Screenshot (Optional)
    screenshot_path = input("Path or URL to screenshot (or leave blank): ")

    # Contact
    author_name = input("Your Name: ")
    contact_email = input("Contact Email: ")

    # License
    license_type = input("License (e.g., MIT): ")

    # Begin Markdown Content
    badge = f"![Stars](https://img.shields.io/github/stars/{github_user}/{repo_name}?style=social)\n"
    screenshot_md = f"![Screenshot]({screenshot_path})\n" if screenshot_path else ""

    content = f"""# {title}

{badge}
{description}

🔗 [View on GitHub]({github_link})

---

## 📸 Screenshot

{screenshot_md}

---

## 🚀 Features
""" + ''.join([f"- {f.strip()}\n" for f in features]) + f"""
---

## 📦 Installation

```bash
{install_cmd}
