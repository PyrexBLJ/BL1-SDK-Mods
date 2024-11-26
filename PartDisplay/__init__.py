import unrealsdk
from typing import TypedDict
from mods_base import keybind, EInputEvent, get_pc, build_mod, ENGINE, hook, SliderOption, SETTINGS_DIR, BoolOption, DropdownOption, NestedOption
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
import os, json

WeaponParts: BoolOption = BoolOption("Show Weapon Parts", True, "Yes", "No")
ItemParts: BoolOption = BoolOption("Show Equipable Item Parts", True, "Yes", "No")
PartR: SliderOption = SliderOption("Display R Value", 255, 0, 255, 1, True)
PartG: SliderOption = SliderOption("Display G Value", 255, 0, 255, 1, True)
PartB: SliderOption = SliderOption("Display B Value", 255, 0, 255, 1, True)
PartA: SliderOption = SliderOption("Display A Value (Transparency)", 255, 0, 255, 1, True)


def splitthestring(part: str) -> str:
    noweirdshit: str = part.replace("'", "")
    namelist: list = noweirdshit.split(".")
    return namelist[-1]

@hook(hook_func="Engine.GameViewportClient:PostRender", hook_type=Type.POST)
def render(obj: UObject, __args: WrappedStruct, __ret: any, __func: BoundFunction) -> None:
    if get_pc().CurrentSeenPickupable != None:
        __args.Canvas.Font = unrealsdk.find_object("Font", "ui_fonts.font_willowbody_18pt")
        __args.Canvas.SetPos(50, 50)
        __args.Canvas.DrawColor = unrealsdk.make_struct("Color", R=PartR.value, G=PartG.value, B=PartB.value, A=PartA.value)

        if WeaponParts.value == True:
            if "Weapon" in str(get_pc().CurrentSeenPickupable.Inventory):
                __args.Canvas.DrawText(f"Body: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.BodyPartDefinition))}", False, 1, 1)
                __args.Canvas.SetPos(50, 50 + (25 * 1))
                __args.Canvas.DrawText(f"Grip: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.GripPartDefinition))}", False, 1, 1)
                __args.Canvas.SetPos(50, 50 + (25 * 2))
                __args.Canvas.DrawText(f"Mag: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.MagazinePartDefinition))}", False, 1, 1)
                __args.Canvas.SetPos(50, 50 + (25 * 3))
                __args.Canvas.DrawText(f"Barrel: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.BarrelPartDefinition))}", False, 1, 1)
                __args.Canvas.SetPos(50, 50 + (25 * 4))
                __args.Canvas.DrawText(f"Sight: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.SightPartDefinition))}", False, 1, 1)
                __args.Canvas.SetPos(50, 50 + (25 * 5))
                __args.Canvas.DrawText(f"Stock: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.StockPartDefinition))}", False, 1, 1)
                __args.Canvas.SetPos(50, 50 + (25 * 6))
                __args.Canvas.DrawText(f"Action: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.ActionPartDefinition))}", False, 1, 1)
                __args.Canvas.SetPos(50, 50 + (25 * 7))
                __args.Canvas.DrawText(f"Accessory: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.AccessoryPartDefinition))}", False, 1, 1)
                __args.Canvas.SetPos(50, 50 + (25 * 8))
                __args.Canvas.DrawText(f"Material: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.MaterialPartDefinition))}", False, 1, 1)

        if ItemParts.value == True:
            if "EquipAbleItem" in str(get_pc().CurrentSeenPickupable.Inventory):
                __args.Canvas.DrawText(f"Body: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.BodyItemPartDefinition))}", False, 1, 1)
                __args.Canvas.SetPos(50, 50 + (25 * 1))
                __args.Canvas.DrawText(f"Left Side: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.LeftSideItemPartDefinition))}", False, 1, 1)
                __args.Canvas.SetPos(50, 50 + (25 * 2))
                __args.Canvas.DrawText(f"Right Side: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.RightSideItemPartDefinition))}", False, 1, 1)
                __args.Canvas.SetPos(50, 50 + (25 * 3))
                __args.Canvas.DrawText(f"Material: {splitthestring(str(get_pc().CurrentSeenPickupable.Inventory.DefinitionData.MaterialItemPartDefinition))}", False, 1, 1)

    return None


build_mod(options=[WeaponParts, ItemParts, PartR, PartG, PartB, PartA])