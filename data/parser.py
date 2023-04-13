from flask_restful import reqparse

review_parser = reqparse.RequestParser()
review_parser.add_argument('content', required=True)
review_parser.add_argument('send_date', required=True, type=str)
review_parser.add_argument('user_id', required=True, type=int)


