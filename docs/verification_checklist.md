# ✅ Verification Checklist
---

# Phase 4 Verification Checklist (QA)

✅ **Pipeline**
- [ ] GitHub Actions runs on push to main
- [ ] Unit tests executed
- [ ] Security scans executed without errors
- [ ] Reports uploaded to AWS S3
- [ ] EC2 auto-deploy works

✅ **Dashboard**
- [ ] Dashboard loads at `/dashboard`
- [ ] Trend line updates with new builds
- [ ] Severity colors match expected
- [ ] Responsive layout verified (mobile + desktop)

✅ **Docs**
- [ ] README updated
- [ ] CI/CD and dashboard guides present
---


## Phase 5 — Alerts & Notifications

- [ ] `config/config.yaml` contains notifications section.  
- [ ] `scripts/notify.py` runs without errors.  
- [ ] Slack webhook tested successfully.  
- [ ] Email alerts tested (optional).  
- [ ] GitHub Secrets correctly configured.  
- [ ] Workflow calls `scripts/notify.py` on failure.  
- [ ] Unit tests in `tests/test_notify.py` pass.  
- [ ] Slack message includes repo name, build ID, and severity counts.  
- [ ] Documentation (`docs/notify.md`) reviewed and committed.
