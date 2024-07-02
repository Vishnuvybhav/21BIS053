from django.http import JsonResponse
import requests
from collections import deque
from calculator import settings

WINDOW_SIZE = 10
window = deque(maxlen=WINDOW_SIZE)

TEST_SERVER_URLS = {
    'p': 'http://20.244.56.144/test/prime',
    'f': 'http://20.244.56.144/test/fibonacci',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/random'
}

def fetch_numbers(number_id):
    url = TEST_SERVER_URLS.get(number_id)
    if url:
        try:
            headers = {
                'Authorization': f'Bearer {settings.ACCESS_TOKEN}'
            }
            response = requests.get(url, headers=headers, timeout=0.5)
            if response.status_code == 200:
                return response.json().get('numbers', [])
        except requests.RequestException:
            pass
    return []

def calculate_average(request, number_id):
    numbers = fetch_numbers(number_id)
    if not numbers:
        return JsonResponse({'error': 'Unable to fetch numbers'}, status=500)

    for number in numbers:
        if number not in window:
            window.append(number)

    avg = sum(window) / len(window) if window else 0
    return JsonResponse({
        'numbers': list(numbers),
        'windowPrevState': list(window)[:-len(numbers)],
        'windowCurrState': list(window),
        'avg': avg
    })