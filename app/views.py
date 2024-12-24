from django.shortcuts import render
import requests
from datetime import datetime
import math
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
import json
import requests
from datetime import datetime
from django.shortcuts import render
from urllib.parse import quote_plus
def index(request):
    query = request.GET.get('search_query', '')  # Get search query from the URL
    search_results = []

    if query:
        # URL-encode the query to handle special characters
        encoded_query = quote_plus(query)

        # Make the API request to Jikan search endpoint
        response = requests.get(f'https://api.jikan.moe/v4/anime?q={encoded_query}&limit=10')  # You can adjust the limit
        print(f"Request URL: https://api.jikan.moe/v4/anime?q={encoded_query}&limit=10")
        if response.status_code == 200:
            search_results = response.json().get('data', [])

        else:
            print(f"Error fetching search results: {response.status_code}")
    def get_season():
        month = datetime.now().month
        if 4 <= month <= 6:
            return "spring"
        elif 7 <= month <= 9:
            return "summer"
        elif 10 <= month <= 12:
            return "fall"
        else:
            return "winter"

    current_year = datetime.now().year

    # Inisialisasi variabel dengan nilai default
    airing_now_data = {}
    top_anime_data = {}
    popular_anime_data = {}
    anime_recommendations = []

    # Fetch data anime airing sekarang
    response = requests.get(f'https://api.jikan.moe/v4/seasons/{current_year}/{get_season()}')
    if response.status_code == 200:
        airing_now_data = response.json()
    else:
        print(f"Error fetching airing now data: {response.status_code}")

    # Fetch data top anime
    response = requests.get('https://api.jikan.moe/v4/top/anime')
    if response.status_code == 200:
        top_anime_data = response.json()
    else:
        print(f"Error fetching top anime data: {response.status_code}")

    # Fetch data popular anime
    response = requests.get('https://api.jikan.moe/v4/top/anime?filter=bypopularity')
    if response.status_code == 200:
        popular_anime_data = response.json()
    else:
        print(f"Error fetching popular anime data: {response.status_code}")

    # Fetch data anime recommendations (misalnya, rekomendasi untuk anime dengan id tertentu)
    anime_id = 5114  # Contoh ID anime, ganti sesuai dengan ID anime yang relevan
    response = requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}/recommendations')
    if response.status_code == 200:
        anime_recommendations = response.json().get('data', [])
    else:
        print(f"Error fetching anime recommendations data: {response.status_code}")

    context = {
        'airing_now_data': airing_now_data.get('data', []),
        'top_anime_data': top_anime_data.get('data', []),
        'popular_anime_data': popular_anime_data.get('data', []),
        'anime_recommendations': anime_recommendations,
        'search_results': search_results
    }
    return render(request, 'index.html', context)

def getAnimeRecommendations(anime_id):
    try:
        response = requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}/recommendations')
        if response.status_code == 200:
            recommendations_data = response.json().get('data', [])
            return recommendations_data
        else:
            print(f"Error fetching recommendations: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return []




def index_two(request, anime_id):
    # Menggunakan Jikan API untuk mendapatkan data anime
    response = requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}')

    anime_data = {}  # Inisialisasi default anime_data sebagai dictionary kosong

    if response.status_code == 200:
        anime_data = response.json().get('data', {})
        recommendations_data = getAnimeRecommendations(anime_id)
        
        # Get the related anime data
    else:
        print(f"Error: {response.status_code}")
    
    # Error handling untuk memastikan bahwa 'anime_data' tidak kosong
    if not anime_data:
        return render(request, 'error.html', {'message': 'Anime data not found'})

    start_date = datetime.fromisoformat(anime_data['aired']['from'])
    end_date = datetime.fromisoformat(anime_data['aired']['to'])
    context = {
        'anime_data': anime_data,
        'relation_length': len(anime_data.get('related', [])),
        'start_date':start_date,
        'recommendation': recommendations_data
        
    }
    return render(request, 'anime-view.html', context)


# def index_three(request, search_query):
#     from django.http import JsonResponse
#     headers = {'X-MAL-CLIENT-ID': API_KEY}
#     response = requests.get(f'https://api.myanimelist.net/v2/anime?q={search_query}&fields=mean,media_type,num_episodes,start_date,end_date', headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         return JsonResponse(data)
#     else:
#         print(f"Error: {response.status_code}")
            