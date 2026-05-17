import json
from flask import Flask, render_template, abort

app = Flask(__name__)

HOMEPAGE_PATH = "data/home_page.json"
PROJECTS_PATH = "data/projects.json"

TECH_MAP = {
    "Python": "images/tech/python.png",
    "Flask": "images/tech/flask.png",
    "SQL": "images/tech/sql.png",
    "GCP": "images/tech/gcp.png",
    "Docker": "images/tech/docker.png",
    "Pandas": "images/tech/pandas.png",
    "SMTP": "images/tech/email.png",
    "Cron": "images/tech/cron.png"
}


def load_projects():
    with open(PROJECTS_PATH, "r") as file:
        data = json.load(file)

    if isinstance(data, dict):
        projects = data.get("projects", [])
    else:
        projects = data

    return format_tech_stack(projects)


def format_tech_stack(projects):
    for project in projects:
        project["tech_images"] = [
            {
                "name": tech,
                "image": TECH_MAP.get(tech, "images/tech/default.png")
            }
            for tech in project.get("tech_stack", [])
        ]

    return projects


@app.route("/")
def home():
    with open(HOMEPAGE_PATH, "r") as file:
        index_content = json.load(file)

    projects_data = load_projects()

    featured_ids = index_content.get("featured_projects", [])
    
    featured_projects = [
        project for project in projects_data
        if project.get("id") in featured_ids
    ]

    return render_template(
        "index.html",
        content=index_content,
        projects=featured_projects
    )


@app.route("/projects")
def projects():
    projects_data = load_projects()

    return render_template(
        "projects.html",
        projects=projects_data
    )


@app.route("/projects/<project_id>")
def project_detail(project_id):
    projects_data = load_projects()

    project = None

    for item in projects_data:
        if item.get("id") == project_id:
            project = item
            break

    if project is None:
        abort(404)

    return render_template(
        "project_detail.html",
        project=project
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)