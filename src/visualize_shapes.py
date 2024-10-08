import cv2

color_map = {
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'yellow': (0, 255, 255),
    'violet': (255, 0, 255),
    'black': (0, 0, 0),
}

text_color = color_map['black']


def visualize_shapes(frame, shapes, logger=None):
    for contour, shape, color_name in shapes:
        contour_color = (255, 20, 147)  # Violet color for contour

        fill_color = color_map.get(color_name, (255, 255, 255))  # Default to white if color not recognized

        cv2.drawContours(frame, [contour], -1, fill_color, thickness=cv2.FILLED)
        cv2.drawContours(frame, [contour], -1, contour_color, 2)

        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv2.putText(frame, shape, (cX - 20, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)

            if logger:
                logger.log_data(shape, color_name)

    return frame
