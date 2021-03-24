import humanize

potential_saving = 0


def track_saving(size):
    global potential_saving
    potential_saving += size


def display_potential_saving():
    global potential_saving
    print(
        f"Cleaning these packages will save {humanize.naturalsize(potential_saving * 1024)}"
    )
