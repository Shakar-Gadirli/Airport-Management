from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
import json
import random


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_db.db"
db=SQLAlchemy(app)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sessions = {}



class Flight(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    from_city = db.Column(db.String(50),nullable=False)
    to_city = db.Column(db.String(50),nullable=False)
    departure_time = db.Column(db.String(50),nullable=False)
    arrival_time = db.Column(db.String(50),nullable=False)
    airplane = db.Column(db.String(50),nullable=False)
    passenger_num = db.Column(db.String(50),nullable=False)

    def __init__(self,from_city,to_city,departure_time,arrival_time,airplane,passenger_num):
        self.from_city = from_city
        self.to_city=to_city
        self.departure_time=departure_time
        self.arrival_time=arrival_time
        self.airplane=airplane
        self.passenger_num=passenger_num



class Admin(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(50),nullable=False)

    def __init__(self,username,password):
        self.username = username
        self.password = password


class EndSession(Resource):
    def delete(self):
        args = reqparse.RequestParser()
        args.add_argument("token",type=str,help="Token")
        args.parse_args()

        if(args.token in sessions.values()):
            for key, value in sessions.items():
                if value == args.token:
                    del sessions[key]
                    print("Session ended!")

class Authorize(Resource):
    def post(self):
        argss = reqparse.RequestParser()
        argss.add_argument("username",type=str,help="username")
        argss.add_argument("password",type=str,help="password")
        args = argss.parse_args()

        admin_check = Admin.query.filter_by(username=args.username,password=args.password).first()
        print(admin_check)
        token=""
        if admin_check:
            token = str(random.randint(50000, 5000000000))
            sessions[args.username] = token
        return {"token":token}
    
            


class AdminProcesses(Resource):
    def delete(self):
        argss = reqparse.RequestParser()
        argss.add_argument("id",type=str,help = "id of flight")
        argss.add_argument("token",type=str,help="Token")
        args = argss.parse_args()

        if(args.token in sessions.values()):
            del_flight = Flight.query.filter_by(id=args.id).first()
            db.session.delete(del_flight)
            db.session.commit()

        else:
            print("Invalid token")

    def post(self):
        argss = reqparse.RequestParser()
        argss.add_argument("token",type=str,help="Token")
        argss.add_argument("from_city",type=str,help = "from city")
        argss.add_argument("to_city",type=str,help = "to city")
        argss.add_argument("departure_time",type=str,help = "departure time")
        argss.add_argument("arrival_time",type=str,help = "arrival time")
        argss.add_argument("airplane",type=str,help = "airplane")
        argss.add_argument("passenger_num",type=str,help = "number of passengers")
        args = argss.parse_args()


        if(args.token in sessions.values()):
            new_flight = Flight(from_city=args.from_city,to_city=args.to_city,departure_time=args.departure_time,arrival_time=args.arrival_time,airplane=args.airplane,passenger_num=args.passenger_num)
            db.session.add(new_flight)
            db.session.commit()

        else:
            print("invalid token")

    def put(self):
        argss = reqparse.RequestParser()
        argss.add_argument("id",type=str,help="Id of flight")
        argss.add_argument("from_city",type=str,help = "from city")
        argss.add_argument("to_city",type=str,help = "to city")
        argss.add_argument("departure_time",type=str,help = "departure time")
        argss.add_argument("arrival_time",type=str,help = "arrival time")
        argss.add_argument("airplane",type=str,help = "airplane")
        argss.add_argument("passenger_num",type=str,help = "number of passsengers")
        argss.add_argument("token",type=str,help="Token")
        args = argss.parse_args()

        if(args.token in sessions.values()):
            flight_to_update = Flight.query.filter_by(id=args.id).first()
            flight_to_update.from_city = args.from_city
            flight_to_update.to_city = args.to_city
            flight_to_update.departure_time = args.departure_time
            flight_to_update.arrival_time = args.arrival_time
            flight_to_update.airplane = args.airplane
            flight_to_update.passenger_num = args.passenger_num
            db.session.commit()

        else:
            print("Invalid token")


class AllInfo(Resource):
    def get(self):
        flight_list = list()
        all_flights = Flight.query.all()
        for f in all_flights:
            one_flight = {"id":f.id,"from_city":f.from_city,"to_city":f.to_city,"departure_time":f.departure_time,"arrival_time":f.arrival_time,"airplane":f.airplane,"passenger_num":f.passenger_num}
            flight_list.append(one_flight)
        return flight_list



class Client(Resource):
    def get(self,from_city,to_city):
        specific_flights = []
        all_flights = AllInfo.get(self)
        for f in all_flights:
            if f["from_city"] == from_city and f["to_city"] == to_city:
                one_flight = {"from_city":f["from_city"],"to_city":f["to_city"],"departure_time":f["departure_time"],"arrival_time":f["arrival_time"],"airplane":f["airplane"],"passenger_num":f["passenger_num"]}
                specific_flights.append(one_flight)
        return specific_flights

def main():

    api.add_resource(AllInfo,"/all_flights")

    api.add_resource(Authorize,"/authentication_authorization")
    api.add_resource(EndSession,"/end_session")
    api.add_resource(AdminProcesses,"/flights")
    api.add_resource(Client,"/flights/<from_city>/<to_city>")


    
    db.create_all()
    flights_json = open("flights.json")
    flights = json.load(flights_json)
    

    for row in flights:
        new_flight = Flight(from_city=row['from_city'],to_city=row["to_city"],departure_time=row["departure_time"],arrival_time=row["arrival_time"],airplane=row["airplane"],passenger_num=row["passenger_num"])
        db.session.add(new_flight)
    
    
    
    
    admins_json = open("admins.json")
    admins = json.load(admins_json)

    for row in admins:
        new_admin = Admin(username=row["username"],password=row["password"])
        db.session.add(new_admin)
    
    
    db.session.commit()
    app.run()


if __name__ == "__main__":
    main()






