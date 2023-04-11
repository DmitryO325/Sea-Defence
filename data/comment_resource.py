from flask import jsonify
from flask_restful import Resource, abort

from .comments import Comment
from data import db_session
from data.parser import comment_parser
from data.users import User


def abort_if_comments_not_found(comment_id):
    session = db_session.create_session()
    news = session.query(Comment).get(comment_id)
    if not news:
        abort(404, message=f"Comment {comment_id} not found")


class CommentsResource(Resource):
    def get(self, comment_id):
        abort_if_comments_not_found(comment_id)
        session = db_session.create_session()
        comments = session.query(Comment).get(comment_id)
        return jsonify({'news': comments.to_dict(
            only=('id', 'content', 'user_id', 'send_date'))})

    def delete(self, comment_id):
        abort_if_comments_not_found(comment_id)
        session = db_session.create_session()
        comments = session.query(Comment).get(comment_id)
        session.delete(comments)
        session.commit()
        return jsonify({'success': 'OK'})


class CommentsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        comments = db_sess.query(Comment).all()
        return jsonify({'comments': [item.to_dict(only=('id', 'content', 'user_id', 'send_date'))
                                     for item in comments]})

    def post(self):
        args = comment_parser.parse_args()
        db_sess = db_session.create_session()
        comment = Comment(content=args['content'], user_id=args['user_id'], send_date=args['send_date'])
        db_sess.add(comment)
        db_sess.commit()
        return jsonify({'result': 'success'})


class UserCommentsResource(Resource):
    def get(self, user_name):
        db_sess = db_session.create_session()
        for user in db_sess.query(User):
            if User.surname + ' ' + User.name == user_name:
                id = user.id
                break
        if id:
            comments = db_sess.query(Comment).get({'user_id': id})
            return jsonify({'comments': [item.to_dict(only=('id', 'content', 'user_id', 'send_date'))
                                         for item in comments]})

