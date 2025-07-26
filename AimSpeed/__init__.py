import unrealsdk
from mods_base import get_pc, build_mod, hook, SliderOption, BoolOption
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any

mainMouseSens: float = 1
mainControllerXSens: float = 1
mainControllerYSens: float = 1

SensitivityModifier: SliderOption = SliderOption("Sensitivity Modifier", 1, 1, 100, 1, True)
SpeedType: BoolOption = BoolOption("Type", True, "Faster", "Slower")
SnipersOnly: BoolOption = BoolOption("Snipers Only", False, "Yes", "No")

@hook("WillowGame.WillowProfileSettings:SetProfileSettingValueIntByName", Type.POST_UNCONDITIONAL)
def updateProfileSetting(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    global mainControllerXSens, mainControllerYSens, mainMouseSens
    if args.SettingName == "ControllerSensitivityX":
        mainControllerXSens = args.NewValue
    elif args.SettingName == "ControllerSensitivityY":
        mainControllerYSens = args.NewValue
    elif args.SettingName == "MouseSensitivity":
        mainMouseSens = args.NewValue
    return None

@hook("WillowGame.WillowWeapon:SetZoomState", Type.POST_UNCONDITIONAL)
def setZoomState(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    global mainControllerXSens, mainControllerYSens, mainMouseSens
    if SnipersOnly.value == False:
        pass
    if get_pc().Pawn is not None and get_pc().Pawn.Weapon is not None:
        if SnipersOnly.value == True and "sniper_rifle" in str(get_pc().Pawn.Weapon.DefinitionData.WeaponTypeDefinition):
            pass
        if SnipersOnly.value == True and "sniper_rifle" not in str(get_pc().Pawn.Weapon.DefinitionData.WeaponTypeDefinition):
            return None
        if args.NewZoomState == 2:
            if SpeedType.value == True:
                finalValue = SensitivityModifier.value
            else:
                finalValue = SensitivityModifier.value / 100
            get_pc().PlayerInput.ControllerSensitivityX = mainControllerXSens * finalValue
            get_pc().PlayerInput.ControllerSensitivityY = mainControllerYSens * finalValue
            get_pc().PlayerInput.MouseSensitivity = mainMouseSens * finalValue
        elif args.NewZoomState == 3:
            get_pc().PlayerInput.ControllerSensitivityX = mainControllerXSens
            get_pc().PlayerInput.ControllerSensitivityY = mainControllerYSens
            get_pc().PlayerInput.MouseSensitivity = mainMouseSens
    return None

def Enable() -> None:
    global mainControllerXSens, mainControllerYSens, mainMouseSens
    mainMouseSens = get_pc().PlayerInput.MouseSensitivity
    mainControllerXSens = get_pc().PlayerInput.ControllerSensitivityX
    mainControllerYSens = get_pc().PlayerInput.ControllerSensitivityY
    return None

build_mod(on_enable=Enable, options=[SensitivityModifier, SpeedType, SnipersOnly])