# linktracker/tests.py
import json
from django.test import TestCase, Client
from .models import VisitedLink


class LinkTrackerTests(TestCase):

    def setUp(self):
        # Создаем клиент для отправки HTTP-запросов
        self.client = Client()

    def test_visited_links(self):
        # Тест для проверки корректного сохранения посещенных ссылок
        response = self.client.post(
            '/visited_links/',
            json.dumps({"links": ["https://example.com", "https://example.org"]}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(VisitedLink.objects.count(), 2)

    def test_visited_domains_all(self):
        # Тест для получения всех уникальных доменов
        response = self.client.post(
            '/visited_links/',
            json.dumps({"links": ["https://example.com", "https://example.com/123", "https://example.org", "https://example.org/123"]}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # Формируем запрос
        response = self.client.get('/visited_domains/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))

        # Проверяем, что возвращенные домены соответствуют ожидаемым
        expected_domains = {VisitedLink(link=link).get_domain() for link in ["https://example.com", "https://example.com/123", "https://example.org", "https://example.org/123"]}
        self.assertEqual(set(data["domains"]), expected_domains)

    def test_visited_domains_filtered(self):
        # Тест для получения уникальных доменов в заданном временном интервале
        response = self.client.post(
            '/visited_links/',
            json.dumps({"links": ["https://example.com", "https://example.com/123", "https://example.org", "https://example.org/123"]}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # Формируем запрос с временными фильтрами
        response = self.client.get('/visited_domains/', {'from': '0', 'to': '9999999999'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))

        # Проверяем, что возвращенные домены соответствуют ожидаемым
        expected_domains = {VisitedLink(link=link).get_domain() for link in ["https://example.com", "https://example.com/123", "https://example.org", "https://example.org/123"]}
        self.assertEqual(set(data["domains"]), expected_domains)
