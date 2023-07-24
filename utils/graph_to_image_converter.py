import cv2
import numpy as np

def convert_graph_to_cv2_image(graph, width, height, output_path, color=(0, 0, 0),
                               size=1, texts={}):
    width_threshold, height_threshold = 10, 10
    output = np.ones((width + 2 * width_threshold, height + 2 * height_threshold, 3), np.uint8) * 255

    for u, v in graph.edges:
        x1, y1 = u[0] + width_threshold, u[1] + height_threshold
        x2, y2 = v[0] + width_threshold, v[1] + height_threshold
        cv2.line(output, (x1, y1), (x2, y2), (0, 0, 0), 2)

    for x, y in graph.nodes:
        x, y = x + width_threshold, y + height_threshold
        cv2.circle(output, (x, y,), size, color, -1)

    for point, text in texts.items():
        x, y = point[0] + width_threshold, point[1] + height_threshold
        x += 20 if x < width / 3 else -100
        y += 3 if y < height / 2 else -3
        direction = 1 if y < height / 2 else -1

        for i, line in enumerate(str(text).split('\n')):
            y += (i + 1) * 12 * direction
            cv2.putText(output, line, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA, False)

    cv2.imwrite(output_path, output)
