import numpy as np

class AlphaParticle:
    """
    Represents an alpha particle.
    """
    def __init__(self, initial_position, kinetic_energy_MeV=5.0, charge_state=2, initial_velocity_vector=None):
        """
        Initializes the AlphaParticle object.

        Args:
            initial_position (np.ndarray): Initial position vector (x, y, z) in meters.
            kinetic_energy_MeV (float): Kinetic energy of the alpha particle in MeV. Default is 5 MeV.
            charge_state (int): Charge state of the alpha particle (0, 1, or 2). Default is 2.
            initial_velocity_vector (np.ndarray, optional): Initial velocity vector (vx, vy, vz) in m/s.
                                                            If None, a random direction is chosen.
        """
        self.mass = 6.644657230e-27  # kg
        self.elementary_charge = 1.602176634e-19 # Coulombs
        self.charge_state = charge_state # Number of elementary charges
        self.charge = self.charge_state * self.elementary_charge # Coulombs
        self.position = np.array(initial_position, dtype=float)
        self.kinetic_energy = kinetic_energy_MeV * 1.60218e-13 # Joules

        # Calculate velocity from kinetic energy
        self.velocity_scalar = self._calculate_velocity()

        if initial_velocity_vector is None:
            # Choose a random direction for the velocity
            theta = np.random.uniform(0, 2 * np.pi)
            self.velocity_vector = np.array([self.velocity_scalar * np.cos(theta), self.velocity_scalar * np.sin(theta), 0.0])
        else:
            self.velocity_vector = np.array(initial_velocity_vector)
            # Normalize the velocity vector to match the calculated speed
            self.velocity_vector = self.velocity_vector / np.linalg.norm(self.velocity_vector) * self.velocity_scalar


    def _calculate_velocity(self):
        """Calculates the velocity vector from the kinetic energy."""
        return np.sqrt(2 * self.kinetic_energy / self.mass)

    def get_momentum(self):
        """
        Calculates the momentum vector of the alpha particle.

        Returns:
            np.ndarray: Momentum vector (px, py, pz) in kg*m/s.
        """
        return self.mass * self.velocity_vector

    @classmethod
    def from_source(cls, source_type, initial_position, initial_velocity_vector=None):
        """
        Creates an AlphaParticle object from a specified source type.
        This is a factory method.

        Args:
            source_type (str): Type of alpha source (e.g., "Am241", "Cm244").
            initial_position (np.ndarray): Initial position vector (x, y, z) in meters.
            initial_velocity_vector (np.ndarray, optional): Initial velocity vector (vx, vy, vz) in m/s.

        Returns:
            AlphaParticle: An AlphaParticle object with initial parameters set according to the source type.
        """
        if source_type == "Am241":
            # Americium-241 emits alpha particles with a kinetic energy of 5.486 MeV (main peak)
            kinetic_energy_MeV = 5.486
        elif source_type == "Cm244":
            # Curium-244 emits alpha particles with a kinetic energy of 5.805 MeV
            kinetic_energy_MeV = 5.805
        else:
            raise ValueError("Unsupported alpha source type.")

        return cls(initial_position, kinetic_energy_MeV, initial_velocity_vector=initial_velocity_vector)
