from django.http import JsonResponse
from django.conf import settings
import requests

TEST_SERVER_URLS = {
    'AMZ': 'http://20.244.56.144/test/companies/AMZ/categories',
    'FLP': 'http://20.244.56.144/test/companies/FLP/categories',
    'SNP': 'http://20.244.56.144/test/companies/SNP/categories',
    'MYN': 'http://20.244.56.144/test/companies/MYN/categories',
    'AZO': 'http://20.244.56.144/test/companies/AZO/categories',
}

def get_top_products(request, category_name):
    n = int(request.GET.get('top', 10))
    min_price = request.GET.get('minPrice', 0)
    max_price = request.GET.get('maxPrice', 100000)
    sort_by = request.GET.get('sortBy', 'price')
    order = request.GET.get('order', 'asc')

    results = []

    for company, base_url in TEST_SERVER_URLS.items():
        url = f"{base_url}/{category_name}/products"
        params = {
            'n': n,
            'minPrice': min_price,
            'maxPrice': max_price,
            'sortBy': sort_by,
            'order': order
        }

        try:
            headers = {
                'Authorization': f'Bearer {settings.ACCESS_TOKEN}'
            }
            response = requests.get(url, headers=headers, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results.extend(data)
            else:
                return JsonResponse({'error': f'Error fetching data from {company}'}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse(results, safe=False)

def get_product_details(request, category_name, product_id):
    company = request.GET.get('company', 'AMZ')
    
    if company not in TEST_SERVER_URLS:
        return JsonResponse({'error': 'Invalid company'}, status=400)

    url = f"{TEST_SERVER_URLS[company]}/{category_name}/products/{product_id}"

    try:
        headers = {
            'Authorization': f'Bearer {settings.ACCESS_TOKEN}'
        }
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Error fetching data from server'}, status=response.status_code)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
