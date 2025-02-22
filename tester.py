import pytest
import os

for test_file in os.listdir('tests'):
    if test_file.startswith('test_') and test_file.endswith('.py'):
        result = pytest.main(['tests/' + test_file, '-q'])
        if result == 0:
            print("Passed")
        else:
            print("Failed")
