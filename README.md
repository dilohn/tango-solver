# Tango Puzzle Solver

This project automatically solves LinkedIn's Tango puzzle using a screenshot of the board. It detects the initial state and constraints of the puzzle from the image, solves it using a constraint satisfaction algorithm, and overlays the solution on the original image.

---

## How It Works

1. **Input**: Start with a screenshot of an empty or partially filled Tango puzzle board.
2. **Detection**: The script detects all known symbols (`C` for yellow, `M` for blue) and constraint symbols (`=` and `X`) using template matching and color detection.
3. **Solving**: A backtracking constraint solver deduces the full solution based on the detected input.
4. **Overlay**: The solution is rendered back onto the original image.

---

## Example

Start with an empty board:

![puzzle](https://github.com/user-attachments/assets/2710e2a5-de89-46ae-adbe-7010b0df9ff8)

Detect the initial pieces and constraints:

![detections](https://github.com/user-attachments/assets/8a5ba83a-7f01-43e2-ab19-ca1707847421)

Solve the puzzle and fill in the missing values:

![filled](https://github.com/user-attachments/assets/da5ce730-d961-4fe7-b15c-985d2d7b5f5d)

---

## Usage

Make sure you have the required images:

- `puzzle.png` — your puzzle screenshot
- `equals_template.png` — cropped template of the "=" constraint
- `x_template.png` — cropped template of the "X" constraint

Then run:

```bash
python main.py
