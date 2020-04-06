from flask import Flask,jsonify,request
from flask_restful import Api,Resource

app=Flask(__name__)
api=Api(app)

client= MongoClient("mongodb://db:27017")
db= client.SimilarityDB
users= db["Users"]

def UserExist(username):
	if users.find({"Username":username}).count()==0:
		return False
	else:
	    return True



class Register(Resource):
	def post(self):
		postedData =request.get_json()
		username= postedData["username"]
		password= postedData["password"]

		if UserExist(Username):
			retJson ={
			    "status": 301,
			    "msg": "invalid username"
			}
			return jsonify(retJson)

		hashed_pw= bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())	

		users.insert({
			"Username":username,
			"Password": hashed_pw,
			"Tokens": 6 
		})
        
        retJson={
            "status":200,
            "msg": "You have successfully signed up to the api"
        }
        return jsonify(retJson)



class Detect(Resource):
	def post(self):
		postedData= request.get_json()
		username= postedData["username"]
		password= postedData["password"]
		text1= postedData["text1"]
		text2= postedData["text2"]

		if not UserExist(username):
			retJson{
			    "status": "301"
			    "msg": "username not found"
			}



if __name__=='__main__':
	app.run('debug='True')