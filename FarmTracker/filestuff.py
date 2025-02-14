import os
from mods_base import SETTINGS_DIR #type: ignore

def initFarmTracker() -> None:
    if not os.path.exists(f"{SETTINGS_DIR}\\FarmTracker"):
        os.makedirs(f"{SETTINGS_DIR}\\FarmTracker")

    if not os.path.exists(f"{SETTINGS_DIR}\\FarmTracker\\Farms"):
        os.makedirs(f"{SETTINGS_DIR}\\FarmTracker\\Farms")

    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\AutoLoad.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\AutoLoad.txt", "+a")
        file.write("None")
        file.close()
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\FarmName.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\FarmName.txt", "+a")
        file.write("No Farm Selected")
        file.close()
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyWithCount.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyWithCount.txt", "+a")
        file.write("None")
        file.close()
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyKills.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyKills.txt", "+a")
        file.write("0")
        file.close()
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemWithCount.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemWithCount.txt", "+a")
        file.write("None")
        file.close()
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemCount.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemCount.txt", "+a")
        file.write("0")
        file.close()
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\PearlCount.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\PearlCount.txt", "+a")
        file.write("0")
        file.close()
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCount.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCount.txt", "+a")
        file.write("0")
        file.close()
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\PearlCountWithText.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\PearlCountWithText.txt", "+a")
        file.write("Pearl Drops: 0")
        file.close()
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCountWithText.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCountWithText.txt", "+a")
        file.write("Legendary Drops: 0")
        file.close()
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\TrackedObjectCount.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\TrackedObjectCount.txt", "+a")
        file.write("0")
        file.close()
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\FarmNameAndTrackedObjectCount.txt"):
        file = open(f"{SETTINGS_DIR}\\FarmTracker\\FarmNameAndTrackedObjectCount.txt", "+a")
        file.write("None: 0")
        file.close()
    return None

def setValue(file: str, value: int) -> None:
    fileobj = open(file, "+r")
    fileobj.seek(0)
    fileobj.write(str(value))
    fileobj.truncate()
    fileobj.close()
    return None

def setValuestr(file: str, value: str) -> None:
    fileobj = open(file, "+r")
    fileobj.seek(0)
    fileobj.write(str(value))
    fileobj.truncate()
    fileobj.close()
    return None

def getValuestr(file: str) -> str:
    fileobj = open(file, "+r")
    data = fileobj.read()
    fileobj.close()
    return data