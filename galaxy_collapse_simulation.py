import numpy as np
import numpy.typing as npt
import tkinter as tk
from typing import Annotated, List, Optional
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
    n_arms: int = 5,
    center: Optional[Vector2D] = None,
    GM: float = 10.0,   # "гравитационный параметр" центральной массы
) -> List[Particle]:
    if center is None:
        center = np.array([0.0, 0.0], dtype=np.float64)

    particles: List[Particle] = []

    radii = np.linspace(1.0, 10.0, n_particles)

    #черная дыра
    particles.append(Particle(20, center, np.array([0,0])))
    for i in range(n_particles):
        r = radii[i]

        # базовый угол спирали
        base_angle = 0.5 * r

        # выбор рукава
        arm = i % n_arms
        arm_offset = 2.0 * np.pi * arm / n_arms

        # небольшой шум
        angle = base_angle + arm_offset + np.random.normal(scale=0.2)

        # позиция
        x = center[0] + r * np.cos(angle)
        y = center[1] + r * np.sin(angle)
        pos = np.array([x, y], dtype=np.float64)

        # направление скорости по касательной
        vx_dir = -np.sin(angle)
        vy_dir = np.cos(angle)

        # скорость для почти круговой орбиты: v ~ sqrt(GM / r)
        speed = np.sqrt(GM / r)
        vel = np.array([vx_dir * speed, vy_dir * speed], dtype=np.float64)

        mass = float(np.random.uniform(0.5, 2.0))
        particles.append(Particle(mass, pos, vel))

    return particles


# ---------------- TK + анимация ----------------

WIDTH, HEIGHT = 800, 800
SCALE = 20.0          # пикселей на единицу
DT = 0.01             # шаг времени
G = 1.0
M_central = 10.0      # центральная масса
CENTER = np.array([0.0, 0.0], dtype=np.float64)

root = tk.Tk()
root.title("Galaxy simulation")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# создаём частицы
particles = generate_spiral_galaxy(n_particles=500, GM=G * M_central)

# рисуем точки
RADIUS = 2
items: List[int] = []


for i,p in enumerate(particles):
    sx = WIDTH / 2 + p.position[0] * SCALE
    sy = HEIGHT / 2 + p.position[1] * SCALE
    item_id = canvas.create_oval(
        sx - RADIUS, sy - RADIUS, sx + RADIUS, sy + RADIUS,
        fill= "white" if i != 0 else "red" , outline=""
    )
    items.append(item_id)


def update():
    for i, p in enumerate(particles):
        # вектор от частицы к центру
        r_vec = p.position - CENTER
        r = np.linalg.norm(r_vec)

        if r > 1e-3:
            # ускорение к центру: a = -G*M * r / r^3
            a = -G * M_central * r_vec / (r ** 3)
        else:
            a = np.zeros(2, dtype=np.float64)

        # интегрирование (простая схема Эйлера)
        p.velocity = p.velocity + a * DT
        p.position = p.position + p.velocity * DT

        # в экранные координаты
        sx = WIDTH / 2 + p.position[0] * SCALE
        sy = HEIGHT / 2 + p.position[1] * SCALE

        canvas.coords(
            items[i],
            sx - RADIUS, sy - RADIUS,
            sx + RADIUS, sy + RADIUS
        )

    canvas.after(16, update)  # ~60 FPS


update()
root.mainloop()
