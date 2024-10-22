import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

# Hide the default Streamlit header and set padding
st.markdown(
    """
    <style>
    .stApp > header {display: none;}  
    .stApp > div {padding-top: 0;}    
    </style>
    """,
    unsafe_allow_html=True
)

# Function to read coordinates from a file
def read_coordinates(file):
    try:
        coordinates = pd.read_csv(file, header=None)
        if coordinates.shape[1] != 3:
            st.error("Uploaded file must contain exactly 3 columns (x, y coordinates, and a flag).")
            return None
        return coordinates
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return None

# Function to create plots based on coordinates
def create_plots(coordinates, dot_color, dot_size, page_width, page_height):
    figures = []
    fig, ax = plt.subplots(figsize=(page_width, page_height))
    ax.set_xlim(0, page_width * 100)
    ax.set_ylim(0, page_height * 100)
    ax.axis('off')  # Hide axes
    ax.invert_yaxis()  # Invert the y-axis

    last_x, last_y = 0, 0  # Start from the top-left corner

    for i in range(len(coordinates)):
        x, y, flag = coordinates.iloc[i]

        # Only draw if the flag is 1
        if flag == 1:
            # Draw line from the last point to the current point
            ax.plot([last_x, x], [last_y, y], color=dot_color, linewidth=dot_size)
            last_x, last_y = x, y
        else:
            # Reset last_x and last_y if the flag is not 1
            last_x, last_y = x, y  # This will skip drawing

    # Append and close the last figure only if it has drawn lines
    figures.append(fig) if last_x != 0 or last_y != 0 else plt.close(fig)  # Close if empty

    return figures

# Streamlit app
st.title("Smart Pen Sketcher")

# File Upload section
st.sidebar.header("File Upload Options")
uploaded_file = st.sidebar.file_uploader("Choose a file with x,y,flag coordinates", type=["csv", "txt"])

coordinates_data = None

if uploaded_file is not None:
    coordinates_data = read_coordinates(uploaded_file)

# Settings Section
if coordinates_data is not None:
    st.sidebar.header("Settings")
    with st.sidebar.expander("Plot Settings", expanded=True):
        dot_color = st.color_picker("Choose Dot Color", "#010b13")
        dot_size = st.slider("Choose Dot Size", min_value=1, max_value=20, value=2)

        st.subheader("Choose Page Size")
        page_size_option = st.selectbox("Select Page Size", options=["A4", "Letter", "Custom"])

        standard_sizes = {
            "A4": (8.268, 11.693),
            "Letter": (8.5, 11)
        }

        if page_size_option in standard_sizes:
            page_width, page_height = standard_sizes[page_size_option]
        else:
            page_width = st.number_input("Page Width (inches)", value=8.268, min_value=0.1)
            page_height = st.number_input("Page Height (inches)", value=11.693, min_value=0.1)

    # Create plot and display it with a spinner
    with st.spinner("Creating plot... Please wait."):
        figures = create_plots(coordinates_data, dot_color, dot_size, page_width, page_height)

        for fig in figures:
            st.pyplot(fig)

        # Automatically generate the PDF when the figures are ready
        pdf_buffer = io.BytesIO()
        with PdfPages(pdf_buffer) as pdf:
            for fig in figures:
                pdf.savefig(fig)
                plt.close(fig)  # Close each figure after saving to PDF
        pdf_buffer.seek(0)  # Reset buffer position to the beginning

        # Initialize session state for PDF name if not already set
        if 'pdf_name' not in st.session_state:
            st.session_state.pdf_name = f"mno-{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Editable PDF name input
        pdf_name_input = st.sidebar.text_input("PDF File Name", st.session_state.pdf_name, key="pdf_name_input")

        # Update PDF name in session state on change
        if pdf_name_input:
            st.session_state.pdf_name = pdf_name_input.strip()

        # Store the PDF buffer in session state
        st.session_state.pdf_buffer = pdf_buffer

        # Download button for the generated PDF
        if st.session_state.pdf_buffer is not None:
            pdf_name_final = st.session_state.pdf_name.strip() or f"mno-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.sidebar.download_button(
                label="Download PDF", 
                data=st.session_state.pdf_buffer, 
                file_name=f"{pdf_name_final}.pdf",
                mime="application/pdf"
            )

# Sidebar with hover link
with st.sidebar:
    st.markdown("""
        <style>
            .hover-link {
                color: #ffffff; /* Original color */
                text-decoration: none; /* No underline */
            }
            .hover-link:hover {
                color: #c43d3e; /* Color on hover */
                text-decoration: none; /* Keep no underline on hover */
            }
            .hover-container {
                background-color: #0e1117;
                border-radius: 10px;
                padding: 10px;
            }
        </style>
        <div class='hover-container'>
            <strong>🔗 <a href='https://github.com/nomanyousafnomi/mno-smartpensketcher' class='hover-link'>MNO-SmartPenSketcher</a></strong>
        </div>
    """, unsafe_allow_html=True)
