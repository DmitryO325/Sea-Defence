from flask import jsonify
from flask_restful import Resource, abort

from .reviews import Review
from data import db_session
from data.parser import review_parser
from data.users import User


def abort_if_reviews_not_found(review_id):
    session = db_session.create_session()
    news = session.query(Review).get(review_id)

    if not news:
        abort(404, message=f"Review {review_id} not found")


class ReviewsResource(Resource):
    def get(self, review_id):
        abort_if_reviews_not_found(review_id)
        session = db_session.create_session()
        reviews = session.query(Review).get(review_id)

        return jsonify({'news': reviews.to_dict(
            only=('id', 'user_id', 'topic', 'text', 'send_date'))})

    def delete(self, review_id):
        abort_if_reviews_not_found(review_id)
        session = db_session.create_session()
        reviews = session.query(Review).get(review_id)
        session.delete(reviews)
        session.commit()

        return jsonify({'success': 'OK'})


class ReviewsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        reviews = db_sess.query(Review).all()

        return jsonify({'reviews': [item.to_dict(only=('id', 'user_id', 'topic', 'text', 'send_date'))
                                    for item in reviews]})

    def post(self):
        args = review_parser.parse_args()
        db_sess = db_session.create_session()

        review = Review()
        review.user_id = args['user_id']
        review.topic = args['topic']
        review.text = args['text']
        review.send_date = args['send_date']

        db_sess.add(review)
        db_sess.commit()

        return jsonify({'result': 'success'})


class UserReviewsResource(Resource):
    def get(self, user_name):
        user_id = None

        db_sess = db_session.create_session()
        for user in db_sess.query(User):
            if User.surname + ' ' + User.name == user_name:
                user_id = user.id
                break
        if user_id:
            reviews = db_sess.query(Review).get({'user_id': user_id})
            return jsonify({'reviews': [item.to_dict(only=('id', 'topic', 'text', 'user_id', 'send_date'))
                                        for item in reviews]})

# Этот весь код помечен как Димин, по факту это Юрин код с моими небольшими изменениями
