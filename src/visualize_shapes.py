import cv2

# Define the color map globally to avoid re-creating it each time the function is called
color_map = {
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'yellow': (0, 255, 255),
    'violet': (255, 0, 255),
}


def visualize_shapes(frame, shapes):
    for contour, shape, color_name in shapes:  # Loop through each detected shape
        contour_color = (0, 0, 0)  # Black color for contour

        # Use the globally defined color_map to fill the shape with the detected color
        fill_color = color_map.get(color_name, (255, 255, 255))  # Default to white if color not recognized

        # Fill the inside of the shape with the detected color
        cv2.drawContours(frame, [contour], -1, fill_color, thickness=cv2.FILLED)

        # Draw the contour in black
        cv2.drawContours(frame, [contour], -1, contour_color, 2)

        # Calculate the centroid (center point) of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # Write the detected shape (e.g., "Square", "Circle") on the shape
            cv2.putText(frame, shape, (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, contour_color, 2)

    return frame  # Return the frame with the visualized shapes
