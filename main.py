from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

#Initialization
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#Each row represents one video
class VideoModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  views = db.Column(db.Integer, nullable=False)
  likes = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return f"Video(name = {name}, views = {views}, likes = {likes})"

#Required arguments searched for in put request
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video is required", required=True)

#Optional arguments searched for in patch request
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

#Format data from database so it can be returned appropriately
resource_fields = {
  'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

class Video(Resource):
  
  #If video found by ID return, otherwise abort
  @marshal_with(resource_fields)
  def get(self, video_id):
    result = VideoModel.query.filter_by(id=video_id).first()
    if not result:
      abort(404, message="Not found with ID")
    return result

  #If ID not in use then add video with given information
  @marshal_with(resource_fields)
  def put(self, video_id):
    args = video_put_args.parse_args()
    result = VideoModel.query.filter_by(id=video_id).first()
    if result:
      abort(409, message="ID already in use")
    video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
    db.session.add(video)
    db.session.commit()
    return video, 201

  #If video found then check which argument is provided and update accordingly
  @marshal_with(resource_fields)
  def patch(self, video_id):
    args = video_update_args.parse_args()
    result = VideoModel.query.filter_by(id=video_id).first()
    if not result:
      abort(404, message="Video does not exist")

    if args['name']:
      result.name = args['name']
    if args['views']:
      result.views = args['views']
    if args['likes']:
      result.likes = args['likes']

    db.session.commit()
    return result

  #If video exists delete, otherwise abort
  def delete(self, video_id):
    result = VideoModel.query.filter_by(id=video_id).first()
    if not result:
      abort(404, message="Not found with ID")
    db.session.delete(result)
    db.session.commit()
    return '', 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
	app.run(debug=True)