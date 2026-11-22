import tkinter as tk
from tkinter import ttk
from collections import deque

ROADS = [
    ("Jaipur", "Bagru", 32),
    ("Bagru", "Dudu", 38),
    ("Dudu", "Kishangarh", 65),
    ("Kishangarh", "Ajmer", 30),
    ("Ajmer", "Beawar", 55),
    ("Beawar", "Sojat", 65),
    ("Sojat", "Pali", 40),
    ("Pali", "Rohat", 25),
    ("Rohat", "Jodhpur", 75),
    ("Jodhpur", "Osian", 65),
    ("Osian", "Phalodi", 115),
    ("Phalodi", "Pokaran", 105),
    ("Pokaran", "Ramdevra", 12),
    ("Ramdevra", "Jaisalmer", 120),
    ("Ajmer", "Sojat", 95),
    ("Beawar", "Pali", 85),
    ("Pali", "Jodhpur", 75),
    ("Jodhpur", "Phalodi", 140),
    ("Phalodi", "Jaisalmer", 160),
    ("Pokaran", "Jaisalmer", 110)
]

GRAPH = {}

for city1, city2, km in ROADS:
    GRAPH.setdefault(city1, []).append((city2, km))
    GRAPH.setdefault(city2, []).append((city1, km))

GRAPH["Pali"].sort(
    key=lambda x: 0 if x[0] == "Rohat" else 1
)

POSITIONS = {
    "Jaipur": (100, 100),
    "Bagru": (200, 140),
    "Dudu": (300, 180),
    "Kishangarh": (410, 220),
    "Ajmer": (510, 280),
    "Beawar": (610, 350),
    "Sojat": (720, 400),
    "Pali": (820, 450),
    "Rohat": (920, 500),
    "Jodhpur": (1020, 400),
    "Osian": (1120, 300),
    "Phalodi": (1120, 190),
    "Pokaran": (1000, 100),
    "Ramdevra": (900, 80),
    "Jaisalmer": (780, 80)
}


def make_path(parent, start, end):
    if start == end:
        return [start]

    if end not in parent:
        return []

    path = []
    city = end

    while city != start:
        path.append(city)
        city = parent[city]

    path.append(start)
    path.reverse()
    return path


def path_distance(path):
    total = 0

    for i in range(len(path) - 1):
        for nxt, km in GRAPH[path[i]]:
            if nxt == path[i + 1]:
                total += km
                break

    return total


def bfs(start, end):
    queue = deque([start])
    visited = {start}
    parent = {}
    steps = []

    while queue:
        city = queue.popleft()

        steps.append({
            "action": "VISIT",
            "city": city,
            "visited": set(visited),
            "edge": None
        })

        if city == end:
            break

        for nxt, km in GRAPH[city]:
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = city
                queue.append(nxt)

                steps.append({
                    "action": "DISCOVER",
                    "city": nxt,
                    "visited": set(visited),
                    "edge": (city, nxt)
                })

                if nxt == end:
                    return steps, make_path(parent, start, end)

    return steps, make_path(parent, start, end)


def dfs(start, end):
    visited = set()
    parent = {}
    steps = []
    found = False

    def search(city):
        nonlocal found

        visited.add(city)

        steps.append({
            "action": "VISIT",
            "city": city,
            "visited": set(visited),
            "edge": None
        })

        if city == end:
            found = True
            return

        for nxt, km in GRAPH[city]:
            if nxt not in visited and not found:
                parent[nxt] = city

                steps.append({
                    "action": "DISCOVER",
                    "city": nxt,
                    "visited": set(visited) | {nxt},
                    "edge": (city, nxt)
                })

                search(nxt)

    search(start)

    return steps, make_path(parent, start, end)


root = tk.Tk()
root.title("Rajasthan AI Route Finder")
root.geometry("1200x800")
root.minsize(900, 650)
root.configure(bg="#172033")

steps = []
path = []
step_index = 0
running = False
after_id = None
algorithm = ""

title = tk.Label(
    root,
    text="RAJASTHAN AI ROUTE FINDER",
    font=("Arial", 23, "bold"),
    bg="#172033",
    fg="white"
)
title.pack(pady=10)

subtitle = tk.Label(
    root,
    text="BFS and DFS Route Searching Visualization",
    font=("Arial", 12),
    bg="#172033",
    fg="#38bdf8"
)
subtitle.pack()

panel = tk.Frame(root, bg="#243149")
panel.pack(fill="x", padx=15, pady=10)

tk.Label(
    panel,
    text="START CITY",
    bg="#243149",
    fg="white",
    font=("Arial", 10, "bold")
).grid(row=0, column=0, padx=8, pady=10)

start_box = ttk.Combobox(
    panel,
    values=list(GRAPH.keys()),
    state="readonly",
    width=13
)
start_box.set("Pali")
start_box.grid(row=0, column=1, padx=5)

tk.Label(
    panel,
    text="DESTINATION",
    bg="#243149",
    fg="white",
    font=("Arial", 10, "bold")
).grid(row=0, column=2, padx=8)

end_box = ttk.Combobox(
    panel,
    values=list(GRAPH.keys()),
    state="readonly",
    width=13
)
end_box.set("Jodhpur")
end_box.grid(row=0, column=3, padx=5)

map_frame = tk.Frame(root)
map_frame.pack(fill="both", expand=True, padx=15, pady=5)

canvas = tk.Canvas(
    map_frame,
    bg="#f1f5f9",
    scrollregion=(0, 0, 1400, 700),
    highlightthickness=0
)

vertical_scroll = ttk.Scrollbar(
    map_frame,
    orient="vertical",
    command=canvas.yview
)

horizontal_scroll = ttk.Scrollbar(
    map_frame,
    orient="horizontal",
    command=canvas.xview
)

canvas.configure(
    yscrollcommand=vertical_scroll.set,
    xscrollcommand=horizontal_scroll.set
)

canvas.grid(row=0, column=0, sticky="nsew")
vertical_scroll.grid(row=0, column=1, sticky="ns")
horizontal_scroll.grid(row=1, column=0, sticky="ew")

map_frame.grid_rowconfigure(0, weight=1)
map_frame.grid_columnconfigure(0, weight=1)

status = tk.Label(
    root,
    text="Select BFS or DFS to start",
    font=("Arial", 12, "bold"),
    bg="#172033",
    fg="white"
)
status.pack(pady=5)

info = tk.Label(
    root,
    text="Route Distance: 0 KM",
    font=("Arial", 12, "bold"),
    bg="#172033",
    fg="#facc15"
)
info.pack()


def draw_map():
    canvas.delete("all")

    for city1, city2, km in ROADS:
        x1, y1 = POSITIONS[city1]
        x2, y2 = POSITIONS[city2]

        canvas.create_line(
            x1, y1, x2, y2,
            fill="#94a3b8",
            width=3
        )

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        canvas.create_text(
            mx, my - 10,
            text=str(km) + " km",
            fill="#334155",
            font=("Arial", 8, "bold")
        )

    for city, (x, y) in POSITIONS.items():
        color = "#2563eb"

        if city == start_box.get():
            color = "#16a34a"

        if city == end_box.get():
            color = "#dc2626"

        canvas.create_oval(
            x - 22, y - 22,
            x + 22, y + 22,
            fill=color,
            outline="white",
            width=2
        )

        canvas.create_text(
            x, y + 34,
            text=city,
            fill="#111827",
            font=("Arial", 9, "bold")
        )


def show_step():
    global step_index

    if step_index >= len(steps):
        finish()
        return

    event = steps[step_index]
    city = event["city"]

    draw_map()

    for visited_city in event["visited"]:
        x, y = POSITIONS[visited_city]

        canvas.create_oval(
            x - 22, y - 22,
            x + 22, y + 22,
            fill="#22c55e",
            outline="white",
            width=2
        )

    x, y = POSITIONS[city]

    canvas.create_oval(
        x - 24, y - 24,
        x + 24, y + 24,
        fill="#facc15",
        outline="#111827",
        width=3
    )

    edge = event["edge"]

    if edge:
        c1, c2 = edge
        x1, y1 = POSITIONS[c1]
        x2, y2 = POSITIONS[c2]

        canvas.create_line(
            x1, y1, x2, y2,
            fill="#f59e0b",
            width=5
        )

    status.config(
        text=f"{algorithm}: {event['action']} - {city}"
    )

    step_index += 1

    if step_index >= len(steps):
        finish()


def finish():
    global running, after_id

    running = False

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    draw_map()

    if not path:
        status.config(text="No route found!")
        info.config(text="Route Distance: Not Available")
        return

    for i in range(len(path) - 1):
        c1 = path[i]
        c2 = path[i + 1]

        x1, y1 = POSITIONS[c1]
        x2, y2 = POSITIONS[c2]

        canvas.create_line(
            x1, y1, x2, y2,
            fill="#ef4444",
            width=6
        )

    for city in path:
        x, y = POSITIONS[city]

        canvas.create_oval(
            x - 22, y - 22,
            x + 22, y + 22,
            fill="#ef4444",
            outline="white",
            width=2
        )

    distance = path_distance(path)

    status.config(
        text="FINAL ROUTE: " + " -> ".join(path)
    )

    info.config(
        text=f"Algorithm: {algorithm} | Total Distance: {distance} KM"
    )


def start_algorithm(name):
    global steps, path, step_index, algorithm

    pause()

    start = start_box.get()
    end = end_box.get()

    if name == "BFS":
        steps, path = bfs(start, end)
    else:
        steps, path = dfs(start, end)

    algorithm = name
    step_index = 0

    canvas.xview_moveto(0)
    canvas.yview_moveto(0)

    status.config(text=f"{name} started...")
    info.config(text="Searching route...")

    show_step()


def auto_play():
    global running, after_id

    if running or step_index >= len(steps):
        return

    running = True
    after_id = root.after(600, auto_step)


def auto_step():
    global running, after_id

    if not running:
        return

    after_id = None
    show_step()

    if running and step_index < len(steps):
        after_id = root.after(600, auto_step)


def pause():
    global running, after_id

    running = False

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None


def next_step():
    pause()
    show_step()


def reset():
    global steps, path, step_index

    pause()

    steps = []
    path = []
    step_index = 0

    canvas.xview_moveto(0)
    canvas.yview_moveto(0)

    draw_map()

    status.config(text="Select BFS or DFS to start")
    info.config(text="Route Distance: 0 KM")


buttons = tk.Frame(root, bg="#172033")
buttons.pack(pady=10)

tk.Button(
    buttons,
    text="BFS",
    command=lambda: start_algorithm("BFS"),
    bg="#2563eb",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12
).grid(row=0, column=0, padx=5)

tk.Button(
    buttons,
    text="DFS",
    command=lambda: start_algorithm("DFS"),
    bg="#7c3aed",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12
).grid(row=0, column=1, padx=5)

tk.Button(
    buttons,
    text="AUTO PLAY",
    command=auto_play,
    bg="#16a34a",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12
).grid(row=0, column=2, padx=5)

tk.Button(
    buttons,
    text="PAUSE",
    command=pause,
    bg="#ea580c",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12
).grid(row=0, column=3, padx=5)

tk.Button(
    buttons,
    text="NEXT STEP",
    command=next_step,
    bg="#0891b2",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12
).grid(row=0, column=4, padx=5)

tk.Button(
    buttons,
    text="RESET",
    command=reset,
    bg="#dc2626",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12
).grid(row=0, column=5, padx=5)

legend = tk.Label(
    root,
    text="GREEN = Visited | YELLOW = Current City | RED = Final Route",
    bg="#172033",
    fg="white",
    font=("Arial", 10, "bold")
)
legend.pack(pady=5)

draw_map()
root.mainloop()
