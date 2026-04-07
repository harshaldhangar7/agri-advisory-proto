# Manual QA Testing Checklist - Agri Advisory Prototype

**Date:** April 7, 2026  
**Tester:** Senior QA Engineer  
**Frontend URL:** http://localhost:5174  
**Backend URL:** http://localhost:8000/api  
**Status:** In Progress ✓

---

## 🧪 TEST EXECUTION TRACKING

### FarmerForm Tests

#### ✅ TC-FF-001: Create Farmer with Valid Data
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Navigate to "Create Farmer" section
2. Enter Name: "Rajesh Kumar"
3. Enter Phone: "9876543210"  
4. Click "Create Farmer" button
5. Observe success message and form reset

**Expected Result:**
- Success message: "✓ Farmer created! ID: {id}"
- Form fields cleared
- New farmer visible in Farmers List after refresh

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FF-002: Create Farmer with Empty Name
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Leave Name field empty
2. Enter Phone: "9876543210"
3. Click "Create Farmer" button

**Expected Result:**
- Error alert: "Name is required"
- Form not submitted
- No API call made

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FF-003: Create Farmer with Phone Only
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Leave Name field empty
2. Enter Phone: "9876543210"
3. Click "Create Farmer" button

**Expected Result:**
- Error alert: "Name is required"
- Form not submitted

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FF-004: Create Farmer with Special Characters
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Enter Name: "John@Doe#123"
2. Enter Phone: "9876543210"
3. Click "Create Farmer" button

**Expected Result:**
- Farmer created successfully (special chars allowed)
- Success message shown
- Farmer in list

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FF-005: Create Farmer with Whitespace-Only Name
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Enter Name: "   " (spaces only)
2. Click "Create Farmer" button

**Expected Result:**
- Error alert: "Name is required"
- Form not submitted

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FF-006: Create Farmer with Very Long Name (500+ chars)
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Copy 500+ character string
2. Paste into Name field
3. Click "Create Farmer" button

**Expected Result:**
- Either success OR validation error (depends on backend limit)
- No system errors or crashes

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FF-007: Create Farmer with Invalid Phone Format
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Enter Name: "John Farmer"
2. Enter Phone: "abc12345"
3. Click "Create Farmer" button

**Expected Result:**
- Farmer created (phone is optional, invalid format may be accepted)
- Phone stored as-is or error message shown

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FF-008: Loading State During Creation
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Enter Name: "Loading Test"
2. Enter Phone: "9876543210"
3. Click "Create Farmer" button
4. Immediately observe button and inputs

**Expected Result:**
- Button text changes to "Creating..."
- Button is disabled
- Name and Phone inputs are disabled
- No double-click possible
- Loading state lasts 1-3 seconds

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FF-009: Success Message Auto-Clear (5 seconds)
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Create a farmer successfully
2. Note success message appears
3. Wait 5 seconds
4. Observe if message disappears

**Expected Result:**
- Success message visible for ~5 seconds
- Auto-clears without user action
- User can create another farmer immediately after

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FF-010: Error Message Persistence
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Attempt invalid farmer creation (empty name)
2. Observe error message
3. Wait 10 seconds

**Expected Result:**
- Error message stays visible
- Does not auto-clear
- User must manually create new entry

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

---

### FarmerList Tests

#### ✅ TC-FL-001: Load Farmers List on Mount
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Open application
2. Scroll to "Farmers List" section
3. Observe list content

**Expected Result:**
- List displays
- Refresh button visible
- List populated if farmers exist
- "No farmers yet" message if empty

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FL-002: Refresh Farmers List
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Click "Refresh" button
2. Observe loading state
3. Wait for completion

**Expected Result:**
- Button shows "Loading..."
- Button disabled during refresh
- List updates with current farmers
- Takes 1-2 seconds

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FL-003: View Farmer Details
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Click on a farmer row in the list
2. Observe farmer details section

**Expected Result:**
- Farmer name displayed
- Phone displayed (if available)
- Plots table shown
- Delete button visible

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FL-004: Farmer Details Include Plots
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Create a farmer
2. Add a plot to the farmer
3. Click on the farmer row
4. View farmer details

**Expected Result:**
- Plots table visible
- Columns: Plot Name, Crop, Area
- New plot displays in table
- Delete button available for each plot

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FL-005: Delete Farmer with Confirmation
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Click "Delete" button for a farmer
2. Confirm in popup dialog
3. Observe list update

**Expected Result:**
- Confirmation popup: "Are you sure?"
- Farmer removed from list after confirm
- Success alert shown
- Browser alert: "Farmer deleted successfully"

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FL-006: Cancel Delete Farmer
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Click "Delete" button for a farmer
2. Click "Cancel" in confirmation
3. Observe list

**Expected Result:**
- Farmer remains in list
- No API call made
- List unchanged

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FL-007: Farmer Without Plots
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Create a farmer without adding plots
2. View farmer details
3. Observe plots section

**Expected Result:**
- Empty plots table OR "No plots" message
- Plot form still available for adding

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FL-008: Empty Farmers List
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Delete all farmers (or start fresh)
2. View Farmers List
3. Observe empty state

**Expected Result:**
- Message: "No farmers yet. Create one above!"
- Refresh button still works
- No errors

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FL-009: Error Loading Farmers
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. (Simulate) Stop backend or cause network error
2. Click "Refresh" button
3. Observe error message

**Expected Result:**
- Error message displayed
- Clear indication of what went wrong
- Can retry with Refresh

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-FL-010: Multiple Farmers Display
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Create 5+ farmers
2. View Farmers List
3. Verify all display

**Expected Result:**
- All farmers visible in list
- Scrollable if many entries
- Each farmer clickable
- No rendering issues

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

---

### PlotForm Tests

#### ✅ TC-PF-001: Add Plot with Valid Data
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Create a farmer
2. Click on farmer to view details
3. Enter Plot Name: "North Field"
4. Enter Crop: "Wheat"
5. Enter Area: "5.5"
6. Click "Add Plot" button

**Expected Result:**
- Success message: "✓ Plot "North Field" added successfully!"
- Form cleared
- Plots table refreshes with new plot
- Message auto-clears in 3 seconds

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-PF-002: Add Plot Without Selecting Farmer
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Don't select any farmer
2. Scroll to PlotForm section
3. Observe form state

**Expected Result:**
- PlotForm appears disabled/greyed out (opacity 0.5)
- Message: "Select a farmer to add plots"
- All inputs disabled
- Button disabled or hidden

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-PF-003: Add Plot with Empty Name
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Select a farmer
2. Leave Plot Name empty
3. Enter Crop: "Wheat"
4. Enter Area: "5"
5. Click "Add Plot"

**Expected Result:**
- Error alert: "Plot name is required"
- Form not submitted
- No API call

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-PF-004: Add Plot with Empty Crop
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Select a farmer
2. Enter Plot Name: "Field A"
3. Leave Crop empty
4. Enter Area: "5"
5. Click "Add Plot"

**Expected Result:**
- Error alert: "Crop name is required"
- Form not submitted

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-PF-005: Add Plot with Zero Area
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Select a farmer
2. Fill Plot Name and Crop
3. Enter Area: "0"
4. Click "Add Plot"

**Expected Result:**
- Error alert: "Area must be greater than 0 hectares"
- Form not submitted

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-PF-006: Add Plot with Negative Area
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Select a farmer
2. Fill Plot Name and Crop
3. Enter Area: "-5"
4. Click "Add Plot"

**Expected Result:**
- Error alert: "Area must be greater than 0 hectares"
- Form not submitted

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-PF-007: Add Plot with Area > 10000
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Select a farmer
2. Fill Plot Name and Crop
3. Enter Area: "15000"
4. Click "Add Plot"

**Expected Result:**
- Error alert: "Area must be less than 10000 hectares"
- Form not submitted

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-PF-008: Add Plot with Lower Boundary Area (0.1)
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Select a farmer
2. Fill Plot Name and Crop
3. Enter Area: "0.1"
4. Click "Add Plot"

**Expected Result:**
- Plot created successfully
- Success message shown
- Plot appears in table with area "0.1"

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-PF-009: Add Plot with Upper Boundary Area (9999)
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Select a farmer
2. Fill Plot Name and Crop
3. Enter Area: "9999"
4. Click "Add Plot"

**Expected Result:**
- Plot created successfully
- Success message shown
- Plot appears in table

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-PF-010: Plot Success Message Auto-Clear
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Add a plot successfully
2. Watch success message
3. Wait 3 seconds

**Expected Result:**
- Message visible for ~3 seconds
- Auto-clears without user action
- Form ready for next entry

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-PF-011: Delete Plot from Details
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Select a farmer with plots
2. Click delete button on a plot row
3. Confirm in popup

**Expected Result:**
- Confirmation popup shown
- Plot removed from table after confirm
- Success alert: "Plot deleted successfully"
- Table updates immediately

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-PF-012: Cancel Delete Plot
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Select a farmer with plots
2. Click delete button on a plot
3. Click "Cancel" in popup

**Expected Result:**
- Plot remains in table
- No API call made
- Table unchanged

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

---

### AdvisoryPanel Tests

#### ✅ TC-AP-001: Get Advice for Valid Plot
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Create farmer and plot
2. Note the Plot ID (e.g., "1")
3. Go to Advisory Panel
4. Enter Plot ID
5. Click "Get Advice"

**Expected Result:**
- Advice displayed with recommendations
- Clear agricultural advice shown
- Advice section visible with styled box
- Takes 1-3 seconds

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-AP-002: Get Advice Without Plot ID
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Leave Plot ID empty
2. Click "Get Advice"

**Expected Result:**
- Error alert: "Plot ID is required"
- No API call made

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-AP-003: Get Advice for Non-Existent Plot
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Enter Plot ID: "99999"
2. Click "Get Advice"

**Expected Result:**
- Error message displayed (plot not found)
- Clear error indication

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-AP-004: Get Advice with Symptoms
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Enter valid Plot ID
2. Enter Symptoms: "Yellow leaves, brown spots"
3. Click "Get Advice"

**Expected Result:**
- Advice displayed
- Recommendations consider symptoms
- Specific guidance based on symptoms

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-AP-005: Get Advice Without Symptoms
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Enter valid Plot ID
2. Leave Symptoms empty
3. Click "Get Advice"

**Expected Result:**
- Advice displayed
- General/default recommendations shown

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-AP-006: Loading State During Advice
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Enter valid Plot ID
2. Click "Get Advice"
3. Immediately observe button

**Expected Result:**
- Button shows "Getting advice..."
- Button disabled
- Input fields disabled
- Loading state 1-3 seconds

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-AP-007: Clear Previous Advice
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Get advice for Plot 1
2. Observe advice displayed
3. Change Plot ID to Plot 2
4. Click "Get Advice"

**Expected Result:**
- Previous advice cleared
- New advice displayed
- No stale data shown

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

#### ✅ TC-AP-008: Long Symptoms Text (500+ chars)
<details>
<summary>Test Details</summary>

**Step-by-Step:**
1. Enter valid Plot ID
2. Enter 500+ character symptoms
3. Click "Get Advice"

**Expected Result:**
- Symptoms accepted
- API call successful
- Advice displayed
- No truncation issues

**Actual Result:** ____________________________________________

**Status:** [ ] Pass [ ] Fail [ ] Skip

**Notes:** ___________________________________________________
</details>

---

### UI/UX Design Tests

#### ✅ UI-001: Header Design and Styling
- [ ] Header has gradient background (green)
- [ ] Title: "🌾 Agri Advisory Prototype"
- [ ] Subtitle: "Smart agriculture advisory system..."
- [ ] Text is centered
- [ ] Text is white
- [ ] Padding and spacing appropriate
- [ ] Shadow at bottom

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ UI-002: Form Container Styling
- [ ] White background
- [ ] Card-like appearance with shadow
- [ ] Proper padding (20px)
- [ ] Border radius (5px)
- [ ] Title color: primary green (#2d7a3e)
- [ ] Clean spacing between sections

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ UI-003: Input Fields Design
- [ ] Inputs have border (1px, #ddd)
- [ ] Padding 10px
- [ ] Border radius 5px
- [ ] Font size 1em
- [ ] Focus state: border color changes to green
- [ ] Focus state: shadow appears (0 0 5px rgba(45, 122, 62, 0.3))
- [ ] Labels bold above inputs

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ UI-004: Button Design
- [ ] Primary color: #2d7a3e (green)
- [ ] White text
- [ ] Padding: 10px 20px
- [ ] Border radius: 5px
- [ ] Font weight: 600
- [ ] Hover state: darker green, slight lift (transform: translateY(-2px))
- [ ] Hover state: shadow appears
- [ ] Disabled state: opacity 0.6, cursor not-allowed

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ UI-005: Button Danger Variant
- [ ] Delete buttons are red (#e74c3c)
- [ ] Hover: darker red (#c0392b)
- [ ] Same hover effects as primary button

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ UI-006: Alert Messages
- [ ] Error alerts: red background (#fadbd8)
- [ ] Error alerts: red text (#e74c3c)
- [ ] Success alerts: green background
- [ ] Success alerts: dark text
- [ ] Padding: 12px 15px
- [ ] Border radius: 5px
- [ ] Clear icons (✓, ✗)
- [ ] Proper spacing

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ UI-007: Footer Design
- [ ] Dark background (#333)
- [ ] White text
- [ ] Centered
- [ ] Padding: 20px
- [ ] Displays copyright year (2026)

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ UI-008: Color Consistency
- [ ] Primary color (#2d7a3e) used for headers, focus, and hover
- [ ] Secondary color (#f39c12) if used for accents
- [ ] Error color (#e74c3c) for delete/error messages
- [ ] Success color (#27ae60) for success messages
- [ ] Border color (#ddd) for inputs and separators

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ UI-009: Typography
- [ ] Font family: Segoe UI, Tahoma, Geneva (clean, professional)
- [ ] Body font size: 1em (16px)
- [ ] Line height: 1.6 (readable)
- [ ] Heading sizes appropriate
- [ ] Font weights consistent (600 for semibold labels, 400 for body)
- [ ] Text color: #333 (dark, readable)

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ UI-010: Layout and Spacing
- [ ] Sections have 30px margin-bottom
- [ ] Form groups have 15px margin-bottom
- [ ] Proper padding inside containers
- [ ] Content centered with max-width 1200px
- [ ] Responsive margins on smaller screens
- [ ] No horizontal scrolling on desktop

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

---

### Responsive Design Tests

#### ✅ RES-001: Desktop (1920x1080)
- [ ] All content visible without horizontal scroll
- [ ] App-main has max-width: 1200px (effective)
- [ ] No overlapping elements
- [ ] Proper spacing maintained
- [ ] Tables fully readable
- [ ] All buttons accessible

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ RES-002: Laptop (1366x768)
- [ ] No horizontal scrolling
- [ ] Content width appropriate
- [ ] Tables readable
- [ ] Form not too wide
- [ ] All elements accessible

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ RES-003: Tablet Portrait (768x1024)
- [ ] Single column layout
- [ ] Content takes full width (with padding)
- [ ] Form inputs properly sized
- [ ] Tables responsive (may scroll horizontally)
- [ ] Touch targets ≥44px
- [ ] Text readable without zoom

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ RES-004: Tablet Landscape (1024x768)
- [ ] Multiple columns if appropriate
- [ ] No overflow
- [ ] Readable without zoom
- [ ] Touch targets adequate

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ RES-005: Mobile (375x667)
- [ ] Single column layout
- [ ] Full-width forms (with padding)
- [ ] Readable without zoom
- [ ] Text size ≥14px
- [ ] Touch targets ≥44x44px
- [ ] No side scrolling
- [ ] Header readable
- [ ] Buttons easy to tap

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ RES-006: Mobile Small (320x568)
- [ ] Very readable
- [ ] All content accessible
- [ ] No overlapping
- [ ] Touch targets sufficient

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ RES-007: Orientation Change (Portrait ↔ Landscape)
- [ ] Smooth transition
- [ ] No content loss
- [ ] Layout reflows properly
- [ ] No broken elements

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

---

### Browser Compatibility Tests

#### ✅ BROWSER-001: Google Chrome (Latest)
- [ ] All features work
- [ ] No console errors
- [ ] Forms submit properly
- [ ] API calls successful
- [ ] Styling correct
- [ ] Performance acceptable

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ BROWSER-002: Mozilla Firefox (Latest)
- [ ] All features work
- [ ] No console errors
- [ ] Forms submit properly
- [ ] API calls successful
- [ ] Styling correct
- [ ] No CSS issues

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ BROWSER-003: Microsoft Edge (Latest)
- [ ] All features work
- [ ] No console errors
- [ ] Styling consistent with Chrome
- [ ] No vendor-specific issues

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ BROWSER-004: Safari (If available)
- [ ] All features work
- [ ] No console errors
- [ ] Styling correct
- [ ] Fonts render properly
- [ ] No WebKit-specific issues

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

---

### Performance Testing

#### ✅ PERF-001: Page Load Time
**Target:** < 3 seconds

- [ ] Initial page load time measured
- [ ] Time to First Contentful Paint (FCP)
- [ ] Time to Largest Contentful Paint (LCP)
- [ ] All resources loaded

**Measurement:** _________________________ seconds  
**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ PERF-002: Form Submission Response Time
**Target:** < 1 second (excluding network)

- [ ] Create farmer response time
- [ ] Add plot response time
- [ ] Get advice response time
- [ ] No timeout issues

**Average:** _________________________ seconds  
**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ PERF-003: Farmers List Refresh
**Target:** < 2 seconds

- [ ] Time to refresh list measured
- [ ] List update smooth
- [ ] No lag or stutter

**Measurement:** _________________________ seconds  
**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ PERF-004: No Layout Shift (CLS)
- [ ] Forms don't shift when loading
- [ ] Error messages appear without layout jump
- [ ] Success messages appear smoothly
- [ ] Table updates smoothly

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ PERF-005: Memory Leaks
- [ ] Create 10 farmers (no memory leak)
- [ ] Add 50 plots (no memory leak)
- [ ] Get 10 advisories (no memory leak)
- [ ] Memory usage stable

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

---

### Security Tests

#### ✅ SEC-001: API Key Exposure
- [ ] API key not in localStorage
- [ ] API key not in sessionStorage
- [ ] API key not visible in network tab
- [ ] API key passed in headers only

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ SEC-002: Input Sanitization (XSS Prevention)
- [ ] Can enter HTML tags without injection
- [ ] Can enter quotes/special chars safely
- [ ] Script tags not executed
- [ ] No console XSS vectors

**Test:** Enter `<script>alert('xss')</script>` in inputs  
**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ SEC-003: No Sensitive Data in Console
- [ ] No passwords logged
- [ ] No API keys logged
- [ ] No sensitive user data logged
- [ ] Only errors/debug info

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ SEC-004: CORS Headers
- [ ] Backend CORS properly configured
- [ ] API accessible from frontend
- [ ] No "blocked by CORS" errors
- [ ] Credentials handled correctly

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ SEC-005: Credentials Handling
- [ ] API key not in request body
- [ ] API key in headers (x-api-key)
- [ ] No hardcoded credentials in frontend code
- [ ] Secure key management

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

---

### Accessibility Tests

#### ✅ A11Y-001: Semantic HTML
- [ ] Form tags used for forms
- [ ] Button tags for buttons  
- [ ] Input tags for inputs
- [ ] Label tags for labels
- [ ] Heading hierarchy (h1, h2, h3)

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ A11Y-002: Form Labels
- [ ] All inputs have associated labels
- [ ] Labels visible and clear
- [ ] "required" indicated
- [ ] Labels accessible

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ A11Y-003: Keyboard Navigation
- [ ] Can tab through all inputs
- [ ] Can navigate with arrow keys
- [ ] Can submit with Enter
- [ ] Focus order logical
- [ ] No keyboard traps

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ A11Y-004: Focus Indicators
- [ ] Visible focus outline on inputs
- [ ] Visible focus on buttons
- [ ] Focus style meets contrast requirements
- [ ] Users can see where focus is

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ A11Y-005: Color Contrast (WCAG AA)
- [ ] Text on background ≥4.5:1 (normal text)
- [ ] Large text ≥3:1
- [ ] Not relying on color alone
- [ ] All text readable with color-blind mode

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ A11Y-006: Screen Reader Compatibility
- [ ] Form labels announced
- [ ] Buttons announced with purpose
- [ ] Error messages announced
- [ ] Success messages announced
- [ ] Loading states communicated

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

#### ✅ A11Y-007: Error Messages
- [ ] Associated with form field
- [ ] Clear and specific
- [ ] Visible and announced
- [ ] Non-color-dependent

**Status:** [ ] Pass [ ] Fail [ ] Skip  
**Notes:** ___________________________________________________

---

## 📊 Summary

| Category | Total | Passed | Failed | Skipped | Pass % |
|----------|-------|--------|--------|---------|---------|
| FarmerForm | 10 | _ | _ | _ | __ % |
| FarmerList | 10 | _ | _ | _ | __ % |
| PlotForm | 12 | _ | _ | _ | __ % |
| AdvisoryPanel | 8 | _ | _ | _ | __ % |
| UI/UX | 10 | _ | _ | _ | __ % |
| Responsive | 7 | _ | _ | _ | __ % |
| Browser | 4 | _ | _ | _ | __ % |
| Performance | 5 | _ | _ | _ | __ % |
| Security | 5 | _ | _ | _ | __ % |
| Accessibility | 7 | _ | _ | _ | __ % |
| **TOTAL** | **78** | **_** | **_** | **_** | **__%** |

---

## 🐛 Issues Found

### Critical Issues
1. ________________________________________
2. ________________________________________

### High Priority Issues
1. ________________________________________
2. ________________________________________

### Medium Priority Issues
1. ________________________________________
2. ________________________________________

### Low Priority Issues / Recommendations
1. ________________________________________
2. ________________________________________

---

## ✅ Recommendations

- [ ] ...
- [ ] ...
- [ ] ...

---

## 📝 Sign-Off

**Tester Name:** _________________________________  
**Date:** _________________________________  
**Recommendation:** [ ] Pass [ ] Pass with Minor Issues [ ] Fail

**Notes:** _________________________________________________________________
