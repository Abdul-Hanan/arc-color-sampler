import cv2
import numpy as np
import math

# --- Synthetic Test Image Generator ---
def create_test_image(width=400, height=400):
    """Generates a synthetic image with gradients and shapes for testing."""
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Background gradient: Blue increases with Y, Red increases with X
    for y in range(height):
        img[y, :, 0] = int(255 * (y / height)) # Blue channel
    for x in range(width):
        img[:, x, 2] = int(255 * (x / width)) # Red channel

    # Add a green circle in the center
    cv2.circle(img, (width // 2, height // 2), 60, (0, 255, 0), -1) # BGR: Green

    # Add a yellow rectangle
    cv2.rectangle(img, (50, 50), (120, 120), (0, 255, 255), -1) # BGR: Yellow

    # Add a bright magenta spot
    cv2.circle(img, (width - 70, 70), 30, (255, 0, 255), -1) # BGR: Magenta

    return img

# --- Main Logic ---
def main():
    print("Arc Color Sampler running in headless mode.")

    # 1. Generate the test image
    image_filename = "test_image.png"
    original_img = create_test_image()
    cv2.imwrite(image_filename, original_img)
    print(f"Generated synthetic test image: {image_filename}")

    # Use a copy for drawing output to preserve the original for pixel sampling
    display_img = original_img.copy()
    h, w, _ = original_img.shape

    # 2. Define arc parameters (simulating user input in a headless environment)
    # These parameters mimic the "clicking two points" and "adjusting an angle trackbar"
    # Center point of the arc
    center_point = (w // 2, h // 2) # Example: center of the image
    # A point on the circumference of the arc, defines radius and initial orientation
    point_on_circumference = (w // 2 + 50, h // 2 + 30) # Example: slightly offset from center
    # The sweep angle in degrees, simulates trackbar adjustment. Can be positive (CCW) or negative (CW).
    sweep_angle_deg = 150 # Example: a 150-degree counter-clockwise arc

    print(f"Simulated Input:")
    print(f"  Center Point: {center_point}")
    print(f"  Point on Circumference: {point_on_circumference}")
    print(f"  Sweep Angle (degrees): {sweep_angle_deg}")

    # 3. Calculate arc properties
    cx, cy = center_point
    px, py = point_on_circumference

    # Radius of the arc
    radius = int(math.sqrt((px - cx)**2 + (py - cy)**2))

    if radius == 0:
        print("Error: Center point and circumference point are the same. Radius is zero, cannot define an arc.")
        return

    # Initial angle from the center to the point on circumference (in degrees)
    # math.atan2(y, x) returns angle in radians, CCW from positive x-axis, ranging from -pi to pi.
    start_angle_rad = math.atan2(py - cy, px - cx)
    start_angle_deg = math.degrees(start_angle_rad)

    # End angle of the arc
    end_angle_deg = start_angle_deg + sweep_angle_deg

    print(f"Calculated Arc Properties:")
    print(f"  Radius: {radius}")
    print(f"  Start Angle: {start_angle_deg:.2f}°")
    print(f"  End Angle: {end_angle_deg:.2f}°")

    # 4. Collect unique pixel coordinates along the arc
    arc_pixel_coords = set() # Using a set to automatically handle unique (x, y) coordinates

    # Angle step for sampling. Smaller step means more precise arc and more samples.
    angle_step_deg = 0.25 # Sample every 0.25 degrees

    # Generate angle range for iteration
    if sweep_angle_deg >= 0:
        # Counter-clockwise or zero sweep
        angles_to_iterate = np.arange(start_angle_deg, end_angle_deg + angle_step_deg, angle_step_deg)
    else:
        # Clockwise sweep
        angles_to_iterate = np.arange(start_angle_deg, end_angle_deg - angle_step_deg, -angle_step_deg)

    # Handle the specific case where sweep_angle_deg is exactly 0 or very small
    if len(angles_to_iterate) == 0 and abs(sweep_angle_deg) < angle_step_deg:
        angles_to_iterate = np.array([start_angle_deg]) # Sample just the start point if sweep is negligible

    for angle_deg in angles_to_iterate:
        angle_rad = math.radians(angle_deg)
        x = int(cx + radius * math.cos(angle_rad))
        y = int(cy + radius * math.sin(angle_rad))

        # Check if the calculated point is within image bounds
        if 0 <= x < w and 0 <= y < h:
            arc_pixel_coords.add((x, y))

    # Retrieve BGR colors for the unique sampled pixels
    sampled_colors = []
    for x, y in arc_pixel_coords:
        sampled_colors.append(original_img[y, x])

    if not sampled_colors:
        print("Warning: No pixels sampled along the arc. It might be too small or entirely outside image bounds.")
        avg_bgr = np.array([0, 0, 0]) # Default to black if no pixels are sampled
    else:
        # 5. Calculate average BGR color
        avg_bgr = np.mean(sampled_colors, axis=0).astype(int)
        print(f"Average BGR color along the arc: {avg_bgr}")

    # 6. Visualize the arc and relevant points on the display image
    # Draw center point
    cv2.circle(display_img, center_point, 5, (255, 255, 255), -1) # White circle
    cv2.putText(display_img, "C", (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Draw point on circumference
    cv2.circle(display_img, point_on_circumference, 5, (0, 0, 255), -1) # Red circle
    cv2.putText(display_img, "P", (px + 10, py + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Draw the arc itself
    # cv2.ellipse requires angles in degrees.
    # The 'angle' parameter is the rotation of the ellipse (0 for horizontal major axis for a circle).
    # The startAngle and endAngle define the arc segment.
    cv2.ellipse(display_img, center_point, (radius, radius), 0, start_angle_deg, end_angle_deg, (255, 0, 255), 2) # Magenta arc

    # Add text for the calculated average color
    # Choose text color for visibility: white on dark background, black on light background
    luminance = 0.299 * avg_bgr[2] + 0.587 * avg_bgr[1] + 0.114 * avg_bgr[0] # Calculate luminance for avg_bgr
    display_text_color = (255, 255, 255) if luminance < 128 else (0, 0, 0)
    avg_text = f"Avg BGR: {avg_bgr}"
    cv2.putText(display_img, avg_text, (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, display_text_color, 2)

    # 7. Save the visual output
    output_image_filename = "output_arc_color.png"
    cv2.imwrite(output_image_filename, display_img)
    print(f"Visual output image saved to: {output_image_filename}")
    print("Script finished successfully.")

if __name__ == "__main__":
    main()