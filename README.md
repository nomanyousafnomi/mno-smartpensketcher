# Smart Pen Sketcher

## Overview
The Smart Pen Sketcher is a Streamlit application designed to visualize and save handwritten sketches captured by a KA8 sensor using a Teensy board. This project allows users to upload a text file containing coordinates from the KA8 sensor, which will then be plotted on the screen, resembling the original sketch. 

## Features
- Upload a text or CSV file containing x, y coordinates and a flag.
- Visualize the sketch on a customizable canvas.
- Adjust dot color and size for the visual representation.
- Download the generated plot as a PDF.

## Requirements
- Python 3.x
- Streamlit
- Pandas
- Matplotlib

## Installation
To run this application locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/nomanyousafnomi/mno-smartpensketcher.git
   cd mno-smartpensketcher
   ```

2. Install the required packages:
   ```bash
   pip install streamlit pandas matplotlib
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## How to Use
1. Ensure you have a text or CSV file containing the coordinates (x, y, flag).
2. Upload the file using the file uploader on the sidebar.
3. Adjust the plotting settings such as dot color, dot size, and page size.
4. Click the button to visualize the sketch.
5. Download the plot as a PDF if desired.

## Code Explanation
The core functionality of the app is encapsulated in the provided Python code, which includes:

- **File Reading**: Reads the uploaded file and extracts the coordinates.
- **Plotting**: Uses Matplotlib to plot the points and draw lines between them based on the flag value.
- **PDF Generation**: Creates a downloadable PDF of the plotted sketch.

## Contact
For any inquiries or issues, feel free to reach out at: [p200614@pwr.nu.edu.pk](mailto:p200614@pwr.nu.edu.pk)

## License
Copyright (c) 2024 [Noman Yousaf](https://nomanyousafnomi.me)
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
Thanks to the contributors and the open-source community for their support and resources in building this application.

---

Feel free to explore and modify the code to suit your needs!