"""
pip install flask
pip install flask_sqlalchemy
"""

from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

#Configuring app and creating sqlite db (ORM type DB --> Object Relational Mapper)
app = Flask("server_drink")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#Creating schemas of required tables , This is a Drink table schema
class Drink(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} -- {self.description}"

#   --->COMMENT BELOW LINES (SECOND TIME) / UNCOMMENT BELOW LINES (FIRST TIME), WHEN YOU DELETE THE data.db file
#   --->When we start a Flask server, the code gets executed multiple times, so need to delete during the second time of execution
#db.create_all()      #Creates data.db
#create_def_drinks()  #Creates default drinks

#Create few default rows
def create_def_drinks():
    id1=create_a_drink("KingFisher", "A good Beer")
    id2=create_a_drink("RoyalStag", "A good Whisky")
    id3=create_a_drink("McDowells", "A good Rum")

#   ---->HELPER Functions
#create a drink and commit
def create_a_drink(p_name,p_desc):
    v_drink = Drink(name=p_name,description=p_desc)
    db.session.add(v_drink)
    db.session.commit()
    return v_drink.id

#Drink.query.all() return a sequence of all rows as objects ,which can be viewed like a key-value pair, but they are not really dictionary
def select_all_drinks():
    list_of_drinks =[]
    Drinks = Drink.query.all()
    for drink in Drinks:
        drink_dict ={"name":drink.name ,"description":drink.description}
        list_of_drinks.append(drink_dict)
        
    return list_of_drinks 

#Drink.query.get_or_404(id) return a matching row object ,which can be viewed like a key-value pair, but they are not really dictionary
def select_a_drink_with_id(p_drink_id,r_obj=False):
    v_drink = Drink.query.get_or_404(p_drink_id)
    if r_obj:
        return v_drink
    
    drink_dict ={"name":v_drink.name ,"description":v_drink.description}
    return drink_dict

#db.session.delete(x) deletes the 'x' object and commit
def delete_a_drink_with_id(p_drink_id):
    v_drink = select_a_drink_with_id(p_drink_id,True)
    db.session.delete(v_drink)
    db.session.commit()


#   ---> URL redirections
@app.route('/',methods=['GET'])
def index():
    #http://127.0.0.1:5000/
    return "Welcome to Drinks Page!!"

@app.route('/drinks/',methods=['GET'])
def get_drinks():
    #http://127.0.0.1:5000/drinks
    v_drinks=select_all_drinks()
    return jsonify( {'Available Drinks':v_drinks} )

@app.route('/drinks/<int:drink_id>',methods=['GET'])
def get_drink(drink_id):
    #http://127.0.0.1:5000/drinks/2
    v_drinks=select_a_drink_with_id(drink_id)
    return jsonify( v_drinks )

@app.route('/drinks/add',methods=['POST'])
def add_drink():
    #curl -i -H "Content-Type: Application/json" -X POST -d "{\"name\":\"SmirnOff\" ,\"description\":\"A Good Vodka\"}" http://127.0.0.1:5000/drinks/add
    v_response = request.json
    v_id=create_a_drink(v_response['name'], v_response['description'])
    return jsonify( {"Drink added with id":v_id} )

@app.route('/drinks/delete',methods=['DELETE'])
def delete_drink():
    #curl -i -H "Content-Type: Application/json" -X DELETE -d "{\"id\":4}" http://127.0.0.1:5000/drinks/delete
    v_response = request.json
    delete_a_drink_with_id(v_response['id'])
    return jsonify( {"Drink deleted with id":v_response['id']} )


#   --->Main Method
if __name__=='__main__':
    app.run(host="127.0.0.1", port=5000, threaded=True,debug=True)


