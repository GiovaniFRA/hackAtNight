from flask import Flask, request, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

CLIENT_ID = '88a3a41c9e1a447c9162b9722437b3e7'
CLIENT_SECRET = '25b938fda8d54cb9ad82d2fc10d3497d'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

# 2. Configurando o Spotipy para trabalhar no modo Web
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-top-read"
)

# 3. Rota principal: O usuário entra no seu site e clica em "Logar"
@app.route('/')
def index():
    # Gera o link de login oficial do Spotify
    auth_url = sp_oauth.get_authorize_url()
    # Manda o usuário para a tela preta e verde do Spotify
    return redirect(auth_url)

# 4. A Rota de Callback: O Spotify devolve o usuário para cá
@app.route('/callback', methods=['GET'])
def callback():
    # O Spotify envia um código secreto na URL, o Flask captura aqui
    codigo = request.args.get('code')
    
    if not codigo:
        return "Erro: Autorização negada pelo usuário.", 400

    # Trocamos o código pelo token de acesso definitivo
    token_info = sp_oauth.get_access_token(codigo)
    
    # Agora o Spotipy está destravado e pronto para uso!
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Buscando os artistas
    resultados = sp.current_user_top_artists(limit=5, time_range='medium_term')
    
    # Formatando para mostrar no navegador
    artistas = []
    for item in resultados['items']:
        nome = item['name']
        generos = ", ".join(item['genres'])
        artistas.append(f"<li><b>{nome}</b> (Gêneros: {generos})</li>")
    
    html = f"<h1>Seus artistas mais ouvidos:</h1><ul>{''.join(artistas)}</ul>"
    
    return html

if __name__ == '__main__':
    # Inicia o servidor Flask na porta 5000
    app.run(port=5000, debug=True)