from flask import Flask, request, redirect, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

app = Flask(__name__)

# 1. Chave Secreta: OBRIGATÓRIO para usar sessões no Flask.
# Em produção, isso seria uma senha forte. Para o protótipo, geramos uma aleatória.
app.secret_key = "25b938fda8d54cb9ad82d2fc10d3497d"

CLIENT_ID = '88a3a41c9e1a447c9162b9722437b3e7'
CLIENT_SECRET = '25b938fda8d54cb9ad82d2fc10d3497d'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

# 2. Transformamos a configuração em uma função
# Isso garante que cada usuário ganhe uma instância "limpa" de autenticação
def criar_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-top-read",
        # Essa linha mágica diz ao Spotipy para NÃO criar o arquivo .cache
        cache_handler=spotipy.cache_handler.FlaskSessionCacheHandler(session)
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

    # O FlaskSessionCacheHandler cuida de salvar o token na sessão do usuário automaticamente
    sp_oauth.get_access_token(codigo)
    
    # Redireciona o usuário para a tela final
    return redirect('/artistas')

@app.route('/artistas')
def artistas():
    sp_oauth = criar_spotify_oauth()
    
    # Verifica se o usuário tem um token válido na sessão dele
    if not sp_oauth.validate_token(sp_oauth.cache_handler.get_cached_token()):
        # Se não tiver (ou tiver expirado), manda de volta pra tela de login
        return redirect('/')
    
    # Se passou, conectamos no Spotify!
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    
    resultados = sp.current_user_top_artists(limit=10, time_range='medium_term')
    
    artistas_html = []
    for item in resultados['items']:
        nome = item['name']
        generos = ", ".join(item.get('genres', []))
        artistas_html.append(f"<li><b>{nome}</b> (Gêneros: {generos})</li>")
    
    html = f"<h1>Artistas mais ouvidos do usuário logado:</h1><ul>{''.join(artistas_html)}</ul><br><a href='/logout'>[ Sair / Trocar de Conta ]</a>"
    
    return html
@app.route('/logout')
def logout():
    # Limpa todos os dados da sessão do usuário atual
    session.clear()
    # Manda ele de volta para a tela inicial
    return redirect('/')

if __name__ == '__main__':
    app.run(port=5000, debug=True)