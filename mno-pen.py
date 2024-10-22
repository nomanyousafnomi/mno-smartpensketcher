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
        if coordinates.shape[1] != 2:
            st.error("Uploaded file must contain exactly 2 columns (x and y coordinates).")
            return None
        return coordinates
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return None

# Function to create plots based on coordinates
def create_plot(coordinates, dot_color, dot_size, page_width, page_height):
    fig, ax = plt.subplots(figsize=(page_width, page_height))
    ax.set_xlim(0, page_width * 100)
    ax.set_ylim(0, page_height * 100)
    ax.axis('off')  # Hide axes

    # Invert the y-axis
    ax.invert_yaxis()

    # Draw lines based on coordinates
    for i in range(len(coordinates) - 1):
        x1, y1 = coordinates.iloc[i]
        x2, y2 = coordinates.iloc[i + 1]
        ax.plot([x1, x2], [y1, y2], color=dot_color, linewidth=dot_size)

    return fig

# Streamlit app
st.title("Smart Pen Sketcher")

# File Upload section
st.sidebar.header("File Upload Options")
uploaded_file = st.sidebar.file_uploader("Choose a file with x,y coordinates", type=["csv", "txt"])

coordinates_data = None

if uploaded_file is not None:
    coordinates_data = read_coordinates(uploaded_file)

# Settings Section
if coordinates_data is not None:
    st.sidebar.header("Settings")
    with st.sidebar.expander("Plot Settings", expanded=True):
        dot_color = st.color_picker("Choose Dot Color", "#010b13")  # Default to 
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

    # Create plot and display it
    fig = create_plot(coordinates_data, dot_color, dot_size, page_width, page_height)
    st.pyplot(fig)

    # Automatically generate the PDF when the figure is ready
    pdf_buffer = io.BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        pdf.savefig(fig)
        plt.close(fig)
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
            <strong>🔗 <a href='https://nomanyousafnomi.me' class='hover-link'>Noman Yousaf</a></strong>
        </div>
    """, unsafe_allow_html=True)
