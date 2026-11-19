from flask import request
from flask_restful import Resource, Api, fields, marshal_with, abort, reqparse, inputs
from main import app
from db import db,Blog

api = Api(app)

blog_args = reqparse.RequestParser()
blog_args.add_argument('id', type=int, required=True, help="Name cannot be blank")
blog_args.add_argument('title', type=str, required=True, help="Name cannot be blank")
blog_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
blog_args.add_argument('img_url', type=str, required=True, help="Name cannot be blank")
blog_args.add_argument('subtitle', type=str, required=True, help="Name cannot be blank")
blog_args.add_argument('body', type=str, required=True, help="Name cannot be blank")
blog_args.add_argument('date', type=str, required=True, help="Name cannot be blank")

blog_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'name': fields.String,
    'img_url': fields.String,
    'subtitle': fields.String,
    'body': fields.String,
    'date': fields.Boolean,
}

class Blogs(Resource):
    @marshal_with(blog_fields)
    def get(self):
        all_blogs = Blog.query.all()
        return all_blogs

    @marshal_with(blog_fields)
    def post(self):
        args = blog_args.parse_args()
        new_blog = Blog(
            title=args['title'],
            name=args['name'],
            img_url=args['img_url'],
            subtitle=args['subtitle'],
            body=args['body'],
            date=args['date'],
        )
        db.session.add(new_blog)
        db.session.commit()
        return new_blog, 201
    
class SingleBlog(Resource):
    @marshal_with(blog_fields)
    def get(self, blog_id):
        blog = db.get_or_404(Blog, blog_id)
        return blog

    @marshal_with(blog_fields)
    def put(self, blog_id):
        args = blog_args.parse_args()
        blog = db.get_or_404(Blog, blog_id)
        blog.title = args['title']
        blog.name = args['name']
        blog.img_url = args['img_url']
        blog.subtitle = args['subtitle']
        blog.body = args['body']
        blog.date = args['date']
        db.session.commit()
        return blog, 200

    def delete(self, blog_id):
        blog = db.get_or_404(Blog, blog_id)
        db.session.delete(blog)
        db.session.commit()
        return '', 204

api.add_resource(Blogs, '/api/blogs/')
api.add_resource(SingleBlog, '/api/blogs/<int:blog_id>/')

if __name__ == '__main__':
    app.run(debug=True)
        
