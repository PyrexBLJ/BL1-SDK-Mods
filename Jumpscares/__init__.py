import unrealsdk
from mods_base import get_pc, build_mod, hook, SpinnerOption
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction, WeakPointer
from typing import Any
import time
import random

lastCheckTime: float = 0
jumpscares: list[str] = ["Random", "Foxy", "Gnome", "Cat", "Top5", "Rick", "Pipe", "Tube"]

selectedJumpscare: SpinnerOption = SpinnerOption("Jumpscare To Play: ", "Random", jumpscares)

@hook('Engine.GameViewportClient:Tick', Type.POST)
def HorribleTickHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    global lastCheckTime, jumpscares
    if time.time() >= lastCheckTime + 1:
        lastCheckTime = time.time()
        if random.randint(1, 10000) == 67:
            if selectedJumpscare.value == "Random":
                get_pc().ClientPlayBinkMovie(random.choice(jumpscares[1:]))
            else:
                get_pc().ClientPlayBinkMovie(selectedJumpscare.value)
    return None

build_mod()