import json
from flask import Flask, render_template, abort

app = Flask(__name__)

HOMEPAGE_PATH = "data/home_page.json"
PROJECTS_PATH = "data/projects.json"


def load_projects():
    with open(PROJECTS_PATH, "r") as file:
        data = json.load(file)

    if isinstance(data, dict):
        projects = data.get("projects", [])
    else:
        projects = data

    return add_tech_images(projects)

@app.route("/")
def home():
    with open(HOMEPAGE_PATH, "r") as file:
        content = json.load(file)

    projects = load_projects()

    featured_ids = content.get("featured_projects", [])

    featured_projects = [
        project for project in projects
        if project.get("id") in featured_ids
    ]

    return render_template(
        "index.html",
        content=content,
        projects=featured_projects
    )


@app.route("/projects")
def projects():
    return render_template(
        "projects.html",
        projects=load_projects()
    )


@app.route("/projects/<project_id>")
def project_detail(project_id):
    projects = load_projects()

    project = next(
        (item for item in projects if item.get("id") == project_id),
        None
    )

    if project is None:
        abort(404)

    return render_template(
        "project_detail.html",
        project=project
    )
def add_tech_images(projects):
    for project in projects:
        project["tech_images"] = [
            {
                "name": tech,
                "image": f"images/tech/{tech.lower().replace(' ', '')}.png"
            }
            for tech in project.get("tech", [])
        ]
    return projects

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/education")
def education():
    return render_template("education.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
