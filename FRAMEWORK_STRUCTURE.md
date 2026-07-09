# Patrika Web QA Automation Framework - Project Structure

## 📁 Organized Framework Layout

This project follows a structured format with clear separation of concerns:

```
patrika-web/
│
├── 📚 DOCUMENTATION (docs/)
│   ├── README.md                      # Main framework overview
│   ├── README_PYTHON.md               # Python implementation guide
│   ├── LOGIN_AUTOMATION_GUIDE.md      # CSV-based login test guide
│   ├── CSV_AUTOMATION_SUMMARY.md      # CSV implementation summary
│   ├── TEST_REPORT_STRUCTURE.md       # HTML report structure
│   └── REPORTS_GUIDE.md               # Reporting best practices
│
├── 🧪 TEST DATA (test-data/)
│   └── LoginTest.csv                  # CSV test cases for login automation
│
├── 📄 FRAMEWORK CORE
│   ├── pages/                         # Page Object Model
│   │   ├── __init__.py               # Package exports
│   │   ├── base_page.py              # Base page class (15+ methods)
│   │   ├── home_page.py              # Home page object
│   │   └── login_page.py             # Login page object (25+ methods)
│   │
│   ├── tests/                         # Test Suites
│   │   ├── __init__.py
│   │   ├── test_demo.py              # Demo test suite (10 tests)
│   │   ├── test_example.py           # Example tests (6 tests)
│   │   └── test_login_from_csv.py    # CSV-based login tests (19 tests)
│   │
│   ├── utils/                         # Utilities & Helpers
│   │   ├── __init__.py               # Package exports
│   │   ├── csv_loader.py             # CSV data loader utility
│   │   └── test_helpers.py           # Helper functions (12+ utilities)
│   │
│   └── reports/                       # Test Reports
│       └── pytest-report.html         # Generated HTML test report
│
├── ⚙️ CONFIGURATION
│   ├── pytest.ini                     # Pytest configuration & markers
│   ├── conftest.py                    # Pytest fixtures
│   ├── .env                           # Environment variables
│   ├── requirements.txt               # Python dependencies
│   └── .gitignore                     # Git ignore patterns
│
├── 🐍 VIRTUAL ENVIRONMENT
│   └── .venv/                         # Python virtual environment
│
└── 📋 DOCUMENTATION (ROOT LEVEL)
    ├── FRAMEWORK_STRUCTURE.md         # This file - project structure guide
    └── (Other framework docs in docs/ folder)
```

## 📂 Folder Organization Strategy

### 1. Documentation Folder (`docs/`)
**Purpose:** Centralized location for all markdown documentation

**Contents:**
- Framework guides
- Implementation details
- Usage instructions
- Best practices

**Access:**
```bash
# View any documentation
cat docs/README.md
cat docs/LOGIN_AUTOMATION_GUIDE.md
cat docs/CSV_AUTOMATION_SUMMARY.md
```

### 2. Test Data Folder (`test-data/`)
**Purpose:** Centralized location for all CSV test data

**Contents:**
- LoginTest.csv - Login automation test cases

**Usage:**
```python
from utils.csv_loader import CSVDataLoader
import os

csv_path = os.path.join('test-data', 'LoginTest.csv')
test_data = CSVDataLoader.load_csv(csv_path)
```

### 3. Framework Core Folders

#### `pages/`
Page Object Model classes for different application pages
- BasePage: Foundation with 15+ common methods
- HomePage: Homepage-specific interactions
- LoginPage: Login flow automation (25+ methods)

#### `tests/`
Test suites organized by functionality
- test_demo.py: 10 passing demo tests
- test_example.py: 6 example tests
- test_login_from_csv.py: 19 CSV-based login tests

#### `utils/`
Reusable utilities and helpers
- CSVDataLoader: CSV parsing and filtering
- test_helpers.py: 12+ utility functions

## 🚀 Quick Start Commands

### Run All Tests
```bash
.venv\Scripts\python -m pytest -v
```

### Run CSV-Based Login Tests
```bash
.venv\Scripts\python -m pytest tests/test_login_from_csv.py -v
```

### View Documentation
```bash
# Main framework overview
start docs\README.md

# CSV automation guide
start docs\LOGIN_AUTOMATION_GUIDE.md

# Python implementation details
start docs\README_PYTHON.md
```

### Access Test Data
```bash
# View CSV test cases
type test-data\LoginTest.csv

# Load and analyze CSV
.venv\Scripts\python -c "from utils.csv_loader import CSVDataLoader; import os; print(CSVDataLoader.get_statistics('test-data/LoginTest.csv'))"
```

## 📊 Statistics

- **Documentation Files:** 6 guides in `docs/`
- **Test Data Files:** 1 CSV in `test-data/`
- **Total Tests:** 35+ tests (demo + example + login)
- **Page Objects:** 3 (Base, Home, Login)
- **Helper Utilities:** 12+ functions

## 🔄 File Reference Updates

All file references have been updated to use the new structure:

| Component | Old Path | New Path |
|-----------|----------|----------|
| CSV Data | `LoginTest.csv` | `test-data/LoginTest.csv` |
| Documentation | Root `.md` files | `docs/` folder |
| Test References | N/A | Updated in code |

### Code Updates Made

**test_login_from_csv.py:**
```python
# Before
CSV_FILE = os.path.join(os.path.dirname(__file__), '../LoginTest.csv')

# After
CSV_FILE = os.path.join(os.path.dirname(__file__), '../test-data/LoginTest.csv')
```

## 📚 Documentation Index

Located in `docs/` folder:

1. **README.md** - Framework overview and setup
2. **README_PYTHON.md** - Python-specific implementation guide
3. **LOGIN_AUTOMATION_GUIDE.md** - CSV login test automation
4. **CSV_AUTOMATION_SUMMARY.md** - CSV implementation details
5. **TEST_REPORT_STRUCTURE.md** - HTML report formatting
6. **REPORTS_GUIDE.md** - Reporting best practices

## 🎯 Design Principles

### Separation of Concerns
- Documentation separate from code
- Test data separate from test logic
- Page objects separate from test implementations

### Scalability
- Easy to add new test data files to `test-data/`
- Easy to add new documentation to `docs/`
- Clear structure for adding new page objects

### Maintainability
- Centralized documentation for easy updates
- Organized test data for quick access
- Consistent folder structure

## ✅ Framework Status

```
✅ Structured layout with dedicated folders
✅ Documentation centralized in docs/
✅ Test data organized in test-data/
✅ All file references updated
✅ Framework ready for execution
```

## 🔗 Related Files

- **Configuration:** [pytest.ini](pytest.ini), [conftest.py](conftest.py), [.env](.env)
- **Dependencies:** [requirements.txt](requirements.txt)
- **Framework Code:** [pages/](pages/), [tests/](tests/), [utils/](utils/)
- **Reports:** [reports/](reports/)

## 📞 Getting Started

1. **Read the main guide:**
   ```bash
   start docs\README.md
   ```

2. **Set up environment:**
   ```bash
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run tests:**
   ```bash
   .venv\Scripts\python -m pytest -v
   ```

4. **View reports:**
   ```bash
   start reports\pytest-report.html
   ```

## 📝 Notes

- All `.md` documentation files are in the `docs/` folder
- All `.csv` test data files are in the `test-data/` folder
- Framework code remains in `pages/`, `tests/`, `utils/` folders
- Configuration files stay in project root

---

**Framework Version:** 1.0.0 (Organized Structure)  
**Last Updated:** 2026-07-09  
**Structure Status:** ✅ Complete
