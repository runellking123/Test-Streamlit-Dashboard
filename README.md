# Simple Clearance Tracker App

A lightweight web-based student clearance tracker - no Xcode required!

## Features

### 📊 Data Display
- View all 963 student clearance records
- **Cards View**: Detailed expandable cards for each student
- **Table View**: Compact spreadsheet-style view for quick scanning
- Alphabetical sorting by default

### 🔍 Filtering & Search
- **Search**: Find students by name, ID, class code, or attributes
- **Status Filters**:
  - All Students
  - Fully Cleared
  - Pending Clearance
  - Business Office Pending
  - IT Pending
  - Financial Aid Pending
  - Residential Life Pending
- **Class Code Filter**: Filter by specific class codes (02, 04, GR, etc.)

### 📈 Sorting Options
- Name (A-Z)
- Name (Z-A)
- ID Number
- AR Balance (High to Low)
- AR Balance (Low to High)

### 📥 Data Export
- Export filtered results to CSV
- Works with any active filter or search
- Perfect for creating reports or working offline

### 📊 Statistics Dashboard
- Total students count
- Fully cleared count
- Pending clearance count
- Department-wise pending counts in sidebar

### 🎨 Visual Features
- Color-coded clearance status (✅ cleared, ❌ pending)
- Progress bars showing completion percentage
- Color-coded AR balances (red for positive, green for zero/negative)
- Department statistics at a glance

## How to Run

1. Open Terminal
2. Navigate to this folder:
   ```bash
   cd /Users/dr.runellking/Downloads/SimpleClearanceApp
   ```

3. Install dependencies (first time only):
   ```bash
   pip3 install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python3 -m streamlit run app.py
   ```

5. The app will automatically open in your web browser at http://localhost:8501

## Updating Data

To update with new clearance data:

1. Export your Excel file as `/Users/dr.runellking/Documents/Spring 2026 Clearance Data.xlsx`
2. Run this command to convert it:
   ```bash
   python3 convert_excel.py
   ```
3. Refresh your browser - new data will load automatically

## Benefits Over Xcode App
- ✅ No compilation needed - runs instantly
- ✅ No system freezing or crashes
- ✅ Easy to update data - just replace the JSON file
- ✅ Works on any computer with Python
- ✅ Can be shared with others easily
- ✅ Beautiful, responsive web interface
- ✅ Export capabilities
- ✅ Multiple view modes
