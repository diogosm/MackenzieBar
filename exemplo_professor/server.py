CLIENT_ID="671bd2e367064e5d852ff23bf4cd8456"
CLIENT_SECRET="98bf440c4a624e70a7d63e8180cfab5f"

import spotipy
#from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
#from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from flask import Flask
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import sys

username = "dsm"
scope = "user-modify-playback-state"
redirect_uri = "http://localhost:8888/callback/"
id = ""
firstTime = 1
app = Flask(__name__)
app.config['SECRET_KEY'] = 'batatinhaFrita123'
Bootstrap(app)

token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
sp = spotipy.Spotify(auth=token)

res = sp.devices()
#pprint(res)

class NameForm(FlaskForm):
    name = StringField('Spotify link. Exemplo: https://open.spotify.com/track/6wVWJl64yoTzU27EI8ep20?si=3b9b99c465bc4e6f', validators=[DataRequired()])
    submit = SubmitField('Submit')
	

@app.route('/', methods=['GET', 'POST'])
def index():
	global firstTime, id
	
	if firstTime:
		sp.start_playback(device_id=res['devices'][0]['id'])
		firstTime = 0
	
	form = NameForm()
	message = ""
	if form.validate_on_submit():
		name = form.name.data
		if validaURL(name):
			message = "Música adicionada na fila com sucesso!"
			id = 'spotify:track:' + id
			try:
				sp.add_to_queue(device_id=res['devices'][0]['id'], uri=id)
			except:
				message = "Erro ao processar serviço do spotify"
		else:
			message = "Link inválido."
	return render_template('index.html', form=form, message=message)
	

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

	
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
	
	
def validaURL(line):
	global id
	id = line.split('/')[-1].split('?')[0]
	
	if len(id) > 0:
		return True
	return False
	
	
if __name__ == "__main__" :
	app.run(host="0.0.0.0", debug=True, port=80)
