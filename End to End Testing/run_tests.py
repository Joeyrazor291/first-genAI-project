#!/usr/bin/env python3
"""
Test Execution Script

Convenient script to run end-to-end tests with various options.
Handles API server checking and provides clear output.
"""

import sys
import subprocess
import argparse
import time
import httpx
from pathlib import Path


def check_api_server(base_url: str = "http://localhost:8000", timeout: int = 5) -> bool:
    """
    Check if API server is running.
    
    Args:
        base_url: Base URL of API server
        timeout: Timeout in seconds
        
    Returns:
        True if server is running, False otherwise
    """
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(f"{base_url}/health")
            return response.status_code == 200
    except (httpx.ConnectError, httpx.TimeoutException):
        return False


def wait_for_api_server(base_url: str = "http://localhost:8000", max_wait: int = 30) -> bool:
    """
    Wait for API server to become available.
    
    Args:
        base_url: Base URL of API server
        max_wait: Maximum time to wait in seconds
        
    Returns:
        True if server became available, False if timeout
    """
    print(f"⏳ Waiting for API server at {base_url}...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if check_api_server(base_url):
            print(f"✓ API server is ready")
            return True
        
        time.sleep(1)
        print(".", end="", flush=True)
    
    print(f"\n✗ API server not available after {max_wait}s")
    return False


def run_pytest(args: list) -> int:
    """
    Run pytest with given arguments.
    
    Args:
        args: List of pytest arguments
        
    Returns:
        Exit code from pytest
    """
    cmd = ["pytest"] + args
    print(f"\n🧪 Running: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Run end-to-end tests for AI Restaurant Recommendation Service",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                    # Run all tests
  python run_tests.py --fast             # Run only fast tests
  python run_tests.py --category flow    # Run complete flow tests
  python run_tests.py --coverage         # Run with coverage report
  python run_tests.py --parallel         # Run tests in parallel
        """
    )
    
    parser.add_argument(
        "--category",
        choices=["flow", "api", "validation", "database", "llm", "error", "performance", "security"],
        help="Run specific test category"
    )
    
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Run only fast tests (exclude slow tests)"
    )
    
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run with coverage report"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel (requires pytest-xdist)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--no-api-check",
        action="store_true",
        help="Skip API server availability check"
    )
    
    parser.add_argument(
        "--html-report",
        action="store_true",
        help="Generate HTML test report"
    )
    
    parser.add_argument(
        "--markers",
        help="Run tests matching given mark expression (e.g., 'not slow')"
    )
    
    parser.add_argument(
        "pytest_args",
        nargs="*",
        help="Additional pytest arguments"
    )
    
    args = parser.parse_args()
    
    # Check API server availability
    if not args.no_api_check:
        if not wait_for_api_server():
            print("\n❌ API server is not running!")
            print("\nTo start the API server:")
            print("  cd restaurant-recommendation/phase-2-recommendation-api")
            print("  python src/main.py")
            print("\nOr skip this check with --no-api-check")
            return 1
    
    # Build pytest arguments
    pytest_args = []
    
    # Category selection
    if args.category:
        category_map = {
            "flow": "test_e2e_complete_flow.py",
            "api": "test_e2e_api_endpoints.py",
            "validation": "test_e2e_preference_validation.py",
            "database": "test_e2e_database_integration.py",
            "llm": "test_e2e_llm_integration.py",
            "error": "test_e2e_error_handling.py",
            "performance": "test_e2e_performance.py",
            "security": "test_e2e_security.py",
        }
        pytest_args.append(category_map[args.category])
    
    # Fast tests only
    if args.fast:
        pytest_args.extend(["-m", "not slow"])
    
    # Markers
    if args.markers:
        pytest_args.extend(["-m", args.markers])
    
    # Coverage
    if args.coverage:
        pytest_args.extend([
            "--cov=../restaurant-recommendation",
            "--cov-report=html",
            "--cov-report=term"
        ])
    
    # Parallel execution
    if args.parallel:
        pytest_args.extend(["-n", "auto"])
    
    # Verbose
    if args.verbose:
        pytest_args.append("-v")
    else:
        pytest_args.append("-v")  # Always use verbose by default
    
    # HTML report
    if args.html_report:
        pytest_args.extend([
            "--html=test_report.html",
            "--self-contained-html"
        ])
    
    # Additional pytest arguments
    if args.pytest_args:
        pytest_args.extend(args.pytest_args)
    
    # Run tests
    exit_code = run_pytest(pytest_args)
    
    # Print summary
    print("\n" + "="*70)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ Tests failed with exit code {exit_code}")
    
    if args.coverage:
        print("\n📊 Coverage report generated: htmlcov/index.html")
    
    if args.html_report:
        print("📄 Test report generated: test_report.html")
    
    print("="*70 + "\n")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
