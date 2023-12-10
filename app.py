import json
import os
import re
import uuid

from flask import Flask, Response, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
# -> Verzeichnis des uploads
#app.config["TEMPLATES_FOLDER"] = "/app/templates/"
app.config["TEMPLATES_FOLDER"] = "./"

# -> Index Routing
@app.route("/")
def index():
    return render_template("index.html")

# -> Routing beim upload über POST 
@app.route("/upload", methods=["POST"])
def upload_template():
    # -> message enthält Filename
    message = request.files["template"]
    # -> fields ist ein Array aus den Feldern mit fieldNames und descriptions in JSON
    fields_data = request.form["fields"]
    # -> JSON to py
    fields = json.loads(fields_data)
    # -> Generieren einer UUID für die finale Datei
    template_id = str(uuid.uuid4())
    template_path = os.path.join(
        app.config["TEMPLATES_FOLDER"], secure_filename(template_id + ".html")
    )
    # -> Zusätzlich generieren einer separaten UUID für eine tmp file
    tmp_path = os.path.join(
        app.config["TEMPLATES_FOLDER"], str(uuid.uuid4())
    )
    #-> Zuerst nur die tmp file speichern
    message.save(tmp_path)

    # Prevent any injections
    # -> Suche im tmp template nach allen tags {{XXX}} wobei XXX nur aus buchstaben oder einem Leerzeichen bestehen darf
    # -> Sonst beende die Ausführung
    jinja_objects = re.findall(r"{{(.*?)}}", open(tmp_path).read())
    for obj in jinja_objects:
        if not re.match(r"^[a-z ]+$", obj):
            # An oopsie whoopsie happened
            return Response(
                f"Upload failed for {tmp_path}. Injection detected.", status=400
            )

    # If file is injection-free, save it
    # -> Überschreibe
    os.rename(tmp_path, template_path)
    # -> Öffne schreibend
    with open(
        os.path.join(app.config["TEMPLATES_FOLDER"], f"{template_id}_form.html"), "w"
    ) as f:
        # -> Render template auf form_template -> d.h. führe rendern mit JSON fields aus -> wird als HTML ausgeworfen
        # -> anschließend Speichere in der neuen template UUID datei
        f.write(
            render_template(
                "form_template.html", fields=fields, template_id=template_id
            )
        )
    # -> Redirect to next function with according URL
    return redirect(url_for("render_form", template_id=template_id))

@app.route("/form/<template_id>", methods=["GET", "POST"])
def render_form(template_id):
    # On render
    if request.method == "POST":
        # -> Keine möglichkeit auf die tmp zuzugreifen da +html hinzugefügt wird
        # Render the Jinja template with the provided data
        template = secure_filename(template_id + ".html")
        # Prevent hackers
        # -> Sonst könnte man auf globals von jinja im selbsterstelltem template zugreifen
        app.jinja_env.globals = {}
        # Set the parameters as globals
        # -> request kommt aus flask und enthält die inputs aus form_template.html
        for var_name, var_value in request.form.items():
            app.jinja_env.globals[var_name] = var_value
        # Render the template
        return render_template(template)
    # User just wants to GET
    # -> hier die bereits ausgefüllte form
    return render_template(f"{template_id}_form.html", template_id=template_id)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
