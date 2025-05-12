import cv2
import numpy as np


def fill_puzzle(
    image_path,
    initial_grid,
    solution_grid,
    output_path="filled.png",
    rows=6,
    cols=6,
    font=cv2.FONT_HERSHEY_SIMPLEX,
):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image '{image_path}'")
    H, W = img.shape[:2]
    cell_w, cell_h = W // cols, H // rows

    if isinstance(solution_grid, dict):
        get_val = lambda i, j: solution_grid.get((i, j))
    else:
        get_val = lambda i, j: solution_grid[i][j]

    for i in range(rows):
        for j in range(cols):
            if initial_grid[i][j] is None:
                val = get_val(i, j)
                if not val:
                    continue
                cx = j * cell_w + cell_w // 2
                cy = i * cell_h + cell_h // 2
                text = val

                scale = (cell_h * 0.5) / 30.0
                thickness = max(int(cell_h * 0.04), 1)
                (text_w, text_h), baseline = cv2.getTextSize(
                    text, font, scale, thickness
                )

                org = (int(cx - text_w / 2), int(cy + text_h / 2))

                color = (0, 255, 255) if val == "C" else (255, 0, 0)

                cv2.putText(
                    img,
                    text,
                    org,
                    font,
                    scale,
                    color,
                    thickness,
                    lineType=cv2.LINE_AA,
                )

    cv2.imwrite(output_path, img)
    return output_path
