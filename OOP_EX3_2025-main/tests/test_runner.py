import unittest
import os

def run_tests():
    # Print the current working directory
    print(f"Current working directory: {os.getcwd()}")

    # Discover and load all test cases in the current directory
    test_loader = unittest.TestLoader()
    print("Discovering tests...")
    test_suite = test_loader.discover(start_dir='.', pattern='test_*.py')  # Adjust pattern if necessary
    print(f"Found {test_suite.countTestCases()} test cases.")

    # Run the test suite
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    print(f"Tests run: {result.testsRun}")
    print(f"Errors: {len(result.errors)}")
    print(f"Failures: {len(result.failures)}")

if __name__ == "__main__":
    run_tests()