# Spring 2026 Clearance Tracker

A lightweight web-based student clearance tracker - no Xcode required!

## 🌐 Live Dashboard

**Access the dashboard online:** [https://institutionalresearchwiley.streamlit.app](https://institutionalresearchwiley.streamlit.app)

- No installation required
- Works on any device
- Always up-to-date with the latest data
- Share this link with anyone who needs access

## 📦 Repository

**GitHub:** [https://github.com/runellking123/Test-Streamlit-Dashboard](https://github.com/runellking123/Test-Streamlit-Dashboard)

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
  - Residential Life Pending (automatically excludes commuters)
- **Class Code Filter**: Filter by specific class codes (02, 04, GR, etc.)
- **Attribute Filters**:
  - Filter by student attributes (Athletics, Honor Society, etc.)
  - Search within attributes
- **Department Comparison**:
  - Find students cleared for specific departments
  - Find students NOT cleared for specific departments
  - Combine filters to create complex queries

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
- Total students count (Undergraduate vs Graduate breakdown)
- Fully cleared count
- Pending clearance count
- Department-wise pending counts in sidebar
- Smart commuter handling (380 commuters auto-excluded from Residential Life counts)
- Top student attributes with counts

### 🎨 Visual Features
- Color-coded clearance status (✅ cleared, ❌ pending)
- Progress bars showing completion percentage
- Color-coded AR balances (red for positive, green for zero/negative)
- Department statistics at a glance

## How to Run Locally

Want to run the dashboard on your computer instead of the cloud? Follow these steps:

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

5. The app will automatically open in your web browser at:
   - **http://localhost:8501** (or next available port)
   - Or click the Local URL shown in Terminal

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
