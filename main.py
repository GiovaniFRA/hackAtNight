from flask import Flask, request, redirect, session, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

app = Flask(__name__)
app.secret_key = "chave_secreta_do_projeto_radar"

CLIENT_ID = '88a3a41c9e1a447c9162b9722437b3e7'
# ATENÇÃO: Cole o seu Client Secret real aqui!
CLIENT_SECRET = '25b938fda8d54cb9ad82d2fc10d3497d'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

def criar_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-top-read",
        cache_handler=spotipy.cache_handler.FlaskSessionCacheHandler(session),
        show_dialog=True
    )

@app.route('/')
def index():
    sp_oauth = criar_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = criar_spotify_oauth()
    codigo = request.args.get('code')
    
    if not codigo:
        return "Erro: Autorização negada.", 400

    sp_oauth.get_access_token(codigo)
    return redirect('/artistas')

@app.route('/artistas')
def artistas():
    sp_oauth = criar_spotify_oauth()
    
    if not sp_oauth.validate_token(sp_oauth.cache_handler.get_cached_token()):
        return redirect('/')
    
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    resultados = sp.current_user_top_artists(limit=6, time_range='medium_term')
    
    return render_template('dashboard.html', artistas=resultados['items'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=5000, debug=True)