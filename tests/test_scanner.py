import pytest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
from scanner.gitleaks_scanner import GitLeaksScanner

class TestGitLeaksScanner:
    """Unit tests for GitLeaks scanner"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = GitLeaksScanner(repo_path=".", reports_dir=self.temp_dir)
    
    def test_ensure_reports_dir(self):
        """Test reports directory creation"""
        assert os.path.exists(self.temp_dir)
    
    def test_get_finding_severity(self):
        """Test severity classification"""
        # Critical finding
        critical_finding = {"RuleID": "aws-access-key"}
        assert self.scanner._get_finding_severity(critical_finding) == "critical"
        
        # High finding
        high_finding = {"RuleID": "generic-secret"}
        assert self.scanner._get_finding_severity(high_finding) == "high"
        
        # Medium finding (default)
        medium_finding = {"RuleID": "unknown-pattern"}
        assert self.scanner._get_finding_severity(medium_finding) == "medium"
    
    @patch('subprocess.run')
    def test_run_gitleaks_scan_success(self, mock_run):
        """Test successful GitLeaks scan"""
        # Mock successful subprocess run
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Scan completed successfully",
            stderr=""
        )
        
        # Create mock findings file
        findings_file = os.path.join(self.temp_dir, "gitleaks-latest.json")
        mock_findings = [
            {
                "RuleID": "aws-access-key",
                "File": "config.py",
                "StartLine": 10,
                "Description": "AWS Access Key detected"
            }
        ]
        
        with open(findings_file, 'w') as f:
            json.dump(mock_findings, f)
        
        # Run scan
        results = self.scanner.run_gitleaks_scan()
        
        # Assertions
        assert results["exit_code"] == 0
        assert results["summary"]["total_findings"] == 1
        assert results["summary"]["critical_findings"] == 1
        assert len(results["findings"]) == 1
    
    @patch('subprocess.run')
    def test_run_gitleaks_scan_no_findings(self, mock_run):
        """Test GitLeaks scan with no findings"""
        # Mock successful subprocess run with no findings
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="No secrets found",
            stderr=""
        )
        
        # Run scan
        results = self.scanner.run_gitleaks_scan()
        
        # Assertions
        assert results["exit_code"] == 0
        assert results["summary"]["total_findings"] == 0
        assert results["summary"]["critical_findings"] == 0
        assert len(results["findings"]) == 0
    
    def test_should_fail_build(self):
        """Test build failure logic"""
        # Should fail with critical findings
        critical_results = {
            "summary": {"critical_findings": 1, "total_findings": 1}
        }
        assert self.scanner.should_fail_build(critical_results) == True
        
        # Should pass with no critical findings
        safe_results = {
            "summary": {"critical_findings": 0, "total_findings": 2}
        }
        assert self.scanner.should_fail_build(safe_results) == False
        
        # Should fail with error
        error_results = {"error": "Scan failed"}
        assert self.scanner.should_fail_build(error_results) == True
    
    def test_save_to_history(self):
        """Test saving scan results to history"""
        # Create test results
        test_results = {
            "timestamp": "2024-01-01T00:00:00",
            "summary": {"total_findings": 0}
        }
        
        # Save to history
        self.scanner.save_to_history(test_results)
        
        # Verify file exists and contains data
        history_file = os.path.join(self.temp_dir, "gitleaks-history.json")
        assert os.path.exists(history_file)
        
        with open(history_file, 'r') as f:
            history = json.load(f)
        
        assert len(history) == 1
        assert history[0]["timestamp"] == "2024-01-01T00:00:00"

if __name__ == "__main__":
    pytest.main([__file__])
