import requests
import argparse, json, sys
from colorama import init, Fore, Back, Style
init()

HEADER = "http://127.0.0.1:5000"



#------------------- Admin -------------------------------

def post_data(token,from_c,to,dep_t,arr_t,airplane,pass_num):
    resp = requests.post(HEADER + f"/flights",{"token":token,"from_city":from_c,"to_city":to,"departure_time":dep_t,"arrival_time":arr_t,"airplane":airplane,"passenger_num":pass_num})

def delete_data(id,token):
    resp = requests.delete(HEADER + f"/flights", data={'id': id,'token': token})

def put_data(id,from_c,to,dep_t,arr_t,airplane,pass_num,token):
    resp =requests.put(HEADER + f"/flights",{"id":id,"from_city":from_c,"to_city":to,"departure_time":dep_t,"arrival_time":arr_t,"airplane":airplane,"passenger_num":pass_num,"token":token})

def end_session(token):
    resp = requests.delete(HEADER + f"/end_session",data={'token':token})

def get_all():
    resp = requests.get(HEADER + f'/all_flights')
    resp_txt = resp.text
    f_dict = json.loads(resp_txt)
    ls=""
    for f in f_dict:
        ls += f"Id:{f['id']},From: {f['from_city']}, To: {f['to_city']},Departure:{f['departure_time']},Arrival:{f['arrival_time']},Airplane:{f['airplane']},Passengers:{f['passenger_num']}\n"
    return ls


def authorize(username,password):
    resp = requests.post(HEADER + f"/authentication_authorization", {'username': username, 'password': password})
    return resp.json()




#---------------- Client --------------------------------

def get_flight(from_city,to_city):
    resp = requests.get(HEADER+f"/flights/{from_city}/{to_city}")
    resp_txt = resp.text
    f_dict = json.loads(resp_txt)
    ls = ""
    for f in f_dict:
        ls += f"From: {f['from_city']}, To: {f['to_city']},Departure:{f['departure_time']},Arrival:{f['arrival_time']},Airplane:{f['airplane']},Passengers:{f['passenger_num']}\n"
    return ls



def main():

    while True:
        parser = argparse.ArgumentParser(description = "Airport Management")
        parser.add_argument("role",type=str,help="client or admin")
        args = parser.parse_args()
        if args.role == "client":
            print(Fore.GREEN+Style.BRIGHT+"Add source and destination cities:")
            from_city = input("Source: ")
            to_city = input("Destination: ")
            res = get_flight(from_city,to_city)
            print("")
            if(res):
                print(Fore.WHITE+res)
            else:
                print(Fore.RED+Style.BRIGHT+"There is not such a flight\n")


        elif args.role == "admin":
            print("")
            print(Fore.CYAN+Style.BRIGHT+"username")
            username = input()
            print(Fore.CYAN+Style.BRIGHT+"password")
            password=input()
            t = authorize(username,password)
            token = t['token']
            if(token):
                print("\n")
                print(Fore.GREEN+"All flights:")
                print(Fore.WHITE+get_all())
        
                while True:
                    func = input("\nEnter method (get,post,put,delete,end): ")

                    if func == "post":
                        from_city = input("Enter source city: ")
                        to_city = input("Enter destination city: ")
                        departure_time = input("Enter departure time (DD.MM.YYYY HH:MM): ")
                        arrival_time = input("Enter arrival time (DD.MM.YYYY HH:MM): ")
                        airplane = input("Enter airplane name: ")
                        passenger_num = input("Enter number of passengers: ")

                        post_data(token,from_city,to_city,departure_time,arrival_time,airplane,passenger_num)

                    elif func == "get":
                        print("0 or 1 [0-get all flights, 1 get specific flights]")
                        op = int(input())
                        print("")
                        if(op == 0):
                            print(get_all())
                        else:
                            print(Fore.GREEN+Style.BRIGHT+"Add source and destination cities:")
                            from_city = input("Source: ")
                            to_city = input("Destination: ")
                            res = get_flight(from_city,to_city)
                            print("")
                            if(res):
                                print(Fore.WHITE+res)
                            else:
                                print(Fore.RED+Style.BRIGHT+"There is not such a flight\n")

                    elif func == "delete":
                        print(get_all())
                        print("")
                        id = input("Enter id of flight: ")
                        delete_data(id,token)
                    
                    elif func == "put":
                        id = input("Enter id of the flight: ")
                        new_from_city = input("Enter new source city: ")
                        new_to_city = input("Enter new destination city: ")
                        new_departure_time = input("Enter new departure time (DD.MM.YYYY HH:MM): ")
                        new_arrival_time = input("Enter new arrival time (DD.MM.YYYY HH:MM): ")
                        new_airplane = input("Enter new airplane name: ")
                        new_passenger_num = input("Enter new number of passengers: ")

                        put_data(id,new_from_city,new_to_city,new_departure_time,new_arrival_time,new_airplane,new_passenger_num,token)

                    elif func == "end":
                        print(Fore.BLUE+"Session ending...")
                        end_session(token)
                        break
            else: 
                print(Fore.RED+Style.BRIGHT+"Could not logged in")

if __name__ == "__main__":
    main()


