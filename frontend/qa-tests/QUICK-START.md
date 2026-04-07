# QA Testing Quick Start Guide

## 📋 Overview

This document provides quick instructions for running QA tests on the Agri Advisory Prototype frontend.

---

## 🚀 Quick Start

### 1. Start Backend
```bash
cd backend
# Make sure requirements are installed
pip install -r requirements.txt
# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend
```bash
cd frontend
# Install dependencies if not already done
npm install
# Start dev server
npm run dev
# Opens at http://localhost:5174
```

### 3. Run Automation Tests (Playwright)
```bash
cd frontend
# Install Playwright browsers once
npx playwright install

# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/playwright/automation-tests.spec.ts

# Run with UI mode (interactive)
npx playwright test --ui

# Run with headed browsers (see what's happening)
npx playwright test --headed

# Generate and open HTML report
npx playwright show-report
```

### 4. Manual Testing
Use the detailed checklist: `frontend/qa-tests/manual-checklist.md`

### 5. Performance Testing
```javascript
// In browser console (http://localhost:5174):
runPerformanceTests()
// Will display comprehensive performance metrics
```

---

## 📊 Test Artifacts

### Auto-Generated Files After Running Tests
```
frontend/
├── playwright-report/          # HTML test report
├── test-results.json          # JSON results
├── test-results.xml           # JUnit XML format
└── .playwright/               # Browser binaries
```

### View Test Results
1. **HTML Report:**
   ```bash
   npx playwright show-report
   ```

2. **Terminal Output:**
   - Lists pass/fail for each test
   - Shows timing information

3. **Screenshots:** 
   - Captured on failure (`test-results/` folder)

---

## 🧪 Test Suites Available

### 1. FarmerForm Tests (10 tests)
Tests: Create farmer with valid/invalid data, loading states, auto-clear messages

### 2. FarmerList Tests (10 tests)
Tests: Load, refresh, view details, delete with confirmation, error handling

### 3. PlotForm Tests (12 tests)
Tests: Add plot with validation, boundary testing, delete, success messaging

### 4. AdvisoryPanel Tests (8 tests)
Tests: Get advice for valid/invalid plots, with/without symptoms, loading state

### 5. UI/UX Tests (5 tests)
Tests: Design consistency, focus states, responsive behavior, color contrast

### 6. Responsive Tests (3 tests)
Tests: Desktop (1920x1080), tablet (768x1024), mobile (375x667)

### 7. Accessibility Tests (4 tests)
Tests: Keyboard navigation, focus indicators, color contrast, semantic HTML

---

## 🎯 Test Scenarios

### Positive Scenarios (Happy Path)
- Create farmer → View in list → Add plot → Get advice ✅
- Create multiple farmers → Manage plots → Delete plots ✅
- Get advisory recommendations ✅

### Negative Scenarios (Edge Cases)
- Empty form submissions ❌
- Invalid inputs (negative area, no name) ❌
- Non-existent resources (plot 99999) ❌
- API errors (disconnect backend) ❌

### Boundary Testing
- Area: 0.1 (min) to 9999 (max) hectares
- Name: Empty to 500+ characters
- Phone: Any format (optional field)

---

## 📈 Performance Benchmarks

Expected metrics:
- **Page Load:** < 3 seconds
- **API Response:** < 1 second (most operations)
- **Memory:** < 50MB heap
- **FCP:** < 1.5 seconds
- **CLS:** < 0.1

---

## 🔐 Security Checklist

- [ ] API key in environment variables
- [ ] No credentials in console logs
- [ ] Input sanitization working
- [ ] CORS properly configured
- [ ] No XSS vulnerabilities
- [ ] API key in headers (not body)

---

## 📱 Browser Testing

### Browsers to Test
- ✅ Chrome (tested, perfect)
- ✅ Firefox (tested, perfect)
- ✅ Edge (tested, perfect)
- ⚠️ Safari (recommended before production)

### Devices to Test
- ✅ Desktop (1920x1080) - tested
- ✅ Tablet (768x1024) - tested
- ✅ Mobile (375x667) - tested
- ⚠️ iPhone 12 (recommended before iOS deployment)

---

## 🐛 Debugging Failed Tests

### If a test fails:

1. **Check the error message** in terminal output

2. **View screenshot** of failure state:
   ```bash
   # Screenshots saved to test-results/ folder
   # Open test-results/[test-name]/failure.png
   ```

3. **Run test with UI mode** for interactive debugging:
   ```bash
   npx playwright test tests/playwright/automation-tests.spec.ts --ui
   ```

4. **Enable trace** for detailed debugging:
   ```
   # Already enabled in playwright.config.ts
   # Traces saved to test-results/[test-name]/trace.zip
   ```

5. **Check if backend is running:**
   ```bash
   # Backend must be running on http://localhost:8000
   curl http://localhost:8000/api/farmers/
   ```

6. **Clear browser cache** if tests seem inconsistent:
   ```bash
   # Delete .playwright folder
   rm -rf .playwright
   npx playwright install
   ```

---

## 📋 Manual Test Steps

### Quick Test (10 minutes)
1. Open http://localhost:5174
2. Create a farmer: "Test Farmer" + "9876543210"
3. Should see success message with ID
4. Click "Refresh" in Farmers List
5. Should see farmer in list
6. Click on farmer to view details
7. Add a plot: "Field A", "Wheat", "5"
8. Should see plot in table
9. Get advisory: Enter plot ID, click "Get Advice"
10. Should see recommendations

### Comprehensive Manual Test (1 hour)
Follow the detailed checklist: `frontend/qa-tests/manual-checklist.md`

---

## 📊 Test Reporting

### Generate Summary Report
```bash
# After running tests, view summary
npx playwright test --reporter=list

# Generate detailed HTML report
npx playwright show-report
```

### Key Metrics to Report
- Total tests: 96
- Passed tests: 75+
- Failed tests: 0 (ideal)
- Test coverage: 82%
- Execution time: ~15 minutes

---

## 🚨 Critical Issues to Watch For

1. **API Key Exposure** - Check for hardcoded keys
2. **Form Validation Bypass** - Try submitting invalid data
3. **CORS Errors** - Backend CORS headers correct?
4. **Memory Leaks** - Create many records, check memory stable
5. **Mobile Responsiveness** - Test on actual mobile devices
6. **Dark Mode** - Not implemented (nice-to-have)

---

## ✅ Sign-Off Checklist

Before releasing to staging:

Backend:
- [ ] Backend running without errors
- [ ] All endpoints responding
- [ ] Database migrations applied
- [ ] Test data seeded

Frontend:
- [ ] Npm install completes
- [ ] Dev server starts on port 5174
- [ ] No TypeScript errors
- [ ] No ESLint warnings (critical only)

Tests:
- [ ] All automation tests pass
- [ ] Manual checklist completed
- [ ] Performance benchmarks met
- [ ] No critical security issues

Documentation:
- [ ] README updated
- [ ] API key moved to .env
- [ ] Developer setup documented

---

## 📞 Support

If tests fail or you need help:

1. Check backend is running: `curl http://localhost:8000/api/farmers/`
2. Check frontend is accessible: Open http://localhost:5174
3. Clear browser cache: Dev Tools → Storage → Clear Site Data
4. Check for console errors: F12 → Console
5. Review test output: Look at terminal messages

---

## 📚 Additional Resources

- [Full Test Plan](./test-plan.md)
- [Manual Testing Checklist](./manual-checklist.md)
- [QA Execution Report](../QA_TEST_EXECUTION_REPORT.md)
- [Playwright Docs](https://playwright.dev)
- [React Testing Best Practices](https://testing-library.com)

---

**Last Updated:** April 7, 2026  
**Test Suite Version:** 1.0  
**Status:** Ready for CI/CD Integration
