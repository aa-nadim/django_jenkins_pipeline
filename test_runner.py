#!/usr/bin/env python
"""
Local test runner for Django Hello World application
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def run_tests():
    """Run Django tests locally"""
    print("🧪 Starting Django Hello World Tests...")
    print("=" * 50)
    
    # Configure Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_jenkins_pipeline.settings')
    django.setup()
    
    # Get test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False)
    
    # Run tests
    failures = test_runner.run_tests(['hello.tests'])
    
    print("=" * 50)
    if failures:
        print(f"❌ {failures} test(s) failed!")
        sys.exit(1)
    else:
        print("✅ All tests passed successfully!")
        print("🎉 Your Django application is working correctly!")

if __name__ == '__main__':
    run_tests()