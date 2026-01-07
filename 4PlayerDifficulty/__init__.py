import unrealsdk #type: ignore
from mods_base import ENGINE, build_mod, hook, SliderOption #type: ignore
from unrealsdk.hooks import Type #type: ignore
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction #type: ignore
from typing import Any

FakePlayers: SliderOption = SliderOption("Number of Players", 4, 1, 4, 1, True, description="The number of players to fake in the game", on_change = lambda _, new_value: setPlayers(_, new_value))

def setPlayers(_: SliderOption, new_value: int) -> None:
    ENGINE.GetCurrentWorldInfo().Game.EffectiveNumPlayers = new_value
    return None

@hook(hook_func="WillowGame.WillowPlayerController:SpawningProcessComplete", hook_type=Type.POST)
def finishedSpawning(obj: UObject, __args: WrappedStruct, __ret: Any, __func: BoundFunction) -> None:
    ENGINE.GetCurrentWorldInfo().Game.EffectiveNumPlayers = FakePlayers.value
    return None

def Disable() -> None:
    ENGINE.GetCurrentWorldInfo().Game.EffectiveNumPlayers = ENGINE.GetCurrentWorldInfo().Game.NumPlayers
    return None

build_mod(on_disable=Disable, options=[FakePlayers])