from flask_restful import reqparse

comment_parser = reqparse.RequestParser()
comment_parser.add_argument('content', required=True)
comment_parser.add_argument('send_date', required=True, type=str)
comment_parser.add_argument('user_id', required=True, type=int)


