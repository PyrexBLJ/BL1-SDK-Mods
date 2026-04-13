import unrealsdk
from mods_base import build_mod, hook, get_pc, ENGINE, SpinnerOption, SliderOption
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any

WoodMagnitude: SpinnerOption = SpinnerOption("Wood Size", "69", ["69", "128"], True)
LookitDisShitVolume: SliderOption = SliderOption("Lookit Dis Shit Volume", 2.5, 0.0, 10.0, 0.1, False, description="1.25 is default")

def get_sound() -> UObject:
    cue = unrealsdk.construct_object("SoundCue", ENGINE.Outer, "Plywood_Detector_Sound_Cue", template_obj=unrealsdk.find_object("SoundCue", "BTLD_Player_Brick.Brick_OpenChest_Cue"))
    islocalplayer = unrealsdk.construct_object("SoundNodeIsLocalPlayer", ENGINE.Outer, "Plywood_Detector_Sound_IsLocal", template_obj=unrealsdk.find_object("SoundCue", "BTLD_Player_Brick.Brick_OpenChest_Cue").FirstNode)
    delay = unrealsdk.construct_object("SoundNodeDelay", ENGINE.Outer, "Plywood_Detector_Delay_Node", template_obj=unrealsdk.find_object("SoundCue", "BTLD_Player_Brick.Brick_OpenChest_Cue").FirstNode.ChildNodes[1])
    random = unrealsdk.construct_object("SoundNodeRandom", ENGINE.Outer, "Plywood_Detector_Random_Node", template_obj=unrealsdk.find_object("SoundNodeRandom", "BTLD_Player_Brick.Brick_OpenChest_Cue:SoundNodeRandom_23"))

    random.Weights[0] = 0.0
    random.Weights[1] = 1.0
    delay.ChildNodes[0] = random
    delay.DelayDuration.LookupTable[0] = 0.000000
    delay.DelayDuration.LookupTable[1] = 0.000000
    delay.DelayDuration.LookupTable[2] = 0.000000
    delay.DelayDuration.LookupTable[3] = 0.000000
    delay.DelayDuration.LookupTable[4] = 0.000000
    islocalplayer.ChildNodes[1] = delay
    cue.FirstNode = islocalplayer
    cue.VolumeMultiplier = float(LookitDisShitVolume.value)
    return cue

@hook(hook_func="WillowGame.WillowPickup:InitializeFromInventory", hook_type=Type.POST)
def detectPearl(obj: UObject, __args: WrappedStruct, __ret: Any, __func: BoundFunction) -> None:
    if "plywood" in str(obj.Inventory.GetShortHumanReadableName()).lower():
        get_pc().myHUD.GetHUDMovie().AddCriticalText(0, f"<font color = \"#773700\" size = \"{WoodMagnitude.value}\">WOOD DETECTED</font>", 5.0, get_pc().myHUD.WhiteColor, get_pc().myHUD.WPRI)
        get_pc().PlaySound(get_sound(), False)
    return None

build_mod()