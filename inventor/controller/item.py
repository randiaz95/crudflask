from app1 import app, db
from app1.models.contacts import Contact
from flask import render_template, jsonify, request


@app.route("/")
def index():
    all_contacts = [c for c in Contact.query.all()]
    return render_template("index.html", data=all_contacts)


@app.route("/create", methods=["POST"])
def add():
    try:
        params = request.get_json()
        current = Contact(firstname=params.get("firstname", ""),
                          lastname=params.get("lastname", ""),
                          email=params.get("email", ""),
                          notes=params.get("notes", ""))

        return jsonify({"status": "success",
                        "message": "Created a contact",
                        "id": current.id,
                        "firstname": current.firstname,
                        "lastname": current.lastname,
                        "email": current.email,
                        "notes": current.notes,})

    except Exception as e:
        return jsonify({"status": "error",
                        "message": str(e)})


@app.route("/update")
def update():
    try:
        params = request.get_json()
        current = Contact.query.filter_by(id=params["id"])
        current.firstname = params.get("firstname", "")
        current.lastname = params.get("lastname", "")
        current.email = params.get("email", "")
        current.notes = params.get("notes", "")
        db.session.commit()
        return jsonify({"status": "success",
                        "message": "Updated a contact",
                        "id": current.id,
                        "firstname": current.firstname,
                        "lastname": current.lastname,
                        "email": current.email,
                        "notes": current.notes,})
    except Exception as e:
        return jsonify({"status": "error",
                        "message": str(e)})


@app.route("/delete")
def delete():
    try:
        params = request.get_json()
        Contact.query.filter_by(id=params.get("id", "")).delete()
        db.session.commit()
        return jsonify({"status": "success",
                        "message": "Deleted a contact"})
    except Exception as e:
        return jsonify({"status": "error",
                        "message": str(e)})
