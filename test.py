import json
import os
import re
import uuid

app_config = "/app/templates/"

message = "test.html"
#fields_data = request.form["fields"]
#fields = json.loads(fields_data)

template_id = str(uuid.uuid4())
template_path = os.path.join(
    app_config, template_id + ".html"
        #app_config["TEMPLATES_FOLDER"], secure_filename(template_id + ".html")
)
tmp_path = os.path.join(
    app_config, str(uuid.uuid4())
)
print("Tmp:"+str(tmp_path))
print("Template:"+str(template_path))

template_txt = "huhu\nblabla"


#    message.save(tmp_path)
#
#    # Prevent any injections
jinja_objects = re.findall(r"{{(.*?)}}", template_txt)
for obj in jinja_objects:
    if not re.match(r"^[a-z ]+$", obj):
#            # An oopsie whoopsie happened
#            return Response(
#                f"Upload failed for {tmp_path}. Injection detected.", status=400
        print(f"Upload failed for {tmp_path}. Injection detected.", status=400)
#            )

#    # If file is injection-free, save it
#    os.rename(tmp_path, template_path)
#    with open(
#        os.path.join(app.config["TEMPLATES_FOLDER"], f"{template_id}_form.html"), "w"
#    ) as f:
#        f.write(
#            render_template(
#                "form_template.html", fields=fields, template_id=template_id
#            )
#        )

#    return redirect(url_for("render_form", template_id=template_id))
