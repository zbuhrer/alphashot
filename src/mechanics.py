import numpy as np

class Vane:
    """
    Represents the vane and its rotational dynamics.
    """
    def __init__(self, moment_of_inertia, width, height, damping_coefficient=0.0):
        """
        Initializes the Vane object.

        Args:
            moment_of_inertia (float): The moment of inertia of the vane (kg*m^2).
            width (float): Width of the rectangular vane (m).
            height (float): Height of the rectangular vane (m).
            damping_coefficient (float):  Damping coefficient representing gas friction (N*m*s/rad).
        """
        self.moment_of_inertia = moment_of_inertia
        self.damping_coefficient = damping_coefficient
        self.angle = 0.0  # Radians
        self.angular_velocity = 0.0  # Radians per second
        self.angular_acceleration = 0.0 # Radians per second squared
        self.width = width
        self.height = height

    def apply_torque(self, torque, dt):
        """
        Applies a torque to the vane for a given time step.

        Args:
            torque (float): The applied torque (N*m).
            dt (float): The time step (s).
        """
        # Calculate angular acceleration
        self.angular_acceleration = (torque - self.damping_coefficient * self.angular_velocity) / self.moment_of_inertia

        # Update angular velocity and angle using Euler's method (for now)
        self.angular_velocity += self.angular_acceleration * dt
        self.angle += self.angular_velocity * dt

        # Keep angle within 0 to 2*pi (or handle periodic boundary conditions differently)
        self.angle %= (2 * np.pi)

    def apply_particle_impact(self, particle, dt):
        """Applies the impact of an alpha particle to the vane."""
        # 1. Calculate impact position (random point on the vane's surface)
        x = np.random.uniform(-self.width / 2, self.width / 2)
        y = np.random.uniform(-self.height / 2, self.height / 2)
        impact_position = np.array([x, y, 0.0])

        # 2. Calculate impulse (change in momentum) - assuming perfectly inelastic collision
        impulse = particle.get_momentum()

        # 3. Calculate force (impulse / dt)
        force = impulse / dt

        # 4. Calculate torque (cross product of impact position and force)
        torque_vector = np.cross(impact_position, force)
        torque = torque_vector[2]  # We only care about the z-component of the torque

        # Apply the torque
        self.apply_torque(torque, dt)

    def get_state(self):
        """
        Returns the current state of the vane.

        Returns:
            tuple: (angle, angular_velocity, angular_acceleration)
        """
        return self.angle, self.angular_velocity, self.angular_acceleration


if __name__ == '__main__':
    # Example usage
    vane = Vane(moment_of_inertia=1e-6, width=0.1, height=0.05, damping_coefficient=1e-8)  # Example values

    # Apply a constant torque for 1 second
    torque = 1e-9  # N*m
    dt = 0.01  # s
    duration = 1.0 # s

    for _ in range(int(duration / dt)):
        vane.apply_torque(torque, dt)
        angle, angular_velocity, angular_acceleration = vane.get_state()
        print(f"Angle: {angle:.4f}, Angular Velocity: {angular_velocity:.4f}, Angular Acceleration: {angular_acceleration:.4f}")

    print("Final angle:", vane.angle)
