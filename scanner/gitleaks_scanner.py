import subprocess
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

class GitLeaksScanner:
    """GitLeaks integration for secret scanning in CI/CD pipeline"""
    
    def __init__(self, repo_path: str = ".", reports_dir: str = "reports"):
        self.repo_path = repo_path
        self.reports_dir = reports_dir
        self.ensure_reports_dir()
    
    def ensure_reports_dir(self):
        """Create reports directory if it doesn't exist"""
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def run_gitleaks_scan(self) -> Dict[str, Any]:
        """
        Run GitLeaks scan and return results
        Returns dict with scan results and metadata
        """
        try:
            # GitLeaks command to scan for secrets
            cmd = [
                "gitleaks", "detect",
                "--source", self.repo_path,
                "--report-format", "json",
                "--report-path", f"{self.reports_dir}/gitleaks-latest.json",
                "--verbose"
            ]
            
            print(f"Running GitLeaks scan on {self.repo_path}...")
            
            # Run the scan
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            
            # Parse results
            scan_results = {
                "timestamp": datetime.now().isoformat(),
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "findings": [],
                "summary": {
                    "total_findings": 0,
                    "critical_findings": 0,
                    "high_findings": 0,
                    "medium_findings": 0,
                    "low_findings": 0
                }
            }
            
            # Load findings if scan found secrets
            if os.path.exists(f"{self.reports_dir}/gitleaks-latest.json"):
                with open(f"{self.reports_dir}/gitleaks-latest.json", 'r') as f:
                    content = f.read().strip()
                    if content:  # Only parse if file has content
                        findings = json.loads(content)
                        scan_results["findings"] = findings
                        scan_results["summary"]["total_findings"] = len(findings)
                        
                        # Categorize findings by severity
                        for finding in findings:
                            severity = self._get_finding_severity(finding)
                            scan_results["summary"][f"{severity}_findings"] += 1
            
            return scan_results
            
        except subprocess.CalledProcessError as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": f"GitLeaks scan failed: {e}",
                "exit_code": e.returncode,
                "findings": [],
                "summary": {"total_findings": 0, "critical_findings": 0}
            }
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": f"Unexpected error: {e}",
                "exit_code": 1,
                "findings": [],
                "summary": {"total_findings": 0, "critical_findings": 0}
            }
    
    def _get_finding_severity(self, finding: Dict) -> str:
        """Determine severity of a finding based on rule type"""
        rule_id = finding.get("RuleID", "").lower()
        
        # Critical secrets
        critical_patterns = ["aws", "api_key", "private_key", "password", "token"]
        if any(pattern in rule_id for pattern in critical_patterns):
            return "critical"
        
        # High severity
        high_patterns = ["secret", "credential", "auth"]
        if any(pattern in rule_id for pattern in high_patterns):
            return "high"
        
        # Default to medium
        return "medium"
    
    def save_to_history(self, scan_results: Dict[str, Any]):
        """Save scan results to history file"""
        history_file = f"{self.reports_dir}/gitleaks-history.json"
        
        # Load existing history
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                history = []
        
        # Add current scan
        history.append(scan_results)
        
        # Keep only last 50 scans
        history = history[-50:]
        
        # Save updated history
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def print_summary(self, scan_results: Dict[str, Any]):
        """Print scan summary to console"""
        print("\n" + "="*60)
        print("GITLEAKS SECURITY SCAN SUMMARY")
        print("="*60)
        
        if "error" in scan_results:
            print(f"❌ Scan failed: {scan_results['error']}")
            return
        
        summary = scan_results["summary"]
        print(f"📊 Total findings: {summary['total_findings']}")
        print(f"🔴 Critical: {summary['critical_findings']}")
        print(f"🟠 High: {summary['high_findings']}")
        print(f"🟡 Medium: {summary['medium_findings']}")
        print(f"🟢 Low: {summary['low_findings']}")
        
        if scan_results["findings"]:
            print("\n📋 DETAILED FINDINGS:")
            for i, finding in enumerate(scan_results["findings"][:5], 1):  # Show first 5
                print(f"\n{i}. {finding.get('RuleID', 'Unknown Rule')}")
                print(f"   File: {finding.get('File', 'Unknown')}")
                print(f"   Line: {finding.get('StartLine', 'Unknown')}")
                print(f"   Description: {finding.get('Description', 'No description')}")
                
            if len(scan_results["findings"]) > 5:
                print(f"\n... and {len(scan_results['findings']) - 5} more findings")
        
        print("="*60)
    
    def should_fail_build(self, scan_results: Dict[str, Any]) -> bool:
        """Determine if build should fail based on findings"""
        if "error" in scan_results:
            return True
        
        summary = scan_results["summary"]
        # Fail build if critical secrets found
        return summary["critical_findings"] > 0

def main():
    """Main function for CLI usage"""
    scanner = GitLeaksScanner()
    
    # Run scan
    results = scanner.run_gitleaks_scan()
    
    # Save to history
    scanner.save_to_history(results)
    
    # Print summary
    scanner.print_summary(results)
    
    # Exit with appropriate code for CI/CD
    if scanner.should_fail_build(results):
        print("\n❌ Build should FAIL due to security findings!")
        sys.exit(1)
    else:
        print("\n✅ Build can PROCEED - no critical security issues found")
        sys.exit(0)

if __name__ == "__main__":
    main()
