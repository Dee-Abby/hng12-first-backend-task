import math
import requests
import threading
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.cache import cache



def get_fun_fact(n):
    cache_key = f"fun_fact_{n}"
    cached_fact = cache.get(cache_key)

    if cached_fact:
        return cached_fact

    url = f"http://numbersapi.com/{n}/math?json"
    try:
        response = requests.get(url, timeout=2)  # ⏳ Reduce timeout to prevent delays
        data = response.json()
        fact = data.get("text", "No fun fact found.")
        cache.set(cache_key, fact, timeout=86400)  # Cache for 24 hours
        return fact
    except requests.exceptions.RequestException:
        return "Could not fetch fun fact"



def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(n)) + 1, 2):  # Skip evens, start from 5
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    divisors = {1}
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.update({i, n // i})
    return sum(divisors) == n



def is_armstrong(n):
    digits = list(map(int, str(n)))
    power = len(digits)
    return sum(d ** power for d in digits) == n



def classify_number(n):
    cache_key = f"classify_{n}"
    cached_result = cache.get(cache_key)

    if cached_result:
        return cached_result

    properties = ["even" if n % 2 == 0 else "odd"]
    if is_armstrong(n):
        properties.append("armstrong")

    result = {
        "number": n,
        "is_prime": is_prime(n),
        "is_perfect": is_perfect(n),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(n)),
        "fun_fact": "Fetching..."  # Temporary placeholder
    }

    
    cache.set(cache_key, result, timeout=86400)  # Cache for 24 hours

    
    def fetch_fun_fact():
        result["fun_fact"] = get_fun_fact(n)
        cache.set(cache_key, result, timeout=86400)  # Update cache with fun fact

    threading.Thread(target=fetch_fun_fact).start()

    return result


@require_GET
def classify_number_view(request):
    number = request.GET.get("number")

    try:
        number = int(number.strip())  # Convert safely
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid input. Must be an integer."}, status=400)

    if number < 0:
        return JsonResponse({"error": "Negative numbers are not supported."}, status=400)

    return JsonResponse(classify_number(number), status=200)
