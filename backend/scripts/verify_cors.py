import sys
import urllib.request
import urllib.error

def check_cors(origin):
    url = "http://127.0.0.1:8000/api/v1/documents"
    print(f"Testing CORS for origin: {origin}")
    
    req = urllib.request.Request(url, method="OPTIONS")
    req.add_header("Origin", origin)
    req.add_header("Access-Control-Request-Method", "GET")
    req.add_header("Access-Control-Request-Headers", "authorization")

    try:
        with urllib.request.urlopen(req) as response:
            acao = response.getheader('Access-Control-Allow-Origin')
            acac = response.getheader('Access-Control-Allow-Credentials')
            print(f"  Status: {response.status}")
            print(f"  Access-Control-Allow-Origin: {acao}")
            print(f"  Access-Control-Allow-Credentials: {acac}")
            
            if acao == origin:
                print("  ✅ CORS Header Present and Correct")
            else:
                print("  ❌ CORS Header Missing or Incorrect")
                
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error: {e.code}")
    except Exception as e:
        print(f"  Error: {e}")
    print("-" * 30)

if __name__ == "__main__":
    check_cors("http://localhost:3000")
