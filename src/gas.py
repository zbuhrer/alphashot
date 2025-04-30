import numpy as np

class GasEnvironment:
    """
    Represents the gas environment.
    """
    def __init__(self, gas_type="Hydrogen", pressure=101325.0, temperature=293.15):  # Default: Hydrogen at 1 atm, 20C
        """
        Initializes the GasEnvironment object.

        Args:
            gas_type (str): Type of gas (e.g., "Hydrogen", "Helium").
            pressure (float): Pressure in Pascals.
            temperature (float): Temperature in Kelvin.
        """
        self.gas_type = gas_type
        self.pressure = pressure
        self.temperature = temperature

        #  Basic gas properties (can be expanded for more gases)
        if gas_type == "Hydrogen":
            self.molecular_mass = 2.016e-3  # kg/mol
            self.molecular_diameter = 2.89e-10 # meters
        elif gas_type == "Helium":
            self.molecular_mass = 4.002602e-3 # kg/mol
            self.molecular_diameter = 2.18e-10 # meters
        else:
            raise ValueError("Unsupported gas type.")


        self.boltzmann_constant = 1.380649e-23  # J/K

    def calculate_number_density(self):
         """Calculates the number density of the gas (molecules per cubic meter)."""
         return self.pressure / (self.boltzmann_constant * self.temperature)

    def calculate_mean_free_path(self):
        """Estimates the mean free path of an alpha particle in the gas (meters)."""
        number_density = self.calculate_number_density()
        # Simplified calculation - assumes alpha particle and gas molecules are similar size
        collision_cross_section = np.pi * (self.molecular_diameter**2)
        return 1 / (np.sqrt(2) * number_density * collision_cross_section)
