from flask import Flask, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api=Api(app)

names={"saleh":{"age":23, "Major":"COE"},
       "adnan":{"age":23, "Major":"COE"}}



#TLs={"1":{"streets":{"1":{"amountOfTraffic":1}}}}

video_put_args=reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video")
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video")


TL_put_args=reqparse.RequestParser()
TL_get_args=reqparse.RequestParser()


TL_put_args.add_argument("delays", type=str, help="the delys for the traffic light")
TL_get_args.add_argument("TA", type=str, help="the traffic amount on each street")




videos={}

delays={1:[2,2,2,2],2:[4,4,4,4]}



class HelloWorld(Resource):
    def get(self, name):
        return names[name]


class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    def put(self, video_id):
        args=video_put_args.parse_args()

        ##videos[video_id]=args
        return videos[video_id], 201


class TLD(Resource):
    def get(self, TL_id):
        args=TL_get_args.parse_args()
        temp=args['TA'].split(',')
        new_delays=[]
        for i in range(len(temp)):
            new_delays.append(int(float(temp[i])*5))
        return new_delays

    def get_without_traffic(self, TL_id):
        return delays[TL_id]

    def put(self, TL_id):
        args=request.form.to_dict(flat=False)
        if not TL_id in delays:
            delays[TL_id]=[1,1,1,1]
        for i in range(len(args['delays'][0].split(','))):
            temp=args['delays'][0].split(',')
            delays[TL_id][i]=int(temp[i])
        return delays[TL_id], 201



api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Video,"/video/<int:video_id>")
api.add_resource(TLD, "/tld/<int:TL_id>")

if __name__=="__main__":
    app.run(debug=True)
