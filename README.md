# arc-color-sampler

Analyzes average BGR color along a specified image arc.

This project demonstrates how to define a circular arc on an image and calculate the average BGR color of pixels lying along that arc. It is designed to run in a headless environment, meaning it does not open any graphical windows for user interaction or display.

## How it Works

In an interactive setting, a user would typically define the arc by clicking a center point, then a point on the circumference, and finally adjusting an angle via a trackbar.

For headless operation, these user inputs are simulated by defining fixed `center_point`, `point_on_circumference`, and `sweep_angle_deg` parameters directly within the `main.py` script. The script then:

1.  Generates a synthetic test image (no external image files required).
2.  Calculates the arc's radius and start/end angles based on the simulated input.
3.  Samples pixels along the defined arc.
4.  Computes the average BGR color of the sampled pixels.
5.  Saves a visual representation of the image with the arc and its calculated average BGR color drawn on it.
6.  Prints the calculated average BGR color to the console.

## Files

-   `main.py`: The main script containing all logic, including the synthetic image generator.
-   `requirements.txt`: Lists the necessary Python packages.
-   `README.md`: This file.

## Setup and Running

1.  **Clone the repository (or save `main.py` and `requirements.txt`):**
    ```bash
    # Replace <repo_url> with the actual URL if this were a real repo
    # git clone <repo_url> 
    # cd arc-color-sampler
    ```
    If not cloning, ensure `main.py` and `requirements.txt` are in the same directory.

2.  **Install dependencies:**
    It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows: .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Run the script:**
    ```bash
    python main.py
    ```

## Output

After execution, the script will:

-   Print messages to the console detailing the simulated inputs, calculated arc properties, and the final average BGR color.
-   Generate `test_image.png`: The synthetic image used for analysis.
-   Generate `output_arc_color.png`: An image showing the original content, the defined arc (magenta), its center (white), circumference point (red), and the calculated average BGR color as text.

## Customization

To test with different arc definitions, you can modify the following lines in `main.py`:

```python
    # 2. Define arc parameters (simulating user input in a headless environment)
    center_point = (w // 2, h // 2) # e.g., (100, 100)
    point_on_circumference = (w // 2 + 50, h // 2 + 30) # e.g., (150, 100)
    sweep_angle_deg = 150 # e.g., 90 for a quarter circle, -90 for clockwise
```
Adjust these values to define different arcs on the synthetic image.