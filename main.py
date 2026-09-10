from flask import Flask, render_template
import requests
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

@app.route('/contact')
def contact_page():
    return render_template("contact.html")

@app.route('/post/<int:id>')
def post_page(id):
    all_posts = requests.get(API_URL)
    response = all_posts.json()
    blog = response[id-1]
    return render_template("post.html",blog=blog)




if __name__ == "__main__":
    app.run(debug=True)