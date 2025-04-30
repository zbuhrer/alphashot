import numpy as np

class AlphaParticle:
    """
    Represents an alpha particle.
    """
    def __init__(self, initial_position, initial_velocity_vector):
        """
        Initializes the AlphaParticle object.

        Args:
            initial_position (np.ndarray): Initial position vector (x, y, z) in meters.
            initial_velocity_vector (np.ndarray): Initial velocity vector (vx, vy, vz) in m/s.
        """
        self.mass = 6.644657230e-27  # kg
        self.charge = 3.204353020e-19  # Coulombs (2 elementary charges)
        self.position = np.array(initial_position, dtype=float)
        self.velocity = np.array(initial_velocity_vector, dtype=float)

    def get_momentum(self):
        """
        Calculates the momentum vector of the alpha particle.

        Returns:
            np.ndarray: Momentum vector (px, py, pz) in kg*m/s.
        """
        return self.mass * self.velocity
