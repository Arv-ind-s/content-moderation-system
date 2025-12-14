
import urllib.request
import json
import time

API_URL = "https://2a104jsmyk.execute-api.us-east-1.amazonaws.com/moderate"

def verify_api():
    payload = {
        "text": "You are stupid and I hate you."
    }
    
    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    
    req = urllib.request.Request(API_URL, data=data, headers=headers, method='POST')
    
    print(f"🚀 Sending request to: {API_URL}")
    print(f"📦 Payload: {payload}")
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')
            status_code = response.getcode()
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"✅ Response received in {duration:.2f} seconds")
            print(f"Status Code: {status_code}")
            
            response_json = json.loads(body)
            print("📄 Response Body:")
            print(json.dumps(response_json, indent=2))
            
            # assertions
            if response_json.get('is_toxic') is True:
                print("✅ Correctly identified as toxic.")
            else:
                print("❌ Failed to identify toxicity.")
                
            if 'toxicity_scores' in response_json:
                print("✅ Toxicity scores present.")
            else:
                print("❌ Missing toxicity scores.")
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        print(e.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_api()
