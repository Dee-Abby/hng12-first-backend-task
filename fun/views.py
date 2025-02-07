import math
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.cache import cache


def get_fun_fact(n):
    """Fetches a fun fact about a number from numbersapi.com, using caching."""
    cache_key = f"fun_fact_{n}"
    cached_fact = cache.get(cache_key)

    if cached_fact:
        return cached_fact

    url = f"http://numbersapi.com/{n}/math?json"
    try:
        response = requests.get(url)
        data = response.json()
        fact = data.get("text", "No fun fact found.")
        cache.set(cache_key, fact, timeout=86400)  # Cache for 24 hours
        return fact
    except requests.exceptions.RequestException:
        return "Could not fetch fun fact"


def is_prime(n):
    """Checks if a number is prime (only for positive numbers)."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def is_perfect(n):
    """Checks if a number is perfect (only for positive numbers)."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n


def is_armstrong(n):
    """Checks if a number is an Armstrong number."""
    digits = [int(d) for d in str(abs(n))]  # Use absolute value for digits
    return sum(d ** len(digits) for d in digits) == abs(n)


def classify_number(n):
    """Classifies the given number based on mathematical properties."""
    properties = ["even" if n % 2 == 0 else "odd"]

    if is_armstrong(n):
        properties.append("armstrong")

    return {
        "number": n,
        "is_prime": is_prime(n) if n > 0 else None,  # Prime only for positives
        "is_perfect": is_perfect(n) if n > 0 else None,  # Perfect only for positives
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(n))),  # Absolute value for digit sum
        "fun_fact": get_fun_fact(n),
    }


@require_GET
def classify_number_view(request):
    """Django view to classify a number passed as a GET parameter."""
    number = request.GET.get("number")

    if not number or not number.lstrip('-').isdigit():
        return JsonResponse({"number": number, "error": "Invalid input. Must be an integer."}, status=400)

    number = int(number)  # Convert to integer

    response = classify_number(number)
    return JsonResponse(response, status=200)
