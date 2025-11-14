import tkinter as tk
import numpy as np
from typing import Annotated, List, Optional
import numpy.typing as npt
import os

os.environ["TCL_LIBRARY"] = r"C:\Users\legop\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"]  = r"C:\Users\legop\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

Vector2D = Annotated[npt.NDArray[np.float64], (2,)]

class Particle:
    def __init__(
        self,
        initial_mass: float,
        initial_position: Vector2D,
        initial_velocity: Vector2D
    ):
        self.mass: float = initial_mass
        self.position: Vector2D = initial_position
        self.velocity: Vector2D = initial_velocity

def generate_spiral_galaxy(
    n_particles: int = 50,
    n_arms: int = 2,
    center: Optional[Vector2D] = None,
    GM: float = 10.0,
) -> List[Particle]:
    if center is None:
        center = np.array([0.0, 0.0], dtype=np.float64)

    particles: List[Particle] = []
    radii = np.linspace(1.0, 10.0, n_particles)

    for i in range(n_particles):
        r = radii[i]

        base_angle = 0.5 * r
        arm = i % n_arms
        arm_offset = 2.0 * np.pi * arm / n_arms
        angle = base_angle + arm_offset + np.random.normal(scale=0.2)

        x = center[0] + r * np.cos(angle)
        y = center[1] + r * np.sin(angle)
        pos = np.array([x, y], dtype=np.float64)

        vx_dir = -np.sin(angle)
        vy_dir = np.cos(angle)

        speed = np.sqrt(GM / r)
        vel = np.array([vx_dir * speed, vy_dir * speed], dtype=np.float64)

        mass = float(np.random.uniform(0.5, 2.0))
        particles.append(Particle(mass, pos, vel))

    return particles


# ---------- параметры симуляции ----------

WIDTH, HEIGHT = 800, 800
SCALE = 10.0
DT = 0.01

G = 1.0
M_central = 10.0
CENTER_1 = np.array([5.0, 5.0], dtype=np.float64)

# 1 симуляционная единица времени = столько лет
YEARS_PER_SIM_UNIT = 1_000.0

sim_time_years = 0.0  # "прошло лет", значит и световых лет


# ---------- TK UI ----------

root = tk.Tk()
root.title("Galaxy simulation")

main_frame = tk.Frame(root)
main_frame.pack()

canvas = tk.Canvas(main_frame, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack(side=tk.LEFT)

side_frame = tk.Frame(main_frame, bg="black")
side_frame.pack(side=tk.LEFT, fill=tk.Y)

time_label = tk.Label(
    side_frame,
    text="Свет прошёл:\n0.00 св. лет",
    fg="white",
    bg="black",
    font=("Arial", 12)
)
time_label.pack(padx=10, pady=10, anchor="n")

# ---------- частицы ----------

particles = generate_spiral_galaxy(n_particles=500, n_arms=5, center=CENTER_1, GM=G * M_central)

RADIUS = 2
items: List[int] = []

for p in particles:
    sx = WIDTH / 2 + p.position[0] * SCALE
    sy = HEIGHT / 2 + p.position[1] * SCALE
    item_id = canvas.create_oval(
        sx - RADIUS, sy - RADIUS,
        sx + RADIUS, sy + RADIUS,
        fill="white", outline=""
    )
    items.append(item_id)

# центральная "масса" (для красоты)
center_radius = 4
canvas.create_oval(
    WIDTH / 2 + CENTER_1[0]*SCALE - center_radius,
    HEIGHT / 2 + CENTER_1[0]*SCALE - center_radius,
    WIDTH / 2 + CENTER_1[1]*SCALE + center_radius,
    HEIGHT / 2 + CENTER_1[1]*SCALE + center_radius,
    fill="yellow", outline=""
)


def update():
    global sim_time_years

    for i, p in enumerate(particles):
        r_vec = p.position - CENTER_1
        r = np.linalg.norm(r_vec)

        if r > 1e-3:
            a = -G * M_central * r_vec / (r ** 3)
        else:
            a = np.zeros(2, dtype=np.float64)

        p.velocity = p.velocity + a * DT
        p.position = p.position + p.velocity * DT

        sx = WIDTH / 2 + p.position[0] * SCALE
        sy = HEIGHT / 2 + p.position[1] * SCALE

        canvas.coords(
            items[i],
            sx - RADIUS, sy - RADIUS,
            sx + RADIUS, sy + RADIUS
        )

    # обновляем "счётчик световых лет"
    sim_time_years += DT * YEARS_PER_SIM_UNIT
    time_label.config(
        text=f"Свет прошёл:\n{sim_time_years:.2f} св. лет"
    )

    canvas.after(16, update)  # ~60 FPS


update()
root.mainloop()
