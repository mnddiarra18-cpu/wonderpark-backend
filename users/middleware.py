import logging
from datetime import datetime

logger = logging.getLogger('security')

class SecurityLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Logger les tentatives de connexion
        if request.path == '/api/users/login/':
            ip = self.get_client_ip(request)
            if response.status_code == 200:
                logger.info(
                    f"Connexion réussie - IP: {ip} - "
                    f"{datetime.now()}"
                )
            elif response.status_code == 401:
                logger.warning(
                    f"Tentative échouée - IP: {ip} - "
                    f"{datetime.now()}"
                )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')