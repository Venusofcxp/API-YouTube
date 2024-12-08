import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Chave da API do YouTube
YOUTUBE_API_KEY = 'AIzaSyDNwFRkXyHf2sTabX0XV9wDr1vxeV5FoVw'

# Função para buscar o trailer no YouTube
def get_trailer_id(movie_title):
    search_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={movie_title} trailer&type=video&key={YOUTUBE_API_KEY}'
    response = requests.get(search_url)
    
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            video_id = data['items'][0]['id']['videoId']
            return video_id
    return None

@app.route('/YouTube/get_trailer', methods=['GET'])
def get_trailer():
    # Recebe o título do filme da URL
    movie_title = request.args.get('title', None)
    
    if not movie_title:
        return jsonify({'error': 'Title is required'}), 400
    
    trailer_id = get_trailer_id(movie_title)
    
    if trailer_id:
        return jsonify({'trailer_id': trailer_id})
    else:
        return jsonify({'error': 'Trailer not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
