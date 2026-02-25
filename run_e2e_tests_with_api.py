#!/usr/bin/env python3
"""
Comprehensive E2E Test Runner with API Server Management

This script:
1. Starts the API server
2. Waits for it to be ready
3. Runs all E2E tests
4. Generates reports
5. Cleans up
"""

import subprocess
import time
import sys
import httpx
import os
from pathlib import Path
import signal

# Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_BASE_URL = f"http://localhost:{API_PORT}"
MAX_RETRIES = 30
RETRY_DELAY = 1.0

# Process reference
api_process = None


def check_api_ready(base_url: str = API_BASE_URL, timeout: int = 5) -> bool:
    """Check if API server is ready."""
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(f"{base_url}/health")
            return response.status_code == 200
    except (httpx.ConnectError, httpx.TimeoutException, Exception):
        return False


def wait_for_api(max_wait: int = 60) -> bool:
    """Wait for API server to become available."""
    print(f"\n⏳ Waiting for API server at {API_BASE_URL}...")
    
    start_time = time.time()
    attempt = 0
    while time.time() - start_time < max_wait:
        if check_api_ready():
            print(f"✓ API server is ready!\n")
            return True
        
        attempt += 1
        print(f"  Attempt {attempt}: Waiting... ({int(time.time() - start_time)}s)", end="\r")
        time.sleep(RETRY_DELAY)
    
    print(f"\n✗ API server not available after {max_wait}s")
    return False


def start_api_server() -> subprocess.Popen:
    """Start the API server."""
    print("🚀 Starting API server...")
    
    api_dir = Path("restaurant-recommendation/phase-2-recommendation-api")
    
    # Start the API server
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.api:app", 
         "--host", API_HOST, "--port", str(API_PORT)],
        cwd=str(api_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return process


def run_tests() -> int:
    """Run all E2E tests."""
    print("\n" + "="*70)
    print("🧪 Running End-to-End Tests")
    print("="*70 + "\n")
    
    # Set environment variable for UTF-8 encoding
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    # Run pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "End to End Testing",
        "-v",
        "--tb=short",
        "-m", "not slow",  # Skip slow tests for faster execution
        "--html=test_report.html",
        "--self-contained-html"
    ]
    
    result = subprocess.run(cmd, env=env)
    return result.returncode


def cleanup(process: subprocess.Popen):
    """Clean up resources."""
    if process:
        print("\n🛑 Stopping API server...")
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        print("✓ API server stopped")


def main():
    """Main execution."""
    global api_process
    
    try:
        # Start API server
        api_process = start_api_server()
        time.sleep(2)  # Give it a moment to start
        
        # Wait for API to be ready
        if not wait_for_api():
            print("\n❌ Failed to start API server")
            cleanup(api_process)
            return 1
        
        # Run tests
        exit_code = run_tests()
        
        # Print summary
        print("\n" + "="*70)
        if exit_code == 0:
            print("✅ All tests passed!")
        else:
            print(f"❌ Tests failed with exit code {exit_code}")
        print("="*70)
        print("\n📄 Test report: test_report.html")
        
        return exit_code
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test execution interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    finally:
        cleanup(api_process)


if __name__ == "__main__":
    sys.exit(main())
