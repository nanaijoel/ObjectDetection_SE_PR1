import cv2


class Visualizer:
    def __init__(self, logger=None):
        self.color_map = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0),
            'yellow': (0, 255, 255),
            'pink': (222, 89, 176),
            'black': (0, 0, 0),
            'gray': (128, 128, 128),
            'brown': (42, 42, 165),
            'white': (255, 255, 255),
            'violet': (120, 40, 74),
        }
        self.text_color = self.color_map['black']
        self.logger = logger


    def visualize_shapes(self, frame, shapes):
        """
        visualize the given shapes
        :param frame: frame to be visualized
        :param shapes: given shapes
        :return: frame
        """
        for contour, shape, color_name in shapes:
            contour_color = self.color_map['brown']
            fill_color = self.color_map.get(color_name, self.color_map['white'])
            cv2.drawContours(frame, [contour], -1, fill_color, thickness=cv2.FILLED)
            cv2.drawContours(frame, [contour], -1, contour_color, 2)

            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.putText(frame, shape, (cX - 20, cY - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, self.text_color, 2)

        self.logger.log_shapes(shapes)

        return frame
