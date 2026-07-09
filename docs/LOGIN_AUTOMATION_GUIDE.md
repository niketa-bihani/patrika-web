# Automated Login Tests from CSV

## 📊 Overview

The Patrika Web QA Automation Framework now includes automated login tests generated from the **LoginTest.csv** file. These tests automate all login-related test cases with both positive and negative scenarios.

## 📁 Test Data

**CSV File:** `LoginTest.csv`  
**Location:** `test-data/` folder (organized for structured framework)

**Test Cases Included:**
1. TC-LOGIN-01: Login entry point visibility
2. TC-LOGIN-02: OTP triggering for valid mobile number
3. TC-LOGIN-03: Invalid mobile number rejection
4. TC-LOGIN-04: OTP rate-limiting

## 📂 Framework Components Added

### 1. CSV Data Loader (`utils/csv_loader.py`)

Utility class for loading and parsing CSV test data.

**Features:**
- Load entire CSV file
- Filter by module, priority, test type
- Load only automatable tests
- Get statistics about test data
- Retrieve specific test case by ID

**Usage:**
```python
from utils.csv_loader import CSVDataLoader
import os

# Path to test data
csv_path = os.path.join('test-data', 'LoginTest.csv')

# Load all tests
all_tests = CSVDataLoader.load_csv(csv_path)

# Load by module
login_tests = CSVDataLoader.load_test_cases_by_module(csv_path, 'Login')

# Load by priority
high_priority = CSVDataLoader.load_test_cases_by_priority(csv_path, 'High')

# Load automatable tests only
automatable = CSVDataLoader.load_automatable_tests(csv_path)

# Get statistics
stats = CSVDataLoader.get_statistics(csv_path)
print(stats)
```

### 2. Login Page Object (`pages/login_page.py`)

Page object for login functionality.

**Selectors:**
- `LOGIN_ICON_LOCATOR` - Login button/icon
- `MOBILE_INPUT_LOCATOR` - Mobile number input field
- `GET_OTP_BUTTON_LOCATOR` - "Get OTP" button
- `OTP_INPUT_LOCATOR` - OTP input field
- `ERROR_MESSAGE_LOCATOR` - Error message element
- `RESEND_OTP_BUTTON_LOCATOR` - "Resend OTP" button

**Methods:**
```python
# Navigation
await login_page.navigate_to_home()

# Modal operations
await login_page.click_login_icon()
await login_page.is_login_modal_visible()
await login_page.wait_for_login_modal()
await login_page.close_login_modal()

# Mobile input
await login_page.enter_mobile_number(mobile)
await login_page.get_mobile_input_value()
await login_page.clear_mobile_input()
await login_page.validate_mobile_number_format(mobile)

# OTP operations
await login_page.click_get_otp()
await login_page.is_otp_input_visible()
await login_page.is_otp_sent_confirmation_visible()
await login_page.enter_otp(otp_code)
await login_page.click_verify_otp()

# Rate limiting
await login_page.is_resend_button_disabled()
await login_page.get_resend_cooldown_text()
await login_page.click_resend_otp()

# Error handling
await login_page.is_error_message_visible()
await login_page.get_error_message()

# Full flow
await login_page.login_with_mobile(mobile_number)
```

### 3. Automated Login Tests (`tests/test_login_from_csv.py`)

Complete test suite with multiple test classes.

**Test Classes:**

#### TestLoginFromCSV
Direct mapping to CSV test cases:
- `test_tc_login_01_login_entry_point_visible` - TC-LOGIN-01
- `test_tc_login_02_otp_triggered_for_valid_mobile` - TC-LOGIN-02
- `test_tc_login_03_invalid_mobile_format_rejected` - TC-LOGIN-03
- `test_tc_login_04_otp_rate_limit_check` - TC-LOGIN-04

#### TestLoginPositiveScenarios
Positive test scenarios:
- `test_login_modal_displays_correctly` - Modal UI test
- `test_valid_mobile_numbers` - Parametrized tests with multiple valid numbers

#### TestLoginNegativeScenarios
Negative test scenarios:
- `test_invalid_mobile_numbers` - Parametrized tests with invalid numbers
- `test_login_with_empty_input` - Empty input handling

## 🚀 Running the Tests

### Run All Login Tests
```bash
.venv\Scripts\python -m pytest tests/test_login_from_csv.py -v
```

### Run Specific Test Class
```bash
# CSV-based tests only
.venv\Scripts\python -m pytest tests/test_login_from_csv.py::TestLoginFromCSV -v

# Positive scenarios
.venv\Scripts\python -m pytest tests/test_login_from_csv.py::TestLoginPositiveScenarios -v

# Negative scenarios
.venv\Scripts\python -m pytest tests/test_login_from_csv.py::TestLoginNegativeScenarios -v
```

### Run Specific Test Case
```bash
# TC-LOGIN-01
.venv\Scripts\python -m pytest tests/test_login_from_csv.py::TestLoginFromCSV::test_tc_login_01_login_entry_point_visible -v

# TC-LOGIN-02
.venv\Scripts\python -m pytest tests/test_login_from_csv.py::TestLoginFromCSV::test_tc_login_02_otp_triggered_for_valid_mobile -v
```

### Run by Marker
```bash
# Smoke tests
.venv\Scripts\python -m pytest tests/test_login_from_csv.py -m smoke -v

# High priority tests
.venv\Scripts\python -m pytest tests/test_login_from_csv.py -m high_priority -v

# Regression tests
.venv\Scripts\python -m pytest tests/test_login_from_csv.py -m regression -v

# Medium priority
.venv\Scripts\python -m pytest tests/test_login_from_csv.py -m medium_priority -v
```

### Run with Debugging
```bash
# Show print statements
.venv\Scripts\python -m pytest tests/test_login_from_csv.py -s -v

# Stop on first failure
.venv\Scripts\python -m pytest tests/test_login_from_csv.py -x

# Show slow tests
.venv\Scripts\python -m pytest tests/test_login_from_csv.py --durations=10

# Headed mode (see browser)
HEADED=true .venv\Scripts\python -m pytest tests/test_login_from_csv.py
```

### Generate Reports
```bash
# HTML Report
.venv\Scripts\python -m pytest tests/test_login_from_csv.py --html=reports/login-report.html --self-contained-html

# With captured output
.venv\Scripts\python -m pytest tests/test_login_from_csv.py -s --html=reports/login-report.html --self-contained-html
```

## 📊 CSV Data Structure

The LoginTest.csv contains the following columns:

| Column | Purpose | Example |
|--------|---------|---------|
| TC_ID | Test Case ID | TC-LOGIN-01 |
| Module | Test Module | Login |
| Test Case Title | Description | Verify Login entry point is visible |
| Priority | Priority Level | High, Medium, Low |
| Automatable | Can be automated | Yes, No |
| Test Type | Positive or Negative | Positive, Negative |
| Preconditions | Setup requirements | User is logged out |
| Test Steps | Steps to execute | 1. Open homepage, 2. Click Login |
| Test Data | Test data needed | Mobile Number: 9876543210 |
| Base URL | Application URL | https://www.patrika.com |
| Method | HTTP Method | GET, POST |
| Endpoint | API Endpoint | /login |
| Request Headers | API Headers | Authorization: Bearer token |
| Request Body | API Body | {"mobile": "9876543210"} |
| Expected Result | Expected outcome | Modal renders with input |
| Actual Result | Test result | (Filled during execution) |
| Status | Test status | Pass, Fail |

## 🎯 Test Execution Flow

### TC-LOGIN-01 Flow
```
1. Navigate to homepage
2. Click login icon/button
3. Wait for login modal
4. Verify modal displays
5. Verify mobile input is visible
✅ Test passes if modal opens correctly
```

### TC-LOGIN-02 Flow
```
1. Navigate to homepage
2. Open login modal
3. Enter valid mobile (9876543210)
4. Click "Get OTP"
5. Verify OTP input field appears
✅ Test passes if OTP field becomes visible
```

### TC-LOGIN-03 Flow
```
1. Navigate to homepage
2. Open login modal
3. Enter invalid mobile (98765 - too short)
4. Validate format (should be invalid)
5. Click "Get OTP"
6. Check for error or OTP not triggered
✅ Test passes if error shown or OTP not triggered
```

### TC-LOGIN-04 Flow
```
1. Navigate to homepage
2. Open login modal
3. Enter valid mobile
4. Click "Get OTP" (first time)
5. Wait 1 second
6. Check if Resend button is disabled
✅ Test passes if rate-limiting active
```

## 📈 Test Metrics

### CSV Statistics
```
Total Test Cases:       4
Automatable:           4 (100%)
By Priority:
  - High:              2
  - Medium:            2
By Type:
  - Positive:          2
  - Negative:          2
```

### Test Coverage
- ✅ Login entry point verification
- ✅ Valid mobile number OTP triggering
- ✅ Invalid mobile number rejection
- ✅ OTP rate-limiting
- ✅ Modal UI verification
- ✅ Multiple valid mobile number tests (parametrized)
- ✅ Multiple invalid mobile number tests (parametrized)
- ✅ Empty input handling

## 🔧 Customizing Tests

### Add New Test Case to CSV
1. Add row to `LoginTest.csv`
2. Follow existing column format
3. Run tests with CSV loader
4. New test data will be available

### Modify Page Selectors
If application UI changes, update `pages/login_page.py`:

```python
# Update selector
LOGIN_ICON_LOCATOR = "new-selector-here"

# Update method if needed
async def new_method(self):
    """New functionality."""
    await self.click(self.LOGIN_ICON_LOCATOR)
```

### Add New Test Methods
Add to appropriate test class in `tests/test_login_from_csv.py`:

```python
@pytest.mark.custom_marker
async def test_new_scenario(self, login_page: LoginPage):
    """New test case."""
    log_step(1, "Step 1")
    # Test code here
```

## 🎓 Best Practices

1. **Keep CSV Updated** - Update test data in CSV, regenerate tests as needed
2. **Use Markers** - Tag tests with @pytest.mark for easy filtering
3. **Clear Step Logging** - Use log_step() for better debugging
4. **Validate Locally** - Test first in headless, then headed mode
5. **Generate Reports** - Use HTML reports for better visibility
6. **Document Changes** - Keep this guide updated

## 📚 Related Files

- `test-data/LoginTest.csv` - CSV test data (in test-data folder)
- `pages/login_page.py` - Login page object
- `utils/csv_loader.py` - CSV data loader
- `tests/test_login_from_csv.py` - Test implementations
- `conftest.py` - Pytest configuration with fixtures
- `pytest.ini` - Pytest settings

## 🆘 Troubleshooting

### Tests Not Running
```bash
# Check CSV path
.venv\Scripts\python -c "from utils.csv_loader import CSVDataLoader; import os; csv_path = os.path.join('test-data', 'LoginTest.csv'); print(CSVDataLoader.get_statistics(csv_path))"

# Check imports
.venv\Scripts\python -c "from pages.login_page import LoginPage; print('OK')"
```

### Selectors Not Found
1. Update selector in `login_page.py`
2. Test with Playwright Inspector: `.venv\Scripts\playwright inspect https://www.patrika.com`
3. Run test with screenshots: `--html=reports/report.html`

### Tests Hanging
1. Increase timeout: `TIMEOUT=60000`
2. Check network connectivity
3. Try headed mode: `HEADED=true`

## ✅ Quick Start

```bash
# 1. Activate environment
.venv\Scripts\activate

# 2. Run all login tests
.venv\Scripts\python -m pytest tests/test_login_from_csv.py -v

# 3. View report
start reports/pytest-report.html
```

## 📞 Support

For issues or questions:
1. Check this guide
2. Review test logs
3. Run in debug mode: `.venv\Scripts\python -m pytest -vv -s --pdb`
4. Check framework docs: `README_PYTHON.md`

---

**Status:** ✅ Automated Login Tests Ready  
**Last Updated:** 2026-07-09  
**Framework Version:** 1.0.0
