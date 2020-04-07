from flask import Flask,jsonify,request
from flask_restful import Api,Resource
import en_core_web_sm


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

def verifyPw(username,password):
	if not UserExist(username):
		return False

    hashed_pw= users.find({
         "Username":username

    	})[0]["Password"]
    if bcrypt.hashpw(password.encode('utf8'),hashed_pw)==hashed_pw:
    	return True
    else:
    	return False

def countTokens(username):
    tokens= users.find({
        "Username": username
    	})[0]["Tokens"]
        return tokens 

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

        correct_pw= verifyPw(username,password)

        if not correct_pw:
        	retJson{
        	    "status": "302",
        	    "msg": "Invalid Password"

        	}
        num_tokens =countTokens(username)

        if num_tokens<=0:
        	retJson{
        	    "status":303,
        	    "msg": "you have used all your tokens"

        	}
        	return jsonify(retJson)



        nlp = en_core_web_sm.load()
        text1= nlp(text1)
        text2= nlp(text2)

        ratio= text1.similarity(text2)
        retJson{
            "status": 302,
            "ratio" : ratio,
            "msg": "ratio found successfully"

        }

        currentTokens= countTokens(username)
        users.update({
        	"Username": username,
        },{
            "$set":{
                "Tokens":currentTokens-1
            }



        	})

        return jsonify(retJson)

class postedData(self):
	def post(self):
		postedData=request.get_json()
		username= postedData["username"]
		password=postedData["password"]
		refill= postedData["refill"]

		if not UserExist(username):
			retJson={
                "status": 301,
                "msg": "user not found "


			}
			return jsonify(retJson)
			


if __name__=='__main__':
	app.run('debug='True')