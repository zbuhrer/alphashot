import numpy as np

class GasEnvironment:
    """
    Represents the gas environment.
    """
    def __init__(self, gas_type="Hydrogen", pressure=101325.0, temperature=293.15, gas_composition=None):  # Default: Hydrogen at 1 atm, 20C
        """
        Initializes the GasEnvironment object.

        Args:
            gas_type (str): Type of gas (e.g., "Hydrogen", "Helium").  If gas_composition is specified, this is the primary gas.
            pressure (float): Pressure in Pascals.
            temperature (float): Temperature in Kelvin.
            gas_composition (dict, optional): Dictionary specifying the gas composition as mole fractions.
                                            For example: {"Hydrogen": 0.6, "Helium": 0.4}. Defaults to None.
        """
        self.gas_type = gas_type
        self.pressure = pressure
        self.temperature = temperature
        self.gas_composition = gas_composition if gas_composition else {gas_type: 1.0} # if None, assume pure gas

        # I'm sorry hardcoding these just made the most sense lol
        self.gas_properties = {
            "Hydrogen": {"molecular_mass": 2.016e-3, "molecular_diameter": 2.89e-10},
            "Helium": {"molecular_mass": 4.002602e-3, "molecular_diameter": 2.18e-10},
            "Deuterium": {"molecular_mass": 4.028e-3, "molecular_diameter": 2.9e-10},
            "Nitrogen": {"molecular_mass": 28.014e-3, "molecular_diameter": 3.64e-10},
            "Argon": {"molecular_mass": 39.948e-3, "molecular_diameter": 3.8e-10},
            "Xenon": {"molecular_mass": 131.29e-3, "molecular_diameter": 4.91e-10}
        }


        self.boltzmann_constant = 1.380649e-23  # J/K

    def calculate_number_density(self):
         """Calculates the number density of the gas (molecules per cubic meter)."""
         return self.pressure / (self.boltzmann_constant * self.temperature)

    def calculate_mean_free_path(self, alpha_particle_diameter=1.0e-15): # Reasonable guess for alpha particle "diameter"
        """Estimates the mean free path of an alpha particle in the gas (meters).

        Args:
            alpha_particle_diameter (float): Estimated diameter of the alpha particle (m).

        Returns:
            float: Mean free path in meters.
        """
        number_density = self.calculate_number_density()
        mean_free_path = 0.0

        for gas, fraction in self.gas_composition.items():
            if gas not in self.gas_properties:
                raise ValueError(f"Gas type '{gas}' not supported in gas_properties.")

            gas_diameter = self.gas_properties[gas]["molecular_diameter"]
            reduced_mass = (6.644657230e-27 * self.gas_properties[gas]["molecular_mass"]) / (6.644657230e-27 + self.gas_properties[gas]["molecular_mass"]) # mass of alpha particle is hardcoded here.

            # More accurate collision cross-section (hard sphere model)
            relative_diameter = (alpha_particle_diameter + gas_diameter) / 2.0
            collision_cross_section = np.pi * (relative_diameter**2)


            mean_free_path += fraction / (np.sqrt(2) * number_density * collision_cross_section)


        return 1.0 / mean_free_path # harmonic mean
