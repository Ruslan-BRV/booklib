import logging
import time

from django.utils.timezone import now


logger = logging.getLogger('books')


class LoggingMiddleware:
    """Middleware для логирования запросов и ответов.
    Этот middleware записывает информацию о каждом HTTP-запросе,
    включая метод, URL, заголовки, статус ответа и время обработки.
    В случае возникновения ошибок во время обработки запроса,
    они также будут зафиксированы в логах.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Обработка каждого запроса.
        Логирует информацию о запросе и ответе, включая время обработки запроса.
        """
        logger.info(f"Request: {request.method} {request.get_full_path()} at {now()}")
        logger.info(f"Request headers: {request.headers}")

        start_time = time.time()

        try:
            response = self.get_response(request)
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            raise  # Позволяет другим middleware обрабатывать ошибку

        duration = time.time() - start_time
        logger.info(f"Response: {response.status_code} at {now()}")
        logger.info(f"Processing time: {duration:.2f} seconds")

        return response
    