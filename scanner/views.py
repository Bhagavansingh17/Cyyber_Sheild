from django.shortcuts import render
from django.http import JsonResponse
import json

# Django normally requires a special token (CSRF) for security with POST requests.
# For this simple API, we will disable it for the 'analyze' function to make it easier
# for our frontend JavaScript to send data.
from django.views.decorators.csrf import csrf_exempt

# --- Function 1: Display the Homepage ---
# This function runs when a user first visits your website.
def index(request):
    """
    Renders the main HTML page.
    """
    # It simply takes the request and returns the 'index.html' template.
    return render(request, 'index.html')


# --- Function 2: The Analysis Engine ---
# This function runs when the frontend sends a URL to be analyzed.
@csrf_exempt  # Disables CSRF token requirement for this function
def analyze(request):
    """
    Analyzes the URL sent from the frontend and returns a risk score.
    """
    # We only want to process POST requests, which is how web forms send data.
    if request.method == 'POST':
        try:
            # Get the data sent from the JavaScript fetch request
            data = json.loads(request.body)
            url_to_check = data.get('url')

            if not url_to_check:
                return JsonResponse({'error': 'URL not provided'}, status=400)

            # --- Risk Analysis Logic (moved from JavaScript to Python) ---
            score = 0
            details = []

            # Check #1: Is it a secure connection?
            if not url_to_check.startswith('https://'):
                score += 30
                details.append('Connection is not secure (no HTTPS).')
            else:
                details.append('Uses a secure HTTPS connection.')

            # Check #2: Is the URL suspiciously long?
            if len(url_to_check) > 75:
                score += 15
                details.append('URL is unusually long.')

            # Check #3: Does it use a common URL shortener?
            shorteners = ['bit.ly', 't.co', 'tinyurl.com']
            if any(s in url_to_check for s in shorteners):
                score += 25
                details.append('Uses a URL shortener, which can hide the final destination.')

            # Check #4: Is it a direct IP address instead of a domain name?
            # This is a simplified check for demonstration.
            import re
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url_to_check.replace("https://", "").replace("http://", "")):
                 score += 40
                 details.append('URL is a direct IP address, which is highly suspicious.')

            # Make sure score doesn't go over 100
            final_score = min(score, 100)
            # -------------------------------------------------------------

            # Send the results back to the frontend as a JSON object
            return JsonResponse({
                'score': final_score,
                'details': details
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request format'}, status=400)

    # If it's not a POST request, return an error.
    return JsonResponse({'error': 'Invalid request method'}, status=405)

