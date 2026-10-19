import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def test_login():
    print("="*60)
    print("TEST LOGIN SISFO")
    print("="*60)
    
    base_url = "https://sisfo.upiyptk.ac.id"
    
    # Session
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/html, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
    })
    
    print("\nMengambil CSRF token...")
    try:
        response = session.get(f"{base_url}/login", timeout=10)
        print(f"   Status: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': '_token'})
        
        if csrf_token:
            csrf_token = csrf_token.get('value')
            print(f"   CSRF: {csrf_token[:30]}...")
        else:
            print("   CSRF tidak ditemukan!")
            return False
    except Exception as e:
        print(f"   Error: {e}")
        return False
    
    print("\nLogin...")
    try:
        login_data = {
            '_token': csrf_token,
            'username': username,
            'password': password
        }
        
        response = session.post(
            f"{base_url}/login",
            data=login_data,
            headers={
                'Origin': base_url,
                'Referer': f"{base_url}/login",
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json, text/html, */*',
            },
            allow_redirects=False,
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=2)}")
                
                if result.get('success') == True:
                    print("\n   LOGIN BERHASIL!")
                    
                    # Follow redirect
                    redirect_url = result.get('redirect')
                    if redirect_url:
                        if redirect_url.startswith('http'):
                            full_url = redirect_url
                        else:
                            full_url = urljoin(base_url, redirect_url)
                        
                        print(f"   Following redirect to: {full_url}")
                        dashboard_response = session.get(
                            full_url,
                            headers={
                                'Referer': f"{base_url}/login",
                                'X-Requested-With': 'XMLHttpRequest',
                            },
                            timeout=10
                        )
                        print(f"   Dashboard status: {dashboard_response.status_code}")
                        
                        if dashboard_response.status_code == 200:
                            soup = BeautifulSoup(dashboard_response.text, 'html.parser')
                            name = soup.find('span', class_='user-name') or soup.find('h4', class_='name')
                            if name:
                                print(f"   Nama: {name.text.strip()}")
                    
                    print("\n   Cookies:")
                    for key, value in session.cookies.get_dict().items():
                        print(f"      {key}: {value[:50]}...")
                    
                    return True
                else:
                    print(f"\n   Login gagal: {result}")
                    
            except json.JSONDecodeError:
                print("   Response bukan JSON")
                if 'dashboard' in response.text.lower():
                    print("\n   LOGIN BERHASIL! (HTML response)")
                    return True
                else:
                    print(f"\n   Response: {response.text[:200]}")
        else:
            print(f"\n   Login gagal: {response.status_code}")
            
    except Exception as e:
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return False

if __name__ == "__main__":
    try:
        success = test_login()
        print("\n" + "="*60)
        if success:
            print("ALL TESTS PASSED!")
        else:
            print("TESTS FAILED!")
        print("="*60)
    except Exception as e:
        print(f"Fatal Error: {e}")
        import traceback
        traceback.print_exc()
