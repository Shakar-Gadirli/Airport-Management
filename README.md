# Airport Management 

This is a the client-server based "Airport Management" Flask RESTful API that has two roles.

  - Client - user that has access to get the data.
  - Admin - user that has access to get, post, update and delete flight data.



Client should log in with *username* and *password* to gain admin privileges. Default Admin accounts are created by fetching credentials from json file and adding them to the database.

#### Admin
Admin can make 4 HTTP requests: GET, POST, PUT, DELETE and additionally, log in and end current admin session.
###### GET
Admin can make 2 GET requests  **http://127.0.0.1:5000/flights/from_city/to_city**  and **http://127.0.0.1:5000/flights** to get specific and all flights, respectively.
###### POST, PUT, DELETE
Admin can make requests like **http://127.0.0.1:5000/flights** to add, update and delete flights.
###### END SESSION
Admin can make DELETE request like  **http://127.0.0.1:5000/flights/end_session** to end current admin session.
###### LOG IN
Admin can make POST request like **http://127.0.0.1:5000/authentication_authorization** to log in.

#### Client
 Client can only make GET request like **http://127.0.0.1:5000/flights/from_city/to_city**  to see specific flights.

#### Installation
Clone this reposiory into your directory.
``` bash
git clone https://github.com/Shakar-Gadirli/Airport-Management.git
```

Install requirements using following command.
``` bash
pip3 install -r requirements.txt
```

#### Usage
Open two terminals to use this app. (One for server and another for client)
Run server.
```bash
python3 server.py
```
![server][images/server.jpg]

Client can be run in two modes: admin or client.

**As client:**
```bash
python3 client.py client
```
![client][images/client.jpg]

**As admin:**
```bash
python3 client.py admin
```

![admin][images/admin_start.jpg]

Admin processes examples.

**GET**
![admin][images/admin_get.png]

**POST**
![admim][images/admin_post.png]

**PUT**
![admin][images/admin_put.png]

**DELETE**
![admin][images/admin_delete.png]

**END SESSION**
![admin][images/admin_end.png]
