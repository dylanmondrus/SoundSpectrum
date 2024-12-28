import numpy as np
import os
import time
from GUI2 import automate_gui, getSpectroPath


def fourier_analysis():
    """
    Perform Fourier analysis on the most recent spectrograph file exported to the Desktop.

    - Loads the spectrograph data from the file.
    - Computes normalized levels and their average dot product.
    - Returns the computed average dot product.

    Returns:
        float: The average dot product of the normalized levels.

    Raises:
        FileNotFoundError: If the spectrograph file is not found.
        ValueError: If the file format is invalid or data cannot be loaded.
    """
    try:
        # Get the file path from GUI2
        print("Retrieving spectrograph file path...")
        file_path = getSpectroPath()

        # Wait for the file to be created (if needed)
        time.sleep(5)

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"Spectrograph file found: {file_path}")

        # Load the spectrograph data
        print("Loading spectrograph data...")
        data = np.loadtxt(file_path, delimiter="\t", skiprows=1)  # Skip header

        # Extract frequencies and levels
        frequencies = data[:, 0]  # First column: frequencies (Hz)
        levels_db = data[:, 1]    # Second column: levels (dB)

        print("Converting levels from dB to linear scale...")
        # Convert levels from dB to linear scale
        levels_linear = 10 ** (levels_db / 10)

        print("Normalizing levels...")
        # Normalize the levels
        normalized_levels = levels_linear / np.linalg.norm(levels_linear)

        print("Computing dot products...")
        # Compute pairwise dot products
        dot_products = np.dot(normalized_levels, normalized_levels)

        print("Calculating average dot product...")
        # Compute the average dot product
        average_dot_product = dot_products / len(normalized_levels)

        print(f"Average Dot Product: {average_dot_product}")
        return average_dot_product

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error loading file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


