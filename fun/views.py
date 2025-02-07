import math
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.cache import cache


def get_fun_fact(n):
    cache_key = f"fun_fact_{n}"
    cached_fact = cache.get(cache_key)

    if cached_fact:
        return cached_fact

    url = f"http://numbersapi.com/{n}/math?json"  # 
    try:
        response = requests.get(url)
        data = response.json()
        fact = data.get("text", "No fun fact found.")
        cache.set(cache_key, fact, timeout=86400)  # Cache for 24 hours
        return fact
    except requests.exceptions.RequestException:
        return "Could not fetch fun fact"


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def is_perfect(n):
    return sum(i for i in range(1, n) if n % i == 0) == n


def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n


def classify_number(n):
    properties = []

    if n % 2 == 0:
        properties.append('even')
    else:
        properties.append('odd')

    if is_armstrong(n):
        properties.append('armstrong')

    return {
        "number": n,
        "is_prime": is_prime(n),
        "is_perfect": is_perfect(n),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(n)),
        "fun_fact": get_fun_fact(n),
    }


@require_GET
def classify_number_view(request):
    number = request.GET.get("number")

    # Validate input: ensure it's an integer
    if not number or not number.lstrip('-').isdigit():
        return JsonResponse({"number": number, "error": "Invalid input. Must be an integer."}, status=400)

    number = int(number)  # Convert to integer before checking negativity

    if number < 0:
        return JsonResponse({
            "number": number,
            "error": "Negative numbers are not supported",
        }, status=400)

    response = classify_number(number)
    return JsonResponse(response, status=200)

