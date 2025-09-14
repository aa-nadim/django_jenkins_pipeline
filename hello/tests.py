from django.test import TestCase, Client
from django.urls import reverse

class SimpleHelloTestCase(TestCase):
    """Simple test cases for CI/CD learning"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_homepage_loads(self):
        """Test that homepage loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        print("✅ Homepage loads successfully")
    
    def test_homepage_contains_hello(self):
        """Test that homepage contains hello message"""
        response = self.client.get('/')
        self.assertContains(response, 'Hello')
        print("✅ Homepage contains Hello message")
    
    def test_homepage_contains_django_text(self):
        """Test that homepage mentions Django"""
        response = self.client.get('/')
        self.assertContains(response, 'Django')
        print("✅ Homepage mentions Django")
    
    def test_health_check_works(self):
        """Test that health check endpoint works"""
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        print("✅ Health check endpoint works")
    
    def test_health_check_returns_json(self):
        """Test that health check returns JSON"""
        response = self.client.get('/health/')
        self.assertEqual(response['content-type'], 'application/json')
        print("✅ Health check returns JSON")
    
    def test_health_check_status_healthy(self):
        """Test that health check status is healthy"""
        response = self.client.get('/health/')
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        print("✅ Health check status is healthy")

class BasicIntegrationTest(TestCase):
    """Basic integration tests"""
    
    def test_app_is_working(self):
        """Test that the Django app is working"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 0)
        print("✅ Django app is working")
    
    def test_template_renders(self):
        """Test that template renders without errors"""
        response = self.client.get('/')
        # Check for HTML5 doctype and html tag (more flexible)
        self.assertIn(b'<!DOCTYPE html>', response.content)
        self.assertIn(b'<html', response.content)  # This will match <html lang="en"> too
        self.assertIn(b'</html>', response.content)
        print("✅ Template renders successfully")