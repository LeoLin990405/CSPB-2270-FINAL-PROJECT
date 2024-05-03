# CSPB-2270-FINAL-PROJECT
Certainly! Here's a streamlined version of the README file for your interactive radix sort visualization tool project, excluding demonstration details:

---

## Interactive Radix Sort Visualization Tool

### Project Overview
This project implements an interactive visualization tool for the Radix Sort algorithm using Python and the Tkinter library. Radix Sort is a non-comparative sorting algorithm that sorts integers by processing individual digits. Numbers are processed from the least significant digit to the most significant digit (or vice versa) using queues for each digit from 0 to 9.

### Data Structure Explanation
**Radix Sort** employs queues to collect numbers based on their current significant digit. This visualization tool demonstrates how numbers are distributed into and collected from these queues, helping users visualize the sorting process step-by-step. The tool supports both Least Significant Digit (LSD) and Most Significant Digit (MSD) radix sort methods.

### Project Structure
The project is structured as follows:
- **RadixSort.py**: Contains the main implementation of the Radix Sort algorithm and the visualization logic.
- **SortingVisualizer.py**: Handles the graphical user interface (GUI), user interactions, and integrates the Radix Sort logic with the GUI to animate the sorting process.
- **utils.py**: Includes utility functions such as generating random numbers and calculating the maximum digit length of numbers in the list.

### How to Run the Project
To run this interactive visualization tool, follow these steps:

1. **Prerequisites**:
   - Ensure Python 3 is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
   - Install Tkinter, which typically comes with the standard Python installation. If for some reason Tkinter is not installed, you can install it using pip:
     ```
     pip install tk
     ```

2. **Running the Tool**:
   - Download the project files to your local machine.
   - Open a terminal or command prompt.
   - Navigate to the project directory where `SortingVisualizer.py` is located.
   - Run the following command:
     ```
     python SortingVisualizer.py
     ```

3. **Using the Tool**:
   - Click **Generate** to create a random set of numbers.
   - Choose to start the sort using **Start LSD Sort** or **Start MSD Sort**.
   - Use the **Pause/Resume** button to pause the animation at any time and resume it.

### Conclusion
This visualization tool is designed to enhance understanding of the Radix Sort algorithm by providing an interactive and engaging way to see how the algorithm sorts a list of integers. It's educational, allowing users to control the pace of sorting and observe each step in detail.

