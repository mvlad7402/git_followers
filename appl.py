from flask import Flask, request, json
from flask_restful import reqparse, abort, Api, Resource
import requests


def flw_search(url, cnt, uid='', passw=''):
	jsres = []
	curr_url= url
	d = 0
	m = 0
	mmax= 0;
	while d < cnt:
		mmax= len(jsres)
		while(True) :
			if d>0 and m < mmax :
				curr_url=jsres[m]['followers_url']
				m += 1
			if len(uid)>0 and len(passw) > 0:
				js = requests.get(curr_url, auth=(uid, passw)).json()
			else:
				js = requests.get(curr_url).json()
			if 'message' in js :
				return js
			k=0;
			while k < 5 and k < len(js) :
#				jsres.append({"login": js[k]['login'], "followers_url": js[k]['followers_url'], "follows": curr_url})
				jsres.append(js[k])
				k += 1
			if(mmax <= m or d==0): # do_while
				break
		d += 1
		jsd = json.dumps(jsres)
	return jsd


app = Flask(__name__, static_url_path='')
api = Api(app)

parser = reqparse.RequestParser()
		
class Gitflw(Resource):		
	def get(self,git_id):
		uid = request.authorization.username
		psw = request.authorization.password
		return flw_search('https://api.github.com/users/'+ git_id +'/followers', 3, uid, psw)


api.add_resource(Gitflw, '/gitflw/<git_id>')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/alive')
def present():
    return 'Alive!'

if __name__ == "__main__":
    app.run()



