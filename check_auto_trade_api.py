import requests
import json

# The URL for your Flask API's trade endpoint
# You can change this URL if your server is running on a different address.
API_URL = "http://127.0.0.1:5001/api/trade"

def check_api(url):
    """
    Performs a series of tests to check if the Flask API is running
    and correctly handling both GET and POST requests.
    """
    print("--- Running API Health Check ---")

    # --- Test 1: Check if the server is running (with a GET request) ---
    print("\n[1/2] Checking if the server is running with a GET request...")
    try:
        get_response = requests.get(url, timeout=5)
        if get_response.status_code == 405:
            print("✅ Status Check: Server is running and correctly rejecting GET requests (Status 405).")
        elif get_response.status_code == 200:
            print("⚠️ Warning: Server is running but accepting GET requests. Expected a 405 status code.")
        else:
            print(f"⚠️ Warning: Server is running but returned an unexpected status code: {get_response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: API is not reachable. Is your Flask server running?")
        return
    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out. The server might be slow or not responding.")
        return
    except Exception as e:
        print(f"❌ An unexpected error occurred during the GET test: {e}")
        return

    # --- Test 2: Check if the API correctly handles a POST request ---
    print("\n[2/2] Checking if the API handles a POST request with valid JSON...")
    # This payload must match the data format your Flask API expects.
    test_payload = {
        "symbol": "EURUSD=X",
        "signal": "call",
        "amount": 10
    }
    try:
        post_response = requests.post(url, json=test_payload, timeout=5)
        if post_response.status_code == 200:
            print("✅ POST Test: Signal was successfully sent and received by the API.")
            print(f"   -> API Response: {post_response.json()}")
        else:
            print(f"❌ POST Test Failed: API returned an unexpected status code: {post_response.status_code}")
            print(f"   -> Response Body: {post_response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during the POST test: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred during the POST test: {e}")

    print("\n--- Check complete. ---")

if __name__ == "__main__":
    check_api(API_URL)
