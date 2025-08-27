#!/usr/bin/env python3
"""
Security scanning script for CI/CD integration
This script runs GitLeaks scanning and can be integrated into CI/CD pipelines
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.gitleaks_scanner import GitLeaksScanner

def main():
    """Main function for security scanning"""
    print("🔒 Starting DevSecOps Security Scan...")
    
    # Initialize scanner
    scanner = GitLeaksScanner(repo_path=".", reports_dir="reports")
    
    # Run GitLeaks scan
    print("🔍 Running GitLeaks secret detection...")
    results = scanner.run_gitleaks_scan()
    
    # Save results to history
    scanner.save_to_history(results)
    
    # Print summary
    scanner.print_summary(results)
    
    # Determine exit code for CI/CD
    if scanner.should_fail_build(results):
        print("\nSECURITY SCAN FAILED - Build should be stopped!")
        print("Please review and fix security issues before proceeding.")
        sys.exit(1)
    else:
        print("\nSECURITY SCAN PASSED - Build can proceed")
        sys.exit(0)

if __name__ == "__main__":
    main()
