import numpy as np

class Vane:
    """
    Represents the vane and its rotational dynamics.
    """
    def __init__(self, moment_of_inertia, width, height, damping_coefficient=0.0, coulomb_friction=0.0):
        """
        Initializes the Vane object.

        Args:
            moment_of_inertia (float): The moment of inertia of the vane (kg*m^2).
            width (float): Width of the rectangular vane (m).
            height (float): Height of the rectangular vane (m).
            damping_coefficient (float):  Viscous damping coefficient (N*m*s/rad).
            coulomb_friction (float): Constant frictional torque opposing motion (N*m).
        """
        self.moment_of_inertia = moment_of_inertia
        self.damping_coefficient = damping_coefficient
        self.coulomb_friction = coulomb_friction
        self.angle = 0.0  # Radians
        self.angular_velocity = 0.0  # Radians per second
        self.width = width
        self.height = height
        self.last_torque = 0.0 # N*m,  stores the last torque applied, useful for debugging/plotting

    def _angular_acceleration(self, torque):
        """Calculates the angular acceleration given the torque and current angular velocity."""
        # Apply viscous damping and Coulomb friction
        net_torque = torque - self.damping_coefficient * self.angular_velocity

        # Coulomb friction opposes motion
        if self.angular_velocity > 0:
            net_torque -= self.coulomb_friction
        elif self.angular_velocity < 0:
            net_torque += self.coulomb_friction


        return net_torque / self.moment_of_inertia


    def apply_torque(self, torque, dt):
        """
        Applies a torque to the vane for a given time step using Euler's method.

        Args:
            torque (float): The applied torque (N*m).
            dt (float): The time step (s).
        """
        # Calculate angular acceleration
        angular_acceleration = self._angular_acceleration(torque)

        # Update angular velocity and angle using Euler's method
        self.angular_velocity += angular_acceleration * dt
        self.angle += self.angular_velocity * dt

        # Keep angle within 0 to 2*pi
        self.angle %= (2 * np.pi)
        self.last_torque = torque


    def apply_particle_impact(self, particle, dt):
        """Applies the impact of an alpha particle to the vane."""
        # Coefficient of restitution
        e = 0.5  # Example value

        # 1. Calculate impact position (random point on the vane's surface)
        x = np.random.uniform(-self.width / 2, self.width / 2)
        y = np.random.uniform(-self.height / 2, self.height / 2)
        impact_position = np.array([x, y, 0.0])

        # 2. Calculate impulse (change in momentum)
        impulse = particle.get_momentum()

        # 3. Calculate torque (cross product of impact position and impulse)
        torque_vector = np.cross(impact_position, impulse)
        torque = torque_vector[2]  # We only care about the z-component of the torque

        #4.  Apply the impulse to update the angular momentum
        delta_angular_velocity = torque / self.moment_of_inertia
        self.angular_velocity += delta_angular_velocity

        # Account for reflection (using coefficient of restitution)
        # The change in momentum of the particle is now (1+e) * impulse, so the vane gets that much
        reflected_impulse = (1 + e) * impulse
        reflected_torque_vector = np.cross(impact_position, reflected_impulse)
        reflected_torque = reflected_torque_vector[2]
        delta_angular_velocity_reflected = reflected_torque / self.moment_of_inertia
        self.angular_velocity += delta_angular_velocity_reflected


        self.angle += self.angular_velocity * dt
        self.angle %= (2 * np.pi)  # Keep angle within 0 to 2*pi


        self.last_torque = torque


    def get_state(self):
        """
        Returns the current state of the vane.

        Returns:
            tuple: (angle, angular_velocity, angular_acceleration)
        """
        angular_acceleration = self._angular_acceleration(self.last_torque)
        return self.angle, self.angular_velocity, angular_acceleration

    def get_last_torque(self):
        """Returns the last applied torque."""
        return self.last_torque


if __name__ == '__main__':
    # Example usage
    vane = Vane(moment_of_inertia=1e-6, width=0.1, height=0.05, damping_coefficient=1e-8, coulomb_friction=1e-10)  # Example values

    # Apply a constant torque for 1 second
    torque = 1e-9  # N*m
    dt = 0.01  # s
    duration = 1.0 # s

    for _ in range(int(duration / dt)):
        vane.apply_torque(torque, dt)
        angle, angular_velocity, angular_acceleration = vane.get_state()
        print(f"Angle: {angle:.4f}, Angular Velocity: {angular_velocity:.4f}, Angular Acceleration: {angular_acceleration:.4f}")

    print("Final angle:", vane.angle)
