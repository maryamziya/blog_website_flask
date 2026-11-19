from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_ckeditor import CKEditor, CKEditorField
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import Mapped, mapped_column
from flask_bootstrap import Bootstrap5
from sqlalchemy import Integer, String
import requests
import smtplib

from wtforms.fields.simple import StringField,SubmitField
from wtforms.validators import DataRequired


class Form(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    img_url = StringField('Image url', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    body = CKEditorField('Body')
    submit = SubmitField('Submit')


mail = "testuserbob28@gmail.com"
password = "senx stbb ryos vjnd"


API_URL = "https://api.npoint.io/9f6792b036a57c233116"
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config['SECRET_KEY'] = 'hi'
Bootstrap5(app)
db = SQLAlchemy(app)
ckeditor = CKEditor(app)



class Blog(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(String(100000), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)

    def __repr__(self):
        return f'Blog :{self.title}'


with app.app_context():
    db.create_all()

@app.route('/')
def get_all_posts():
    all_posts = Blog.query.all()
    print(all_posts)
    return render_template("index.html", posts=all_posts)

@app.route('/about')
def abt_page():
    return render_template("about.html")

@app.route('/contact' , methods=["GET","POST"])
def contact_page():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        print(name,message,email,phone)
        # Properly formatted email with headers
        email_message = (
            f"Subject: New Contact Form Submission\n\n"
            # f"To: maryamkumble@gmail.com\n"
            # f"Reply-To: {email}\n\n"  # Double newline separates headers from body
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Message:{message}"
        )
        with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
            connection.starttls()
            connection.login(user=mail, password=password)
            connection.sendmail(
                from_addr=mail,to_addrs="maryamkumble@gmail.com",
                msg=email_message
            )
        return render_template("contact.html", title="Successfully sent your message")

    else:
        return render_template("contact.html",title="Contact me")


@app.route('/post/<int:id>')
def post_page(id):
    post = db.get_or_404(Blog,id)
    return render_template("post.html",blog=post)

@app.route('/new_post',methods=['GET','POST'])
def create_new_post():
    form = Form()
    if form.validate_on_submit():
        title = form.title.data
        name = form.name.data
        img_url = form.img_url.data
        subtitle = form.subtitle.data
        body = form.body.data
        date = datetime.now().strftime("%B %d, %Y")
        blog = Blog(title=title,name=name,img_url=img_url,subtitle=subtitle,body=body,date=date)
        db.session.add(blog)
        db.session.commit()

    return render_template("new_post.html",form=form)
    


# @app.route('/form-entry' , methods=["POST"])
# def receive_data():
#     if request.method == "POST":
#         name = request.form["name"]
#         email = request.form["email"]
#         phone = request.form["phone"]
#         message = request.form["message"]
#         print(name,message,email,phone)
#
#     else:
#         print("get")



if __name__ == "__main__":
    app.run(debug=True)

