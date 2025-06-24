# EVOLVE-BLOCK START
import numpy as np
from datasets import Dataset, load_from_disk
# EVOLVE-BLOCK END

def predict_concentrations(potential_sequence: list[float], current_sequence: list[float]) -> int:
    """
    Predicts unknown concentration of Fc in dpvs.
    """
# EVOLVE-BLOCK START
    # Calculate the average and standard deviation of the current sequence
    avg_current = np.mean(current_sequence)
    
    std_current = np.std(current_sequence)

    # Calculate the maximum and minimum values of the current sequence
    max_current = np.max(current_sequence)
    min_current = np.min(current_sequence)

    # Calculate the peak position and width
    peak_position = potential_sequence[np.argmax(current_sequence)]
    threshold = 0.8 * max_current
    peak_indices = np.where(current_sequence > threshold)[0]
    peak_width = potential_sequence[peak_indices[-1]] - potential_sequence[peak_indices[0]] if peak_indices.size > 0 else 0

    # Define thresholds for different concentrations based on peak characteristics
    if peak_position > 0.3:
        return 0
    elif avg_current < 1.0 or std_current < 0.2 or max_current < 1.5:
        return 100
    else:
        return 200
# EVOLVE-BLOCK END


