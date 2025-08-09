#!/usr/bin/env python3
"""
Test runner script for CliniSight project.

This script discovers and runs all unit tests in the project.
It can be run from the project root directory.
"""

import os
import sys
import unittest
import argparse
import logging
from pathlib import Path

# Set required environment variables for testing
# This must be done before any imports that might check these variables
os.environ.setdefault('OPENAI_API_KEY', 'dummy-key-for-testing')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_python_path():
    """Add the ingest directory to Python path for imports."""
    project_root = Path(__file__).parent
    ingest_path = project_root / "ingest"
    
    if ingest_path.exists():
        sys.path.insert(0, str(ingest_path))
        logger.info(f"Added {ingest_path} to Python path")
    else:
        logger.warning(f"Ingest directory not found at {ingest_path}")


def discover_tests(start_dir="ingest"):
    """Discover all test files in the project."""
    project_root = Path(__file__).parent
    test_dir = project_root / start_dir
    
    if not test_dir.exists():
        logger.error(f"Test directory not found: {test_dir}")
        return []
    
    # Find all test files
    test_files = []
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                test_path = Path(root) / file
                test_files.append(str(test_path))
    
    logger.info(f"Found {len(test_files)} test files:")
    for test_file in test_files:
        logger.info(f"  - {test_file}")
    
    return test_files


def run_tests(test_files=None, verbose=False, pattern=None):
    """Run the discovered tests."""
    if test_files is None:
        test_files = discover_tests()
    
    if not test_files:
        logger.error("No test files found!")
        return False
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests from each file
    for test_file in test_files:
        try:
            # Convert file path to module path
            # Remove the project root and .py extension
            project_root = Path(__file__).parent
            relative_path = Path(test_file).relative_to(project_root)
            module_path = str(relative_path).replace('/', '.').replace('\\', '.')
            if module_path.endswith('.py'):
                module_path = module_path[:-3]
            
            # Load tests from the module
            module_tests = loader.loadTestsFromName(module_path)
            suite.addTests(module_tests)
            logger.info(f"Loaded tests from {test_file}")
            
        except Exception as e:
            logger.error(f"Failed to load tests from {test_file}: {e}")
    
    if not suite.countTestCases():
        logger.error("No test cases found!")
        return False
    
    # Run tests
    logger.info(f"Running {suite.countTestCases()} test cases...")
    
    # Configure test runner
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    
    # Run the tests
    result = runner.run(suite)
    
    # Report results
    logger.info(f"\nTest Results:")
    logger.info(f"  Tests run: {result.testsRun}")
    logger.info(f"  Failures: {len(result.failures)}")
    logger.info(f"  Errors: {len(result.errors)}")
    logger.info(f"  Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        logger.error("\nFailures:")
        for test, traceback in result.failures:
            logger.error(f"  {test}: {traceback}")
    
    if result.errors:
        logger.error("\nErrors:")
        for test, traceback in result.errors:
            logger.error(f"  {test}: {traceback}")
    
    return result.wasSuccessful()


def main():
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(
        description="Run all unit tests for the CliniSight project"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "-p", "--pattern",
        type=str,
        help="Pattern to match test files (e.g., 'test_embedding')"
    )
    parser.add_argument(
        "--test-dir",
        type=str,
        default="ingest",
        help="Directory to search for tests (default: ingest)"
    )
    
    args = parser.parse_args()
    
    # Setup Python path
    setup_python_path()
    
    # Discover tests
    test_files = discover_tests(args.test_dir)
    
    # Filter by pattern if specified
    if args.pattern:
        test_files = [f for f in test_files if args.pattern in f]
        logger.info(f"Filtered to {len(test_files)} test files matching pattern '{args.pattern}'")
    
    # Run tests
    success = run_tests(test_files, args.verbose, args.pattern)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 