import unrealsdk
from mods_base import build_mod, hook, get_pc, ENGINE, SpinnerOption, SliderOption, Game
from unrealsdk.hooks import Type, add_hook, Block
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any

def DisableWeaponValidation(*_): # thanks yeti
    return Block, True

add_hook("WillowGame.WillowPlayerController:ValidateWeaponDefinition", Type.PRE, "ValidateWeaponDefinition", DisableWeaponValidation)
add_hook("WillowGame.WillowPlayerController:ValidateItemDefinition", Type.PRE, "ValidateItemDefinition", DisableWeaponValidation)

def trysetparts(partlist: str, type: str):
    if Game.get_current() == Game.BL1:
        try:
            attr = unrealsdk.find_object("WeaponPartListCollectionDefinition", partlist).__getattr__(type)
            attr.bEnabled = False
            unrealsdk.find_object("WeaponPartListCollectionDefinition", partlist).__setattr__(type, attr)
            attr = None
        except:
            pass
    if Game.get_current() == Game.BL1E:
        try:
            unrealsdk.find_object("WeaponPartListCollectionDefinition", partlist).__setattr__(type, unrealsdk.make_struct("WeaponCustomPartTypeData"))
        except:
            pass

def setHybrids() -> None:
    trysetparts("dlc3_gd_customweapons.Unique_PartCollections.PartCollection_Repeater_KnoxsGold", "AccessoryPartData")
    trysetparts("gd_customweapons.PartCollections.PartCollection_Repeater_LadiesFinger", "SightPartData")
    trysetparts("dlc3_gd_customweapons.Unique_PartCollections.PartCollection_Repeater_AthenasWisdom", "SightPartData")
    trysetparts("dlc3_gd_customweapons.Unique_PartCollections.PartCollection_SMG_Typhoon", "MagazinePartData")
    trysetparts("dlc3_gd_customweapons.Unique_PartCollections.PartCollection_SupportMG_TheChopper", "MagazinePartData")
    trysetparts("dlc3_gd_customweapons.Pearlescent_PartCollections.PartCollection_CombatShotgun_DahlJackal", "MagazinePartData")
    trysetparts("dlc3_gd_customweapons.Pearlescent_PartCollections.PartCollection_CombatRifle_TedioreAvenger", "BodyPartData")
    trysetparts("dlc3_gd_customweapons.Pearlescent_PartCollections.PartCollection_SniperRifle_JakobsBessie", "BarrelPartData")
    if Game.get_current() == Game.BL1E:
        trysetparts("gd_customweapons.Retail_PartCollections.PartCollection_repeater_TheDove", "AccessoryPartData")
    return None

@hook(hook_func="WillowGame.WillowPlayerController:SpawningProcessComplete", hook_type=Type.PRE)
def Spawn(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
    setHybrids()
    return None

def Enable() -> None:
    try:
        setHybrids()
    except:
        print("[More Hybrids] Failed to set hybrids on game load, will try again on character load.")
    return None

build_mod(on_enable=Enable)