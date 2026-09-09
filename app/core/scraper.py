import requests
import json
import re
import time
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class SISFOScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
        })
        self.csrf_token = None
        self.logged_in = False

    def _get_csrf_token(self) -> bool:
        """Mendapatkan CSRF token"""
        try:
            logger.info("🔍 Mengambil CSRF token...")
            
            response = self.session.get(
                f"{self.base_url}/login",
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Gagal akses login page: {response.status_code}")
                return False
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cari token di input field
            token_input = soup.find('input', {'name': '_token'})
            if token_input:
                self.csrf_token = token_input.get('value')
                logger.info(f"✅ CSRF token ditemukan: {self.csrf_token[:30]}...")
                return True
            
            # Cari di meta tag
            meta_token = soup.find('meta', {'name': 'csrf-token'})
            if meta_token:
                self.csrf_token = meta_token.get('content')
                logger.info(f"✅ CSRF token ditemukan di meta: {self.csrf_token[:30]}...")
                return True
            
            logger.error("❌ CSRF token tidak ditemukan")
            return False
            
        except Exception as e:
            logger.error(f"Error getting CSRF: {e}")
            return False

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login ke sistem"""
        try:
            # Step 1: Ambil CSRF token
            if not self._get_csrf_token():
                return {"success": False, "message": "Gagal ambil CSRF token"}

            # Step 2: Siapkan data login
            login_data = {
                '_token': self.csrf_token,
                'username': username,
                'password': password
            }
            
            logger.info(f"🔐 Mencoba login sebagai: {username}")

            # Step 3: Login
            response = self.session.post(
                f"{self.base_url}/login",
                data=login_data,
                headers={
                    'Origin': self.base_url,
                    'Referer': f"{self.base_url}/login",
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/html, */*',
                },
                allow_redirects=False  # Jangan auto redirect, kita handle manual
            )
            
            logger.info(f"Status: {response.status_code}")
            
            # Step 4: Handle response
            if response.status_code == 200:
                try:
                    # Parse JSON response
                    result = response.json()
                    logger.info(f"Response: {result}")
                    
                    # Cek apakah login berhasil
                    if result.get('success') == True:
                        self.logged_in = True
                        
                        # Follow redirect jika ada
                        redirect_url = result.get('redirect')
                        if redirect_url:
                            logger.info(f"🔄 Following redirect to: {redirect_url}")
                            # GET dashboard
                            dashboard_response = self.session.get(
                                f"{self.base_url}{redirect_url}" if redirect_url.startswith('/') else redirect_url,
                                headers={
                                    'Referer': f"{self.base_url}/login",
                                    'X-Requested-With': 'XMLHttpRequest',
                                }
                            )
                            logger.info(f"Dashboard status: {dashboard_response.status_code}")
                        
                        return {
                            "success": True, 
                            "message": result.get('message', 'Login berhasil'),
                            "data": result
                        }
                except json.JSONDecodeError:
                    # Bukan JSON, cek HTML
                    if 'dashboard' in response.text.lower() or 'selamat datang' in response.text.lower():
                        self.logged_in = True
                        return {"success": True, "message": "Login berhasil"}
            
            elif response.status_code == 302:
                # Redirect langsung
                location = response.headers.get('Location', '')
                if 'dashboard' in location.lower():
                    self.logged_in = True
                    # Follow redirect
                    self.session.get(f"{self.base_url}{location}")
                    return {"success": True, "message": "Login berhasil"}

            return {
                "success": False, 
                "message": f"Login gagal. Status: {response.status_code}"
            }

        except Exception as e:
            logger.error(f"Login error: {e}")
            return {"success": False, "message": str(e)}

    def _request(self, endpoint: str, params: Dict = None) -> Dict:
        """Helper request dengan autentikasi"""
        if not self.logged_in:
            return {"error": "Belum login"}

        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}",
                params=params,
                headers={
                    'Referer': f"{self.base_url}/dashboard",
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/html, */*',
                },
                timeout=30
            )

            if response.status_code == 200:
                try:
                    return response.json()
                except:
                    return {"html": response.text}
            else:
                return {"error": f"Status: {response.status_code}"}

        except Exception as e:
            logger.error(f"Request error: {e}")
            return {"error": str(e)}

    # ====== ENDPOINT METHODS ======
    
    def get_dashboard(self) -> Dict:
        return self._request('/dashboard')

    def get_jadwal(self, semester: Optional[str] = None) -> Dict:
        params = {}
        if semester:
            params['semester'] = semester
        return self._request('/jadwal-kuliah', params)

    def get_nilai(self, semester: Optional[str] = None) -> Dict:
        params = {}
        if semester:
            params['semester'] = semester
        return self._request('/nilai', params)

    def get_absensi(self, from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict:
        params = {}
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
        return self._request('/absensi', params)

    def get_krs(self, semester: Optional[str] = None) -> Dict:
        params = {}
        if semester:
            params['semester'] = semester
        return self._request('/krs', params)

    def get_transkrip(self) -> Dict:
        return self._request('/transkrip')

    def get_info_akademik(self) -> Dict:
        return self._request('/info-akademik')

    def get_biaya(self) -> Dict:
        return self._request('/biaya-kuliah')

    def logout(self):
        try:
            self.session.post(f"{self.base_url}/logout")
            self.logged_in = False
        except:
            pass