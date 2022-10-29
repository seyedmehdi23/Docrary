from flask import Flask, render_template, send_from_directory, redirect, url_for, request, session
from os import listdir
from os.path import isfile, join
from markdown2 import markdown
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

home_path = "contents/home.md"
pages_path = "contents/pages/"
microData_path = "contents/micro_data.json"

@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("assets", path)

@app.route("/contents/images/<path:path>")
def send_images_contents(path):
    return send_from_directory("contents/images", path)


@app.route("/")
def index():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    user_data = []
    pages = []
    html_content = ""
    team = []
    # if 'username' in session:
    if True:
        home_contents = open(home_path, encoding="utf8")
        html_content = markdown(home_contents.read(), extras=["break-on-newline", "tables", "task_list", "fenced-code-blocks", 'md_mermaid'])
        # html_content = markdown(home_contents.read(), extensions=["tables", "md_mermaid"])

        pages_files = [f for f in listdir(pages_path) if isfile(join(pages_path, f))]
        for pfile in pages_files:
            title = pfile.split(".")[0]
            page = {
                "title" : title,
                "link" : pfile
            }
            pages.append(page)
        
        micro_data_file = open(microData_path)
        micro_data = micro_data_file.read()
        roles = json.loads(micro_data)["Roles"]

        return render_template("page.html", pages=pages, page_title="Home", content=html_content, user_data=user_data, team_roles=roles)
    else:
        return redirect(url_for("login"))

@app.route("/<path:path>")
def get_page(path):
    user_data = []
    pages = []
    html_content = ""

    # if 'username' in session:
    if True:
        page_contents = open(pages_path + path, encoding="utf8")
        html_content = markdown(page_contents.read(), extras=["break-on-newline", "tables", "task_list", "fenced-code-blocks"])

        page_title = path.split(".")[0]
        pages_files = [f for f in listdir(pages_path) if isfile(join(pages_path, f))]
        for pfile in pages_files:
            title = pfile.split(".")[0]
            page = {
                "title" : title,
                "link" : pfile
            }
            pages.append(page)

        micro_data_file = open(microData_path)
        micro_data = micro_data_file.read()
        roles = json.loads(micro_data)["Roles"]

        return render_template("page.html", pages=pages, page_title=page_title, content=html_content, user_data=user_data, current_page=path, team_roles=roles)
    else:
        return redirect(url_for("login"))

@app.route("/e<path:path>")
def edit_page(path):
    user_data = []
    pages = []
    html_content = ""

    # if 'username' in session:
    if True:
        page_contents = open(pages_path + path, encoding="utf8")
        html_content = page_contents.read()
        # markdown(page_contents.read(), extras=["break-on-newline", "tables", "task_list", "fenced-code-blocks"])

        page_title = path.split(".")[0]
        pages_files = [f for f in listdir(pages_path) if isfile(join(pages_path, f))]
        for pfile in pages_files:
            title = pfile.split(".")[0]
            page = {
                "title" : title,
                "link" : pfile
            }
            pages.append(page)
        return render_template("edit_page.html", pages=pages, page_title=page_title, content=html_content, user_data=user_data, target_page=path)
    else:
        return redirect(url_for("login"))

@app.route("/update_page", methods=["POST"])
def update_page():
    if True:
        md_contents = request.form["md_contents"]
        target_page = request.form["target_page"]

        page_contents = open(pages_path + target_page, "w")
        page_contents.write(md_contents)
        
        return redirect(f"/{target_page}")
    else:
        return redirect(url_for("login"))


@app.route("/questions")
def questions():
    pages = []
    user_data = []
    if True:
        pages_files = [f for f in listdir(pages_path) if isfile(join(pages_path, f))]
        for pfile in pages_files:
            title = pfile.split(".")[0]
            page = {
                "title" : title,
                "link" : pfile
            }
            pages.append(page)
    else:
        return redirect(url_for("login"))
    return render_template("questions.html", pages=pages, page_title="Questions & Issues", user_data=user_data)

@app.route("/login")
def login():
    if 'username' in session:
        return redirect(url_for("home"))
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True)