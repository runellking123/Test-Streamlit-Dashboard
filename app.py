import streamlit as st
import json
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Spring 2026 Clearance Tracker",
    page_icon="✅",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    # Try to load real data, fall back to sample data
    try:
        with open('clearance_data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        # Use sample data if real data doesn't exist (e.g., in deployment)
        with open('clearance_data_sample.json', 'r') as f:
            data = json.load(f)
    return pd.DataFrame(data)

# Main app
def main():
    st.title("🎓 Spring 2026 Clearance Tracker")

    # Load student data
    df = load_data()

    # Add a fully cleared column
    df['fullyCleared'] = (
        df['businessOfficeCleared'] &
        df['itCleared'] &
        df['financialAidCleared'] &
        df['residentialLifeCleared']
    )

    # Statistics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Students", len(df))
    with col2:
        undergrad_count = len(df[df['classCode'] != 'GR'])
        st.metric("Undergraduate", undergrad_count)
    with col3:
        grad_count = len(df[df['classCode'] == 'GR'])
        st.metric("Graduate", grad_count)
    with col4:
        cleared_count = df['fullyCleared'].sum()
        st.metric("Fully Cleared", cleared_count)
    with col5:
        pending_count = len(df) - cleared_count
        st.metric("Pending Clearance", pending_count)

    st.divider()

    # Filters in sidebar
    st.sidebar.header("Filters")

    # Reset button
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        # Clear all filter session state
        for key in ['search_text', 'status_filter', 'class_filter', 'attribute_filter', 'attribute_search', 'sort_by', 'must_be_cleared', 'must_not_be_cleared']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.sidebar.divider()

    # Initialize session state for filters if not exists
    if 'search_text' not in st.session_state:
        st.session_state.search_text = ""
    if 'status_filter' not in st.session_state:
        st.session_state.status_filter = "All Students"
    if 'class_filter' not in st.session_state:
        st.session_state.class_filter = "All"
    if 'attribute_filter' not in st.session_state:
        st.session_state.attribute_filter = "All"
    if 'attribute_search' not in st.session_state:
        st.session_state.attribute_search = ""
    if 'sort_by' not in st.session_state:
        st.session_state.sort_by = "Name (A-Z)"

    # Search box with clear hint
    search = st.sidebar.text_input("🔍 Search by Name or ID", value=st.session_state.search_text, key="search_text", help="Type to search, clear the field to reset")

    # Filter by clearance status
    status_filter = st.sidebar.selectbox(
        "Filter by Status",
        ["All Students", "Fully Cleared", "Pending Clearance",
         "Business Office Pending", "IT Pending",
         "Financial Aid Pending", "Residential Life Pending"],
        index=["All Students", "Fully Cleared", "Pending Clearance",
               "Business Office Pending", "IT Pending",
               "Financial Aid Pending", "Residential Life Pending"].index(st.session_state.status_filter),
        key="status_filter"
    )

    # Filter by class code
    class_codes = ['All'] + sorted(df['classCode'].unique().tolist())
    class_filter = st.sidebar.selectbox("Filter by Class Code", class_codes,
                                        index=class_codes.index(st.session_state.class_filter) if st.session_state.class_filter in class_codes else 0,
                                        key="class_filter")

    # Filter by student attributes
    attribute_filter = st.sidebar.selectbox(
        "Filter by Attributes",
        ["All", "Has Attributes", "No Attributes"],
        index=["All", "Has Attributes", "No Attributes"].index(st.session_state.attribute_filter),
        key="attribute_filter"
    )

    # Search within attributes
    attribute_search = st.sidebar.text_input("🔍 Search Attributes (e.g., Basketball, Soccer)", value=st.session_state.attribute_search, key="attribute_search", help="Clear the field to reset")

    # Department comparison filters
    st.sidebar.divider()
    st.sidebar.subheader("🔍 Compare Clearances")

    with st.sidebar.expander("Show students who ARE cleared for:", expanded=False):
        must_be_cleared = st.multiselect(
            "Select departments:",
            ["Business Office", "IT", "Financial Aid", "Residential Life"],
            key="must_be_cleared",
            label_visibility="collapsed"
        )

    with st.sidebar.expander("Show students who ARE NOT cleared for:", expanded=False):
        must_not_be_cleared = st.multiselect(
            "Select departments:",
            ["Business Office", "IT", "Financial Aid", "Residential Life"],
            key="must_not_be_cleared",
            label_visibility="collapsed"
        )

    # View mode
    st.sidebar.subheader("View Mode")
    view_mode = st.sidebar.radio("Display as:", ["Cards", "Table"])

    # Sort options
    st.sidebar.subheader("Sort Options")
    sort_options = ["Name (A-Z)", "Name (Z-A)", "ID Number", "AR Balance (High to Low)", "AR Balance (Low to High)"]
    sort_by = st.sidebar.radio(
        "Sort by:",
        sort_options,
        index=sort_options.index(st.session_state.sort_by),
        key="sort_by"
    )

    # Department stats in sidebar
    st.sidebar.divider()
    st.sidebar.subheader("📊 Department Statistics")
    st.sidebar.metric("Business Office Pending", (~df['businessOfficeCleared']).sum())
    st.sidebar.metric("IT Pending", (~df['itCleared']).sum())
    st.sidebar.metric("Financial Aid Pending", (~df['financialAidCleared']).sum())
    # Only count residential students for Residential Life
    res_life_pending = (~df['residentialLifeCleared'] & ~df['isCommuter']).sum()
    st.sidebar.metric("Residential Life Pending", res_life_pending)
    st.sidebar.caption(f"({df['isCommuter'].sum()} commuter students excluded)")

    # Attribute stats in sidebar
    st.sidebar.divider()
    st.sidebar.subheader("🏆 Top Student Attributes")
    students_with_attrs = (df['studentAttributes'] != '').sum()
    st.sidebar.caption(f"{students_with_attrs} students have attributes")

    # Count individual attributes (since many are combined)
    all_attrs = {}
    for attrs in df[df['studentAttributes'] != '']['studentAttributes']:
        # Split by comma to get individual attributes
        for attr in str(attrs).split(','):
            attr = attr.strip()
            if attr:
                all_attrs[attr] = all_attrs.get(attr, 0) + 1

    # Show top 5
    top_attrs = sorted(all_attrs.items(), key=lambda x: x[1], reverse=True)[:5]
    for attr, count in top_attrs:
        st.sidebar.caption(f"• {attr}: {count}")

    # Apply filters
    filtered_df = df.copy()

    # Apply search
    if search:
        filtered_df = filtered_df[
            filtered_df['fullName'].str.contains(search, case=False, na=False) |
            filtered_df['idNumber'].str.contains(search, case=False, na=False) |
            filtered_df['classCode'].str.contains(search, case=False, na=False) |
            filtered_df['studentAttributes'].str.contains(search, case=False, na=False)
        ]

    # Apply status filter
    if status_filter == "Fully Cleared":
        filtered_df = filtered_df[filtered_df['fullyCleared']]
    elif status_filter == "Pending Clearance":
        filtered_df = filtered_df[~filtered_df['fullyCleared']]
    elif status_filter == "Business Office Pending":
        filtered_df = filtered_df[~filtered_df['businessOfficeCleared']]
    elif status_filter == "IT Pending":
        filtered_df = filtered_df[~filtered_df['itCleared']]
    elif status_filter == "Financial Aid Pending":
        filtered_df = filtered_df[~filtered_df['financialAidCleared']]
    elif status_filter == "Residential Life Pending":
        # Only show residential students who are pending (exclude commuters)
        filtered_df = filtered_df[~filtered_df['residentialLifeCleared'] & ~filtered_df['isCommuter']]

    # Apply class code filter
    if class_filter != 'All':
        filtered_df = filtered_df[filtered_df['classCode'] == class_filter]

    # Apply attribute filter
    if attribute_filter == "Has Attributes":
        filtered_df = filtered_df[filtered_df['studentAttributes'] != '']
    elif attribute_filter == "No Attributes":
        filtered_df = filtered_df[filtered_df['studentAttributes'] == '']

    # Apply attribute search
    if attribute_search:
        filtered_df = filtered_df[
            filtered_df['studentAttributes'].str.contains(attribute_search, case=False, na=False)
        ]

    # Apply department comparison filters
    dept_mapping = {
        "Business Office": "businessOfficeCleared",
        "IT": "itCleared",
        "Financial Aid": "financialAidCleared",
        "Residential Life": "residentialLifeCleared"
    }

    # Filter for departments that MUST be cleared
    if must_be_cleared:
        for dept in must_be_cleared:
            column = dept_mapping[dept]
            filtered_df = filtered_df[filtered_df[column] == True]

    # Filter for departments that MUST NOT be cleared
    if must_not_be_cleared:
        for dept in must_not_be_cleared:
            column = dept_mapping[dept]
            # For Residential Life, also exclude commuters from "must not be cleared"
            if dept == "Residential Life":
                filtered_df = filtered_df[
                    (filtered_df[column] == False) & (filtered_df['isCommuter'] == False)
                ]
            else:
                filtered_df = filtered_df[filtered_df[column] == False]

    # Apply sorting
    if sort_by == "Name (A-Z)":
        filtered_df = filtered_df.sort_values('fullName')
    elif sort_by == "Name (Z-A)":
        filtered_df = filtered_df.sort_values('fullName', ascending=False)
    elif sort_by == "ID Number":
        filtered_df = filtered_df.sort_values('idNumber')
    elif sort_by == "AR Balance (High to Low)":
        filtered_df = filtered_df.sort_values('arBalance', ascending=False)
    elif sort_by == "AR Balance (Low to High)":
        filtered_df = filtered_df.sort_values('arBalance')

    # Display count and export option
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"Showing **{len(filtered_df)}** students")
    with col2:
        # Export to CSV button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Export to CSV",
            data=csv,
            file_name="clearance_data_export.csv",
            mime="text/csv"
        )

    # Display students based on view mode
    if view_mode == "Table":
        # Table view
        display_df = filtered_df[['fullName', 'idNumber', 'classCode', 'studentAttributes', 'businessOfficeCleared',
                                   'itCleared', 'financialAidCleared', 'residentialLifeCleared',
                                   'arBalance', 'fullyCleared', 'isCommuter']].copy()
        display_df.columns = ['Name', 'ID', 'Class', 'Attributes', 'Business', 'IT', 'FinAid', 'ResLife', 'AR Balance', 'Cleared', 'Commuter']

        # Format AR Balance
        display_df['AR Balance'] = display_df['AR Balance'].apply(lambda x: f"${x:,.2f}")

        # Replace True/False with emojis for clearance columns
        for col in ['Business', 'IT', 'FinAid', 'Cleared']:
            display_df[col] = display_df[col].apply(lambda x: '✅' if x else '❌')

        # Handle ResLife - show "Commuter" for commuters, otherwise show status
        display_df['ResLife'] = display_df.apply(
            lambda row: '🏠 Commuter' if row['Commuter'] else ('✅' if row['ResLife'] else '❌'),
            axis=1
        )

        # Drop the Commuter column (we don't need to show it separately)
        display_df = display_df.drop('Commuter', axis=1)

        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        # Card view (original expander view)
        for idx, student in filtered_df.iterrows():
            with st.expander(
                f"{'✅' if student['fullyCleared'] else '⚠️'} {student['fullName']} (ID: {student['idNumber']})"
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Student Information")
                    st.write(f"**ID Number:** {student['idNumber']}")
                    st.write(f"**Class Code:** {student['classCode']}")
                    st.write(f"**Status:** {student['transactionDescription']}")
                    if student['studentAttributes']:
                        st.write(f"**Attributes:** {student['studentAttributes']}")

                    # Housing information
                    if student['isCommuter']:
                        st.write(f"**Housing:** 🏠 Commuter")
                    elif student['dormBuilding'] or student['dormRoom']:
                        st.write(f"**Housing:** {student['dormBuilding']} {student['dormRoom']}")

                    balance_color = "red" if student['arBalance'] > 0 else "green"
                    st.markdown(f"**AR Balance:** <span style='color:{balance_color}'>${student['arBalance']:,.2f}</span>",
                               unsafe_allow_html=True)

                with col2:
                    st.subheader("Clearance Status")

                    # Business Office
                    status = "✅ Cleared" if student['businessOfficeCleared'] else "❌ Pending"
                    color = "green" if student['businessOfficeCleared'] else "red"
                    st.markdown(f"**Business Office:** <span style='color:{color}'>{status}</span>",
                               unsafe_allow_html=True)

                    # Information Technology
                    status = "✅ Cleared" if student['itCleared'] else "❌ Pending"
                    color = "green" if student['itCleared'] else "red"
                    st.markdown(f"**Information Technology:** <span style='color:{color}'>{status}</span>",
                               unsafe_allow_html=True)

                    # Financial Aid
                    status = "✅ Cleared" if student['financialAidCleared'] else "❌ Pending"
                    color = "green" if student['financialAidCleared'] else "red"
                    st.markdown(f"**Financial Aid:** <span style='color:{color}'>{status}</span>",
                               unsafe_allow_html=True)

                    # Residential Life (or Commuter)
                    if student['isCommuter']:
                        st.markdown(f"**Residential Life:** <span style='color:blue'>🏠 Commuter</span>",
                                   unsafe_allow_html=True)
                        cleared_for_percentage = True  # Count as cleared for percentage
                    else:
                        status = "✅ Cleared" if student['residentialLifeCleared'] else "❌ Pending"
                        color = "green" if student['residentialLifeCleared'] else "red"
                        st.markdown(f"**Residential Life:** <span style='color:{color}'>{status}</span>",
                                   unsafe_allow_html=True)
                        cleared_for_percentage = student['residentialLifeCleared']

                    # Calculate clearance percentage
                    cleared_count = sum([
                        student['businessOfficeCleared'],
                        student['itCleared'],
                        student['financialAidCleared'],
                        cleared_for_percentage
                    ])
                    percentage = (cleared_count / 4) * 100
                    st.progress(percentage / 100)
                    st.write(f"**{percentage:.0f}% Complete**")

if __name__ == "__main__":
    main()
