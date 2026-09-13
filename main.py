from flask import Flask, render_template,request
import requests
import smtplib

mail = "testuserbob28@gmail.com"
password = "senx stbb ryos vjnd"


API_URL = "https://api.npoint.io/9f6792b036a57c233116"
app = Flask(__name__)

@app.route('/')
def get_all_posts():
    all_posts = requests.get(API_URL)
    response = all_posts.json()
    print(response)
    return render_template("index.html", posts=response)

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
    all_posts = requests.get(API_URL)
    response = all_posts.json()
    blog = response[id-1]
    return render_template("post.html",blog=blog)

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