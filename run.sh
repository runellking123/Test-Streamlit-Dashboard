#!/bin/bash

echo "🎓 Starting Simple Clearance Tracker..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
fi

# Run the app
streamlit run app.py
