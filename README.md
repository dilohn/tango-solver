# Tango Puzzle Solver

This project detects and solves 6x6 Tango puzzles from images. It uses OpenCV for visual processing and constraint-based logic to deduce valid solutions based on cell contents and relationship markers.

## Features

- Detects "C" and "M" markers using color recognition.
- Identifies "equals" (=) and "excludes" (X) constraints between adjacent cells via template matching.
- Enforces no-three-in-a-row and balancing constraints for valid logical deduction.
- Overlays the final solution onto the original puzzle image.

## Files

- `main.py`: Main script to process the puzzle image, run the solver, and print the solution.
- `read_board.py`: Handles image parsing, color and symbol detection, and constraint extraction.
- `tango_algo.py`: Contains the logic solver implementing constraint propagation and backtracking.
- `overlay_solution.py`: Writes the solution on top of the puzzle image for visualization.
- `puzzle.png`: Input image containing the puzzle to solve.
- `detections.png`: Debug image showing detected symbols and constraints.
- `filled.png`: Final output image with the solution filled in.
- `x_template.png`: Template for detecting the "X" constraint.
- `equals_template.png`: Template for detecting the "=" constraint.

## Requirements

Make sure you have the following installed:

- Python 3.x
- OpenCV (`opencv-python`)
- NumPy (`numpy`)

## Example

![puzzle](https://github.com/user-attachments/assets/aa786bb4-45fb-4697-b9e1-8ae5e0c6b456)
![detections](https://github.com/user-attachments/assets/baa018f5-5f58-413f-82f3-24a889730f78)
![filled](https://github.com/user-attachments/assets/6263f7dc-545e-4705-80b1-cf7fa26ff31b)

