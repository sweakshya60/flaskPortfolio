from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
db = SQLAlchemy(app)


class Experience(db.Model):
    ex_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.ex_id} - {self.title}"


def truncate_string(s, length):
    if len(s) <= length:
        return s
    else:
        return s[:length] + "..."  # slicing


@app.route("/")
def landing_page():

    allEx = Experience.query.all()
    infos = Info.query.all()
    skills = Skill.query.all()

    # Truncate descriptions for each skill
    for skill in skills:
        skill.truncated_desc = truncate_string(skill.desc, 150)

    # Truncate descriptions for each experience
    for experience in allEx:
        experience.truncated_desc = truncate_string(experience.desc, 150)

    # Initialize an empty dictionary to store key-value pairs
    info_dict = {}

    # Iterate through each Info object and populate the dictionary

    for info in infos:
        info_dict[info.key] = info.value

    return render_template(
        "front/landing_page.html", allEx=allEx, info_dict=info_dict, skills=skills
    )
    # return "<p>Hello, World!</p>"


@app.route("/admin/experience/create")
def create_experince():
    return render_template("admin/experience/create.html")


@app.route("/admin/experience/create", methods=["POST"])
def add_experience():
    title = request.form["title"]
    description = request.form["description"]
    new_experience = Experience(title=title, desc=description)
    db.session.add(new_experience)
    db.session.commit()
    return redirect("/admin/experience")


# Route to edit an experience
@app.route("/admin/experience/edit/<int:id>", methods=["GET", "POST"])
def edit_experience(id):
    experience = Experience.query.get_or_404(id)
    if request.method == "POST":
        experience.title = request.form["title"]
        experience.desc = request.form["description"]
        db.session.commit()
        return redirect("/admin/experience")
    return render_template("admin/experience/edit.html", experience=experience)


# Route to delete an experience
@app.route("/admin/experience/delete/<int:id>", methods=["GET"])
def delete_experience(id):
    experience = Experience.query.get_or_404(id)
    db.session.delete(experience)
    db.session.commit()
    return redirect("/admin/experience")


@app.route("/admin/experience")
def list_experiences():
    experiences = Experience.query.all()
    return render_template("admin/experience/list.html", experiences=experiences)


# skill


class Skill(db.Model):
    ex_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.ex_id} - {self.title}"


@app.route("/admin/skill/create")
def create_skill():
    return render_template("admin/skill/create.html")


@app.route("/admin/skill/create", methods=["POST"])
def add_skill():
    title = request.form["title"]
    description = request.form["description"]
    new_skill = Skill(title=title, desc=description)
    db.session.add(new_skill)
    db.session.commit()
    return redirect("/admin/skill")


# Route to edit an skill
@app.route("/admin/skill/edit/<int:id>", methods=["GET", "POST"])
def edit_skill(id):
    skill = Skill.query.get_or_404(id)
    if request.method == "POST":
        skill.title = request.form["title"]
        skill.desc = request.form["description"]
        db.session.commit()
        return redirect(url_for("list_skills"))
    return render_template("admin/skill/edit.html", skill=skill)


# Route to delete an skill
@app.route("/admin/skill/delete/<int:id>", methods=["GET"])
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    return redirect(url_for("list_skills"))


@app.route("/admin/skill")
def list_skills():
    skills = Skill.query.all()
    return render_template("admin/skill/list.html", skills=skills)


# infooo
class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(200), nullable=False)
    value = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.key} - {self.value}"


@app.route("/admin/info/create")
def create_info():
    return render_template("admin/info/create.html")


@app.route("/admin/info/create", methods=["POST"])
def add_info():
    key = request.form["key"]
    value = request.form["value"]
    new_info = Info(key=key, value=value)
    db.session.add(new_info)
    db.session.commit()
    return redirect("/admin/info")


# Route to edit an info
@app.route("/admin/info/edit/<int:id>", methods=["GET", "POST"])
def edit_info(id):
    info = Info.query.get_or_404(id)
    if request.method == "POST":
        info.key = request.form["key"]
        info.value = request.form["value"]
        db.session.commit()
        return redirect(url_for("list_infos"))
    return render_template("admin/info/edit.html", info=info)


# Route to delete an info
@app.route("/admin/info/delete/<int:id>", methods=["GET"])
def delete_info(id):
    info = Info.query.get_or_404(id)
    db.session.delete(info)
    db.session.commit()
    return redirect(url_for("list_infos"))


@app.route("/admin/info")
def list_infos():
    infos = Info.query.all()
    return render_template("admin/info/list.html", infos=infos)

# about  page
@app.route("/about")
def about():
    return render_template("front/about.html")


# services


class Service(db.Model):
    ser_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.ser_id} - {self.title}"


@app.route("/admin/service/create")
def create_service():
    return render_template("admin/service/create.html")


@app.route("/admin/service/create", methods=["POST"])
def add_service():
    title = request.form["title"]
    description = request.form["description"]
    new_service = Service(title=title, desc=description)
    db.session.add(new_service)
    db.session.commit()
    return redirect("/admin/service")


# Route to edit an service
@app.route("/admin/service/edit/<int:id>", methods=["GET", "POST"])
def edit_service(id):
    service = Service.query.get_or_404(id)
    if request.method == "POST":
        service.title = request.form["title"]
        service.desc = request.form["description"]
        db.session.commit()
        return redirect(url_for("list_services"))
    return render_template("admin/service/edit.html", service=service)


# Route to delete an service
@app.route("/admin/service/delete/<int:id>", methods=["GET"])
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for("list_services"))


@app.route("/admin/service")
def list_services():
    services = Service.query.all()
    return render_template("admin/service/list.html", services=services)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
