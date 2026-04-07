# QA Test Plan - Agri Advisory Prototype

**Test Date:** April 7, 2026  
**Tester:** Senior QA Engineer  
**Application:** Agri Advisory Prototype  
**Frontend URL:** http://localhost:5174  
**Backend URL:** http://localhost:8000/api  

---

## 1. Application Overview

### Components
1. **FarmerForm** - Create new farmers with name and phone
2. **FarmerList** - List farmers, view details, delete farmers
3. **PlotForm** - Add plots to farmers with name, crop, area
4. **AdvisoryPanel** - Get agricultural recommendations for plots

### Key User Flows
- Create Farmer → Add Plots → Get Advisory
- View Farmer Details → Manage Plots (CRUD)
- Get Advisory for specific plots

### Technology Stack
- React 18.2.0 with Hooks
- Vite 5.4.21
- Axios for API calls
- CSS 3 for styling
- Backend: FastAPI with validation models

---

## 2. Functional Testing Test Cases

### 2.1 FarmerForm Component

#### TC-FF-001: Create Farmer with Valid Data
- **Steps:**
  1. Enter "John Doe" in Name field
  2. Enter "9876543210" in Phone field
  3. Click "Create Farmer" button
- **Expected:** Success message with Farmer ID displayed, form cleared

#### TC-FF-002: Create Farmer with Empty Name
- **Steps:**
  1. Leave Name field empty
  2. Click "Create Farmer" button
- **Expected:** Error message "Name is required"

#### TC-FF-003: Create Farmer with Phone Only
- **Steps:**
  1. Leave Name field empty
  2. Enter phone number
  3. Click "Create Farmer" button
- **Expected:** Error message "Name is required"

#### TC-FF-004: Create Farmer with Special Characters in Name
- **Steps:**
  1. Enter "John@Doe#123" in Name
  2. Enter phone number
  3. Click "Create Farmer" button
- **Expected:** Farmer created successfully (special chars allowed)

#### TC-FF-005: Create Farmer with Whitespace-Only Name
- **Steps:**
  1. Enter "   " (spaces only) in Name
  2. Click "Create Farmer" button
- **Expected:** Error message "Name is required"

#### TC-FF-006: Create Farmer with Very Long Name
- **Steps:**
  1. Enter 500+ character string in Name
  2. Click "Create Farmer" button
- **Expected:** Either success or validation error (depends on backend limit)

#### TC-FF-007: Create Farmer with Invalid Phone Format
- **Steps:**
  1. Enter "John Farmer" in Name
  2. Enter "abc12345" (invalid format) in Phone
  3. Click "Create Farmer" button
- **Expected:** Farmer created (phone is optional, so invalid format may be accepted)

#### TC-FF-008: Loading State During Creation
- **Steps:**
  1. Fill in valid data
  2. Click "Create Farmer" button
  3. Observe button and input states
- **Expected:** Button shows "Creating...", inputs disabled, no double-click possible

#### TC-FF-009: Success Message Auto-Clear
- **Steps:**
  1. Create a farmer successfully
  2. Wait 5 seconds
- **Expected:** Success message disappears after 5 seconds

#### TC-FF-010: Error Message Display
- **Steps:**
  1. Attempt invalid creation
  2. Observe error message
- **Expected:** Error message displayed in alert box, doesn't auto-clear

---

### 2.2 FarmerList Component

#### TC-FL-001: Load Farmers List on Mount
- **Steps:**
  1. Open application
  2. Scroll to "Farmers List" section
- **Expected:** List of farmers loaded and displayed

#### TC-FL-002: Refresh Farmers List
- **Steps:**
  1. Click "Refresh" button
- **Expected:** List reloads, shows current farmers

#### TC-FL-003: View Farmer Details
- **Steps:**
  1. Click on a farmer row
  2. Observe farmer details panel
- **Expected:** Farmer details displayed with name, phone, plots table

#### TC-FL-004: Farmer Details Include Plots
- **Steps:**
  1. Create a farmer
  2. Add a plot to the farmer
  3. Click on the farmer to view details
- **Expected:** Plots are displayed in a table with columns: Plot Name, Crop, Area

#### TC-FL-005: Delete Farmer
- **Steps:**
  1. Click "Delete" button for a farmer
  2. Confirm deletion in popup
- **Expected:** Farmer removed from list, success alert shown

#### TC-FL-006: Cancel Delete Farmer
- **Steps:**
  1. Click "Delete" button
  2. Click "Cancel" in confirmation popup
- **Expected:** Farmer not deleted, list unchanged

#### TC-FL-007: Farmer Without Plots
- **Steps:**
  1. Create a farmer but don't add plots
  2. View farmer details
- **Expected:** Empty plots table or "No plots" message

#### TC-FL-008: Empty Farmers List Message
- **Steps:**
  1. Create scenario with no farmers
  2. View Farmers List
- **Expected:** Message "No farmers yet. Create one above!"

#### TC-FL-009: Error Loading Farmers
- **Steps:**
  1. Disconnect backend or cause API error
  2. Click "Refresh"
- **Expected:** Error message displayed

#### TC-FL-010: Multiple Farmers Display
- **Steps:**
  1. Create 5+ farmers
  2. Verify all display in list
- **Expected:** All farmers visible, scrollable if needed

---

### 2.3 PlotForm Component

#### TC-PF-001: Add Plot with Valid Data
- **Steps:**
  1. Create a farmer
  2. View farmer details
  3. Enter plot name: "North Field"
  4. Enter crop: "Wheat"
  5. Enter area: "5"
  6. Click "Add Plot" button
- **Expected:** Plot added, success message shown, FarmerList refreshes with new plot

#### TC-PF-002: Add Plot Without Selecting Farmer
- **Steps:**
  1. Scroll to PlotForm without clicking a farmer
  2. Observe PlotForm state
- **Expected:** PlotForm disabled with message "Select a farmer to add plots"

#### TC-PF-003: Add Plot with Empty Name
- **Steps:**
  1. Select a farmer
  2. Leave Plot Name empty
  3. Enter crop and area
  4. Click "Add Plot"
- **Expected:** Error message "Plot name is required"

#### TC-PF-004: Add Plot with Empty Crop
- **Steps:**
  1. Select a farmer
  2. Enter plot name
  3. Leave Crop empty
  4. Enter area
  5. Click "Add Plot"
- **Expected:** Error message "Crop name is required"

#### TC-PF-005: Add Plot with Zero Area
- **Steps:**
  1. Select a farmer
  2. Fill name and crop
  3. Enter "0" for area
  4. Click "Add Plot"
- **Expected:** Error message "Area must be greater than 0 hectares"

#### TC-PF-006: Add Plot with Negative Area
- **Steps:**
  1. Select a farmer
  2. Fill name and crop
  3. Enter "-5" for area
  4. Click "Add Plot"
- **Expected:** Error message "Area must be greater than 0 hectares"

#### TC-PF-007: Add Plot with Area > 10000
- **Steps:**
  1. Select a farmer
  2. Fill name and crop
  3. Enter "15000" for area
  4. Click "Add Plot"
- **Expected:** Error message "Area must be less than 10000 hectares"

#### TC-PF-008: Add Plot with Valid Area Boundary (0.1)
- **Steps:**
  1. Select a farmer
  2. Enter plot name and crop
  3. Enter "0.1" for area
  4. Click "Add Plot"
- **Expected:** Plot added successfully

#### TC-PF-009: Add Plot with Valid Area Boundary (9999)
- **Steps:**
  1. Select a farmer
  2. Enter plot name and crop
  3. Enter "9999" for area
  4. Click "Add Plot"
- **Expected:** Plot added successfully

#### TC-PF-010: Add Plot Success Message Auto-Clear
- **Steps:**
  1. Add plot successfully
  2. Wait 3 seconds
- **Expected:** Success message disappears after 3 seconds

#### TC-PF-011: Delete Plot from List
- **Steps:**
  1. Select a farmer with plots
  2. Click delete button on a plot
  3. Confirm deletion
- **Expected:** Plot removed from table, success alert shown

#### TC-PF-012: Cancel Delete Plot
- **Steps:**
  1. Select a farmer with plots
  2. Click delete button on a plot
  3. Click "Cancel" in confirmation
- **Expected:** Plot not deleted, table unchanged

---

### 2.4 AdvisoryPanel Component

#### TC-AP-001: Get Advice for Valid Plot
- **Steps:**
  1. Create farmer and plot
  2. Note the Plot ID
  3. Enter Plot ID in AdvisoryPanel
  4. Click "Get Advice"
- **Expected:** Advice displayed with recommendations

#### TC-AP-002: Get Advice Without Plot ID
- **Steps:**
  1. Leave Plot ID empty
  2. Click "Get Advice"
- **Expected:** Error message "Plot ID is required"

#### TC-AP-003: Get Advice for Non-Existent Plot
- **Steps:**
  1. Enter "99999" as Plot ID
  2. Click "Get Advice"
- **Expected:** Error message (plot not found)

#### TC-AP-004: Get Advice with Symptoms
- **Steps:**
  1. Enter valid Plot ID
  2. Enter "Yellow leaves, brown spots" in Symptoms
  3. Click "Get Advice"
- **Expected:** Advice displayed, symptoms considered

#### TC-AP-005: Get Advice Without Symptoms
- **Steps:**
  1. Enter valid Plot ID
  2. Leave Symptoms empty
  3. Click "Get Advice"
- **Expected:** Advice displayed with default/general recommendations

#### TC-AP-006: Loading State During Advice Retrieval
- **Steps:**
  1. Enter a slow API request (or simulate)
  2. Observe button state
- **Expected:** Button shows "Getting advice...", disabled

#### TC-AP-007: Clear Previous Advice
- **Steps:**
  1. Get advice for Plot 1
  2. Change Plot ID to Plot 2
  3. Click "Get Advice"
- **Expected:** Previous advice cleared, new advice shown

#### TC-AP-008: Long Symptoms Text
- **Steps:**
  1. Enter 500+ character symptoms
  2. Click "Get Advice"
- **Expected:** Symptoms accepted and processed

---

## 3. UI/UX Testing

### Layout & Design
- [ ] Header displays correctly with gradient background
- [ ] All sections properly spaced with 30px margins
- [ ] Footer at bottom with dark background
- [ ] Form containers have white background with shadow
- [ ] Colors match design: primary (#2d7a3e), secondary (#f39c12), error (#e74c3c)
- [ ] Typography: consistent fonts, sizes, weights

### Forms & Inputs
- [ ] Input fields have proper focus states (border color, shadow)
- [ ] Labels are above inputs, properly sized
- [ ] Placeholder text visible and helpful
- [ ] Buttons have hover states with transform and shadow
- [ ] Disabled buttons show reduced opacity

### Messages & Alerts
- [ ] Error messages in red alert boxes
- [ ] Success messages in green alert boxes
- [ ] Error messages include field names and validation details
- [ ] Alerts properly styled with padding and border radius

### Navigation & Interactions
- [ ] Form submission works with Enter key
- [ ] Tab order makes sense for accessibility
- [ ] Buttons have clear visual feedback (hover, disabled)
- [ ] Loading states clear to user

---

## 4. Responsive Testing

### Desktop (1920x1080)
- [ ] All sections displayed side-by-side or stacked
- [ ] Maximum width constraint (1200px) respected
- [ ] No horizontal scrolling needed
- [ ] Proper margins and padding

### Tablet (768x1024)
- [ ] Forms stack properly
- [ ] Tables remaining readable
- [ ] Touch targets adequate (min 44px)
- [ ] No text overflow

### Mobile (375x667)
- [ ] Single column layout
- [ ] Full width forms (with padding)
- [ ] Tables scroll horizontally if needed
- [ ] Fonts remain readable

### Orientation Changes
- [ ] Landscape to portrait transitions smooth
- [ ] Layout reflows without content loss
- [ ] No overlapping elements

---

## 5. Cross-Browser Testing

- [ ] **Chrome**: All features, no console errors
- [ ] **Firefox**: All features, no console errors
- [ ] **Edge**: All features, no console errors
- [ ] **Safari**: All features, check CSS compatibility

---

## 6. Performance Testing

- [ ] Page load time < 3 seconds
- [ ] Form submission response < 1 second
- [ ] List refresh < 2 seconds
- [ ] No layout shifts (CLS)
- [ ] No memory leaks on multiple operations

---

## 7. Security Testing

- [ ] No API key exposure in localStorage
- [ ] Form inputs sanitized (no XSS)
- [ ] No sensitive data in console logs
- [ ] CORS headers properly configured
- [ ] No credentials in request body

---

## 8. Accessibility Testing

- [ ] Semantic HTML (form, button, label tags)
- [ ] All buttons and inputs have labels
- [ ] Keyboard navigation works (Tab, Enter, Esc)
- [ ] Color contrast sufficient (WCAG AA)
- [ ] Focus indicators visible
- [ ] Error messages associated with fields
- [ ] Loading states announced

---

## 9. Test Execution Summary

| Section | Test Cases | Passed | Failed | Notes |
|---------|-----------|--------|--------|-------|
| FarmerForm | 10 | | | |
| FarmerList | 10 | | | |
| PlotForm | 12 | | | |
| AdvisoryPanel | 8 | | | |
| UI/UX | 20 | | | |
| Responsive | 15 | | | |
| Cross-Browser | 4 | | | |
| Performance | 5 | | | |
| Security | 5 | | | |
| Accessibility | 7 | | | |
| **TOTAL** | **96** | | | |

---

## 10. Known Issues & Recommendations

(To be filled during testing)

---

## 11. Release Recommendation

- [ ] Ready for QA sign-off
- [ ] Ready for staging
- [ ] Ready for production
