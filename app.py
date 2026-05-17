import json
from flask import Flask, render_template, abort

app = Flask(__name__)

HOMEPAGE_PATH = "data/home_page.json"
PROJECTS_PATH = "data/projects.json"

@app.route("/")
def home():
    with open(HOMEPAGE_PATH, "r") as file:
        index_content = json.load(file)

    with open(PROJECTS_PATH, "r") as file:
        projects_data = json.load(file)

    featured_ids = index_content.get("featured_projects", [])

    featured_projects = [
        project for project in projects_data
        if project["id"] in featured_ids
    ]

    return render_template(
        "index.html",
        content=index_content,
        projects=featured_projects
    )

@app.route("/projects")
def projects():
    with open(PROJECTS_PATH, "r") as file:
        projects_data = json.load(file)

    return render_template(
        "projects.html",
        projects=projects_data
    )

@app.route("/projects/<project_id>")
def project_detail(project_id):
    with open(PROJECTS_PATH, "r") as file:
        projects_data = json.load(file)

    project = None

    for item in projects_data:
        if item["id"] == project_id:
            project = item
            break

    if project is None:
        abort(404)

    return render_template(
        "project_detail.html",
        project=project
    )