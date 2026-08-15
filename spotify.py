import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 1. Configuração das suas credenciais do painel
CLIENT_ID = '88a3a41c9e1a447c9162b9722437b3e7'
CLIENT_SECRET = '25b938fda8d54cb9ad82d2fc10d3497d'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

# 2. Autenticação
# O Spotipy vai abrir o seu navegador automaticamente para você fazer login
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-top-read" # Permissão para ler o que você mais escuta
))

print("Autenticação realizada com sucesso!\n")

# 3. Buscando os artistas que você mais escuta
print("Buscando seus artistas mais ouvidos...")
resultados = sp.current_user_top_artists(limit=10, time_range='medium_term')

# 4. Extraindo os dados para a sua lógica de negócio
for i, item in enumerate(resultados['items']):
    nome_artista = item['name']
    generos = item['genres']
    
    print(f"{i + 1}. {nome_artista}")
    print(f"   Gêneros: {', '.join(generos) if generos else 'Não definido'}\n")