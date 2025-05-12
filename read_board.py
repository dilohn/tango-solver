import cv2
import numpy as np


def parse_puzzle(
    image_path,
    rows=6,
    cols=6,
    yellow_hsv_range=((20, 100, 100), (40, 255, 255)),
    blue_hsv_range=((90, 50, 50), (130, 255, 255)),
    circle_min_area=200,
    match_thresh=0.65,
    eq_tmpl_path="equals_template.png",
    x_tmpl_path="x_template.png",
    output_path="detections.png",
):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load '{image_path}'")
    H, W = img.shape[:2]
    cell_w, cell_h = W // cols, H // rows

    hsv_full = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray_full = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges_full = cv2.Canny(gray_full, 50, 150)

    yellow_lower = np.array(yellow_hsv_range[0])
    yellow_upper = np.array(yellow_hsv_range[1])
    blue_lower = np.array(blue_hsv_range[0])
    blue_upper = np.array(blue_hsv_range[1])

    initial = [[None for _ in range(cols)] for _ in range(rows)]
    constraints = {}
    symbol_boxes = []
    region_boxes = []

    eq_gray = cv2.imread(eq_tmpl_path, cv2.IMREAD_GRAYSCALE)
    x_gray = cv2.imread(x_tmpl_path, cv2.IMREAD_GRAYSCALE)
    eq_tmpl = cv2.Canny(eq_gray, 50, 150)
    x_tmpl = cv2.Canny(x_gray, 50, 150)
    eq_w, eq_h = eq_tmpl.shape[::-1]
    x_w, x_h = x_tmpl.shape[::-1]
    pad = max(eq_w, eq_h, x_w, x_h) // 2 + 5

    def match_symbol(region_edges, tmpl, w, h):
        h_r, w_r = region_edges.shape
        if h_r < h or w_r < w:
            return False
        res = cv2.matchTemplate(region_edges, tmpl, cv2.TM_CCOEFF_NORMED)
        if res.size == 0:
            return False
        return cv2.minMaxLoc(res)[1] >= match_thresh

    for r in range(rows):
        y0_cell = r * cell_h
        y1_cell = y0_cell + cell_h
        for c in range(cols):
            x0_cell = c * cell_w
            x1_cell = x0_cell + cell_w
            cell_hsv = hsv_full[y0_cell:y1_cell, x0_cell:x1_cell]

            mask_y = cv2.inRange(cell_hsv, yellow_lower, yellow_upper)
            cnts, _ = cv2.findContours(
                mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            for cnt in cnts:
                if cv2.contourArea(cnt) < circle_min_area:
                    continue
                peri = cv2.arcLength(cnt, True)
                circ = (
                    (4 * np.pi * cv2.contourArea(cnt) / (peri * peri))
                    if peri > 0
                    else 0
                )
                if circ > 0.6:
                    initial[r][c] = "C"
                    x, y, w_box, h_box = cv2.boundingRect(cnt)
                    symbol_boxes.append(
                        (
                            x0_cell + x,
                            y0_cell + y,
                            x0_cell + x + w_box,
                            y0_cell + y + h_box,
                            "C",
                        )
                    )
                    break
            if initial[r][c] is None:
                mask_b = cv2.inRange(cell_hsv, blue_lower, blue_upper)
                cnts, _ = cv2.findContours(
                    mask_b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )
                for cnt in cnts:
                    if cv2.contourArea(cnt) < circle_min_area:
                        continue
                    initial[r][c] = "M"
                    x, y, w_box, h_box = cv2.boundingRect(cnt)
                    symbol_boxes.append(
                        (
                            x0_cell + x,
                            y0_cell + y,
                            x0_cell + x + w_box,
                            y0_cell + y + h_box,
                            "M",
                        )
                    )
                    break

    for r in range(rows):
        y0 = r * cell_h
        y1 = y0 + cell_h
        for c in range(cols - 1):
            mid_x = (c + 1) * cell_w
            x0 = max(mid_x - pad, 0)
            x1 = min(mid_x + pad, W)
            region_edges = edges_full[y0:y1, x0:x1]
            coord = ((r, c), (r, c + 1))
            if match_symbol(region_edges, eq_tmpl, eq_w, eq_h):
                constraints[coord] = "="
                region_boxes.append((x0, y0, x1, y1, "="))
            elif match_symbol(region_edges, x_tmpl, x_w, x_h):
                constraints[coord] = "X"
                region_boxes.append((x0, y0, x1, y1, "X"))
    for r in range(rows - 1):
        mid_y = (r + 1) * cell_h
        y0 = max(mid_y - pad, 0)
        y1 = min(mid_y + pad, H)
        for c in range(cols):
            x0 = c * cell_w
            x1 = x0 + cell_w
            region_edges = edges_full[y0:y1, x0:x1]
            coord = ((r, c), (r + 1, c))
            if match_symbol(region_edges, eq_tmpl, eq_w, eq_h):
                constraints[coord] = "="
                region_boxes.append((x0, y0, x1, y1, "="))
            elif match_symbol(region_edges, x_tmpl, x_w, x_h):
                constraints[coord] = "X"
                region_boxes.append((x0, y0, x1, y1, "X"))

    vis = img.copy()
    for x0, y0, x1, y1, label in symbol_boxes:
        col = (0, 255, 255) if label == "C" else (255, 0, 0)
        cv2.rectangle(vis, (x0, y0), (x1, y1), col, 2)
    for x0, y0, x1, y1, label in region_boxes:
        col = (0, 255, 0) if label == "=" else (0, 0, 255)
        cv2.rectangle(vis, (x0, y0), (x1, y1), col, 2)
    cv2.imwrite(output_path, vis)

    return initial, constraints
