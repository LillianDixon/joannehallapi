from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku
from flask_mail import Mail, Message
import config
# import os

app = Flask(__name__)
CORS(app)

# app.config["DATABASE_URI"] = os.environ.get('DATABASE_URI')
# app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_DATABASE_URI"] = ''


app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
    MAIL_USERNAME = config.MAIL_USERNAME,
    MAIL_PASSWORD = config.MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER = 'myemail@testemail.com'
)

heroku = Heroku(app)
db = SQLAlchemy(app)
mail = Mail(app)



@app.route("/email", methods=['POST'])
def index():
    if request.content_type == 'application/json':
        get_data = request.get_json()
        name = get_data.get('name')
        sender = get_data.get('email')
        # recipients = [os.environ.get('MAIL_USERNAME')]
        recipients = [config.MAIL_USERNAME]
        headers = [name, sender] + recipients
        subject = get_data.get('subject')
        message = get_data.get('message')
        body = message + "\n\n" + name
        msg = Message(subject, headers, body)
        print(Message)
        mail.send(msg)
    return jsonify('Message has been sent')


@app.route('/login', methods=['POST'])
def login():
    if request.content_type == "application/json":
        post_data = request.get_json()
        email = post_data.get("email")
        password = post_data.get("password")
        
        if password == config.LOGIN_PASSWORD and email == config.LOGIN_EMAIL:
        # if password == os.environ.get("LOGIN_PASSWORD") and email == os.environ.get('LOGIN_EMAIL'):
            Credentials = True
            return jsonify('logged in')
    return jsonify('Wrong Credentials')


class Artwork(db.Model):
    __tablename__ = 'Artwork'
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(120))
    description = db.Column(db.String)
    img_url = db.Column(db.String)
    category = db.Column(db.String)

    def __init__(self, title, description, img_url, category):
        self.title = title
        self.description = description
        self.img_url = img_url
        self.category = category

    def __repr__(self):
        return "<Title %r>" % self.title

    
@app.route("/")
def home():
    return "<h1>Hi from Flask</h1>"

@app.route("/input", methods=["POST"])
def input():
    if request.content_type == "application/json":
        post_data = request.get_json()
        title = post_data.get("title")
        description = post_data.get("description")
        img_url = post_data.get("img_url") 
        category = post_data.get('category')
        reg = Artwork(title, description, img_url,category)
        db.session.add(reg)
        db.session.commit()
        return jsonify("Data Posted")
    return jsonify("Something went wrong")

@app.route("/get-artwork", methods=["GET"])
def return_artwork():
    all_art = db.session.query(Artwork.id, Artwork.title, Artwork.description, Artwork.img_url, Artwork.category).all()
    print(all_current)
    return jsonify(all_art)

@app.route("/get-artwork/<id>", methods=['GET'])
def return_single_artwork(id):
    one_art = db.session.query(Artwork.id, Artwork.title, Artwork.description, Artwork.img_url, Artwork.category). filter(Artwork.id == id).first()
    return jsonify(one_art)

@app.route("/delete_artwork/<id>", methods=["DELETE"])
def artwork_delete(id):
    if request.content_type == "application/json":
        record = db.session.query(Artwork).get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify("completed Delete action")
    return jsonify("Delete failed")

@app.route("/update_artwork/<id>", methods=["PUT"])
def artwork_update(id):
    if request.content_type == 'application/json':
        put_data = request.get_json()
        title = put_data.get("title")
        description = put_data.get("description")
        img_url = put_data.get("img_url")
        category = put_data.get('category')
        record = db.session.query(Artwork).get(id)
        record.title = title
        record.description = description
        record.img_url = img_url
        record.category = category
        db.session.commit()
        return jsonify("Completed Update")
    return jsonify("Failed Update")

if __name__ == "__main__":
    app.debug = True
    app.run()