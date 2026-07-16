# Test Reports - Patrika Web QA Automation Framework

## 📊 Reports Generated (2026-07-09)

### Report Files Available

```
reports/
├── pytest-report.html           (~53 KB) - Interactive HTML Report
├── execution_summary.txt        (4.5 KB) - Text Execution Summary
├── junit.xml                    (JUnit XML) - CI-friendly results
├── test-results.json            (JSON)     - Machine-readable results
├── pytest.log                   (Log)      - Test Execution Log
└── screenshots/                 (Directory) - Failure Screenshots
```

---

## 📈 LATEST TEST EXECUTION RESULTS

### Full Login Suite Execution

**Date:** 2026-07-09
**Framework:** Pytest 9.1.1 + Playwright (async)
**Platform:** Windows 10 (Python 3.14.6)
**Target:** Live site — www.patrika.com
**Duration:** 91.34 seconds

```
╔════════════════════════════════════════╗
║     TEST EXECUTION SUMMARY             ║
╠════════════════════════════════════════╣
║  Total Tests:           19             ║
║  ✅ Passed:            19 (100%)       ║
║  ❌ Failed:             0 (0%)         ║
║  ⏭️  Skipped:            0 (0%)         ║
╚════════════════════════════════════════╝
```

### Test Execution Timeline

```
TestLoginFromCSV
  ✅ test_tc_login_01_login_entry_point_visible
  ✅ test_tc_login_02_otp_triggered_for_valid_mobile
  ✅ test_tc_login_03_invalid_mobile_format_rejected
  ✅ test_tc_login_04_otp_rate_limit_check

TestLoginPositiveScenarios
  ✅ test_login_modal_displays_correctly
  ✅ test_valid_mobile_numbers[9876543210]
  ✅ test_valid_mobile_numbers[9123456789]
  ✅ test_valid_mobile_numbers[8765432109]
  ✅ test_valid_mobile_numbers[7654321098]
  ✅ test_valid_mobile_numbers[6543210987]

TestLoginNegativeScenarios
  ✅ test_invalid_mobile_numbers (8 malformed inputs)
  ✅ test_login_with_empty_input
```

---

## 🏷️ TEST EXECUTION BY MARKER

### Smoke Test Run
**Command:** `.venv\Scripts\python -m pytest -m smoke`

```
✅ 3 tests selected
   - test_tc_login_01_login_entry_point_visible
   - test_tc_login_02_otp_triggered_for_valid_mobile
   - test_login_modal_displays_correctly

Result: 3 passed ✅
```

### Regression Test Run
**Command:** `.venv\Scripts\python -m pytest -m regression`

```
✅ 16 tests selected
   - test_tc_login_03_invalid_mobile_format_rejected
   - test_tc_login_04_otp_rate_limit_check
   - test_valid_mobile_numbers      (5 parametrized cases)
   - test_invalid_mobile_numbers    (8 parametrized cases)
   - test_login_with_empty_input

Result: 16 passed ✅
```

### High-Priority Test Run
**Command:** `.venv\Scripts\python -m pytest -m high_priority`

```
✅ 2 tests selected
   - test_tc_login_01_login_entry_point_visible
   - test_tc_login_02_otp_triggered_for_valid_mobile

Result: 2 passed ✅
```

---

## 📋 REPORT FILES DESCRIPTION

### 1. **pytest-report.html** (Interactive HTML Report)

**Format:** HTML5 with embedded CSS & JavaScript (self-contained)
**Content:**
- Test execution timeline with status indicators
- Detailed test information (class, method, duration)
- Environment metadata (Python, platform, plugins)
- Configuration information
- Summary statistics and graphs
- Failed test details (if any)

**How to View:**
```bash
# Windows
start reports/pytest-report.html

# macOS
open reports/pytest-report.html

# Linux
xdg-open reports/pytest-report.html

# Or open directly in browser:
# File → Open → C:\Users\HP\patrika-web\reports\pytest-report.html
```

**Report Sections:**
1. **Summary Tab** - Overall test results
2. **Tests Tab** - Individual test details
3. **Failures Tab** - Failed test details (if any)
4. **Errors Tab** - Test errors (if any)

---

### 2. **execution_summary.txt** (Text Summary)

**Format:** Plain text
**Content:**
- Test session header information
- Environment metadata
- Pytest configuration info
- Full test execution list with status
- Execution time summary
- Generated report location

**Format:**
```
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
...
collected 19 items

tests/test_login_from_csv.py::TestLoginFromCSV::test_tc_login_01_login_entry_point_visible PASSED
...

======================== 19 passed in 91.34s =========================
```

---

### 3. **junit.xml / test-results.json** (Machine-Readable Results)

**Format:** JUnit XML and JSON
**Content:**
- Structured pass/fail results per test
- Durations and test IDs
- Suitable for dashboards or downstream tooling

---

### 4. **pytest.log** (Detailed Execution Log)

**Format:** Plain text log
**Content:**
- Detailed execution trace
- Print statements from tests
- Log entries from utilities
- Timing information

**To Enable Live Logging:** Set `log_cli = true` in `pytest.ini`

---

## 🎯 HOW TO GENERATE REPORTS

### Standard Execution (Generates HTML + Log)

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run the login suite with configured report generation
.venv\Scripts\python -m pytest tests/test_login_from_csv.py

# Reports automatically created in: reports/
```

### With Specific Report Options

```bash
# HTML Report Only
.venv\Scripts\python -m pytest tests/ --html=reports/report.html --self-contained-html

# HTML Report + JUnit XML
.venv\Scripts\python -m pytest tests/ --html=reports/report.html --junit-xml=reports/junit.xml

# With Console Output
.venv\Scripts\python -m pytest tests/ -v -s

# Show Test Durations
.venv\Scripts\python -m pytest tests/ --durations=10

# Detailed Failure Output
.venv\Scripts\python -m pytest tests/ -vv --tb=long
```

---

## 📊 REPORT CONTENT DETAILS

### Test Metadata in Reports

Each test report includes:

```
Test Name:        test_tc_login_01_login_entry_point_visible
Test Class:       TestLoginFromCSV
Test File:        tests/test_login_from_csv.py
Status:           PASSED ✅
Duration:         ~4.8s
Markers:          smoke, high_priority
Test ID:          tests/test_login_from_csv.py::TestLoginFromCSV::test_tc_login_01_login_entry_point_visible
```

### Environment Information Captured

```
Python Version:   3.14.6
Platform:         Windows-10 10.0.19045-SP0
Pytest Version:   9.1.1
Pluggy Version:   1.6.0

Plugins Installed:
  - pytest-html (4.2.0) - HTML report generation
  - pytest-metadata (3.1.1) - Metadata capture
  - pytest-asyncio (1.4.0) - Async test support
  - pytest-timeout (2.4.0) - Hang protection (30s guard)
```

---

## 🔧 CUSTOMIZING REPORTS

### Modify pytest.ini

Edit: `pytest.ini`

```ini
[pytest]
# Change HTML report location
addopts = --html=reports/custom-report.html

# Add JUnit XML for machine-readable results
addopts = --junit-xml=reports/junit.xml

# Change report style
addopts = --html=reports/report.html --self-contained-html --css=custom.css

# Show slow tests
addopts = --durations=5

# Custom markers
markers =
    smoke: Fast smoke tests
    regression: Full regression suite
    high_priority: High-priority tests
    medium_priority: Medium-priority tests
```

### Report Styling

The HTML report includes:
- **Dark/Light themes** - Switch in browser
- **Responsive design** - Works on mobile
- **Expandable sections** - Click to expand/collapse
- **Search functionality** - Search test names
- **Sorting** - Sort by status, duration, name

---

## 📈 REPORT METRICS & STATISTICS

### Test Execution Statistics

```
Total Tests Collected:    19
Tests Executed:          19
Tests Passed:            19 (100%)
Tests Failed:             0 (0%)
Tests Skipped:            0 (0%)

Execution Time:          91.34 seconds (live site)
Average Test Duration:   ~4.8 seconds per test
```

### By Test Class

```
TestLoginFromCSV:          4 tests - 100% pass rate
TestLoginPositiveScenarios: 6 tests - 100% pass rate
TestLoginNegativeScenarios: 9 tests - 100% pass rate
```

### By Marker/Tag

```
@smoke:            3 tests - 100% pass rate
@regression:      16 tests - 100% pass rate
@high_priority:    2 tests - 100% pass rate
@medium_priority:  2 tests - 100% pass rate
```

---

## 📚 FRAMEWORK REPORT FEATURES

### ✅ Implemented

- HTML reports with styling
- Test metadata capture
- Environment information
- Test timing and duration
- Pass/Fail/Skip tracking
- Test markers/tags
- Configuration information
- Plugin information
- Summary statistics
- JUnit XML + JSON output

### 🔜 Available Options

- Screenshots on failure (for Playwright tests)
- Video recordings (advanced)
- Allure reports (with pytest-allure)
- Coverage reports (with pytest-cov)

---

## 📞 TROUBLESHOOTING REPORTS

### HTML Report Not Generated

**Problem:** Report file doesn't exist
**Solution:**
1. Check `pytest-html` is installed: `.venv\Scripts\pip list | findstr pytest-html`
2. Verify report path in `pytest.ini`
3. Ensure `reports/` directory exists
4. Check file permissions

### Report Shows Warnings

**Problem:** Configuration warnings in output
**Solution:**
1. Update `pytest.ini` with missing options
2. Install missing pytest plugins
3. Remove unsupported config options

### Report Won't Open in Browser

**Problem:** Error opening HTML file
**Solution:**
1. Use full absolute path
2. Check file isn't corrupted (view in text editor)
3. Try different browser (Chrome/Firefox/Edge)
4. Check file permissions

---

## 📖 DOCUMENTATION LINKS

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-HTML Plugin](https://pytest-html.readthedocs.io/)
- [Playwright for Python](https://playwright.dev/python/)
- [Framework README](./README.md)
- [Test Report Structure](./TEST_REPORT_STRUCTURE.md)

---

## ✅ REPORT SUMMARY

**Status:** ✅ Framework reporting fully functional
**Last Generated:** 2026-07-09
**Test Success Rate:** 100% (19/19)
**Ready for:** Development & Production

**Next Steps:**
1. Review HTML report: `reports/pytest-report.html`
2. Configure test environment in `.env`
3. Create page objects for additional features
4. Write feature-specific tests
5. Run full test suite: `.venv\Scripts\python -m pytest`

---

*Framework Version: 1.0.0*
*Last Updated: 2026-07-14*
*Status: Production Ready ✅*
