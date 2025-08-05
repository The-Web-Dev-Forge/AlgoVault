from django.utils.deprecation import MiddlewareMixin
from ChatBot.views import get_or_create_visitor_session, track_page_visit

class VisitorTrackingMiddleware(MiddlewareMixin):
    """Middleware to automatically track all page visits"""
    
    def process_request(self, request):
        # Skip admin pages, static files, and API endpoints
        skip_paths = ['/admin/', '/static/', '/media/', '/api/', '/favicon.ico']
        
        if any(request.path.startswith(path) for path in skip_paths):
            return None
            
        # Skip if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return None
            
        try:
            # Track the page visit
            page_title = self.get_page_title(request.path)
            track_page_visit(request, page_title)
        except Exception as e:
            # Don't break the site if tracking fails
            print(f"Visitor tracking error: {e}")
            
        return None
    
    def get_page_title(self, path):
        """Get page title based on URL path"""
        path_titles = {
            '/': 'Home Page',
            '/tools/': 'Cryptography Tools',
            '/caesar/': 'Caesar Cipher',
            '/vigenere/': 'Vigenère Cipher',
            '/hill/': 'Hill Cipher',
            '/aes/': 'AES Encryption',
            '/des/': 'DES Encryption',
            '/rsa/': 'RSA Encryption',
            '/md5/': 'MD5 Hash',
            '/sha256/': 'SHA-256 Hash',
            '/sha512/': 'SHA-512 Hash',
            '/hmac/': 'HMAC',
            '/diffie-hellman/': 'Diffie-Hellman',
            '/ChatBot/chatbot/': 'AI Chatbot',
            '/about/': 'About Page',
            '/help/': 'Help Page',
        }
        
        return path_titles.get(path, f'Page: {path}')
