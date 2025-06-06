import unrealsdk
from typing import TypedDict
from mods_base import keybind, EInputEvent, get_pc, build_mod, ENGINE, hook, SliderOption, SETTINGS_DIR, BoolOption, DropdownOption, NestedOption
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction, WeakPointer
import os, json
from typing import Any

WeaponParts: BoolOption = BoolOption("Show Weapon Parts", True, "Yes", "No")
ItemParts: BoolOption = BoolOption("Show Equipable Item Parts", True, "Yes", "No")
PartR: SliderOption = SliderOption("Display R Value", 255, 0, 255, 1, True)
PartG: SliderOption = SliderOption("Display G Value", 255, 0, 255, 1, True)
PartB: SliderOption = SliderOption("Display B Value", 255, 0, 255, 1, True)
PartA: SliderOption = SliderOption("Display A Value (Transparency)", 255, 0, 255, 1, True)

ThingToShow: WeakPointer = WeakPointer()

def splitthestring(part: str) -> str:
    noweirdshit: str = part.replace("'", "")
    namelist: list = noweirdshit.split(".")
    return namelist[-1]

@hook(hook_func="Engine.GameViewportClient:PostRender", hook_type=Type.POST)
def render(obj: UObject, _args: WrappedStruct, _ret: Any, _func: BoundFunction) -> None:
    if ThingToShow():
        Inventory = ThingToShow()
    else:
        render.disable()

    Canvas = _args.Canvas

    Canvas.Font = unrealsdk.find_object("Font", "ui_fonts.font_willowbody_18pt")
    Canvas.SetPos(50, 50)
    Canvas.DrawColor = unrealsdk.make_struct("Color", R=PartR.value, G=PartG.value, B=PartB.value, A=PartA.value)

    if WeaponParts.value == True:
        if "Weapon" in str(Inventory):
            Canvas.DrawText(f"Body: {splitthestring(str(Inventory.DefinitionData.BodyPartDefinition))}", False, 1, 1)
            Canvas.SetPos(50, 50 + (25 * 1))
            Canvas.DrawText(f"Grip: {splitthestring(str(Inventory.DefinitionData.GripPartDefinition))}", False, 1, 1)
            Canvas.SetPos(50, 50 + (25 * 2))
            Canvas.DrawText(f"Mag: {splitthestring(str(Inventory.DefinitionData.MagazinePartDefinition))}", False, 1, 1)
            Canvas.SetPos(50, 50 + (25 * 3))
            Canvas.DrawText(f"Barrel: {splitthestring(str(Inventory.DefinitionData.BarrelPartDefinition))}", False, 1, 1)
            Canvas.SetPos(50, 50 + (25 * 4))
            Canvas.DrawText(f"Sight: {splitthestring(str(Inventory.DefinitionData.SightPartDefinition))}", False, 1, 1)
            Canvas.SetPos(50, 50 + (25 * 5))
            Canvas.DrawText(f"Stock: {splitthestring(str(Inventory.DefinitionData.StockPartDefinition))}", False, 1, 1)
            Canvas.SetPos(50, 50 + (25 * 6))
            Canvas.DrawText(f"Action: {splitthestring(str(Inventory.DefinitionData.ActionPartDefinition))}", False, 1, 1)
            Canvas.SetPos(50, 50 + (25 * 7))
            Canvas.DrawText(f"Accessory: {splitthestring(str(Inventory.DefinitionData.AccessoryPartDefinition))}", False, 1, 1)
            Canvas.SetPos(50, 50 + (25 * 8))
            Canvas.DrawText(f"Material: {splitthestring(str(Inventory.DefinitionData.MaterialPartDefinition))}", False, 1, 1)

    if ItemParts.value == True:
        if "EquipAbleItem" in str(Inventory):
            Canvas.DrawText(f"Body: {splitthestring(str(Inventory.DefinitionData.BodyItemPartDefinition))}", False, 1, 1)
            Canvas.SetPos(50, 50 + (25 * 1))
            Canvas.DrawText(f"Left Side: {splitthestring(str(Inventory.DefinitionData.LeftSideItemPartDefinition))}", False, 1, 1)
            Canvas.SetPos(50, 50 + (25 * 2))
            Canvas.DrawText(f"Right Side: {splitthestring(str(Inventory.DefinitionData.RightSideItemPartDefinition))}", False, 1, 1)
            Canvas.SetPos(50, 50 + (25 * 3))
            Canvas.DrawText(f"Material: {splitthestring(str(Inventory.DefinitionData.MaterialItemPartDefinition))}", False, 1, 1)

    return None



@hook('WillowGame.StatusMenuExGFxMovie:UpdateCardPanel', Type.POST)
@hook('WillowGame.BankGFxMovie:UpdateCardPanel', Type.POST)
@hook('WillowGame.VendingMachineGFxMovie:UpdateCardPanel', Type.POST)
def UpdateCardPanel(obj: UObject, _args: WrappedStruct, _ret: Any, _func: BoundFunction) -> None:
    if _args.MainThing:
        global ThingToShow
        ThingToShow = WeakPointer(_args.MainThing)
        render.enable()
    return

@hook('WillowGame.StatusMenuExGFxMovie:OnClose', Type.POST)
@hook('WillowGame.BankGFxMovie:OnClose', Type.POST)
@hook('WillowGame.VendingMachineGFxMovie:OnClose', Type.POST)
@hook('WillowGame.WillowPlayerController:ClearSeenPickupable', Type.POST)
def OnClose(obj: UObject, _args: WrappedStruct, _ret: Any, _func: BoundFunction) -> None:
    global ThingToShow
    ThingToShow = WeakPointer()
    render.disable()
    return

@hook('WillowGame.ItemPickupGFxMovie:extEnableThumbnail', Type.POST)
def extEnableThumbnail(obj: UObject, _args: WrappedStruct, _ret: Any, _func: BoundFunction) -> None:
    if obj.MyHUDOwner.SavedLookAtInventory:
        global ThingToShow
        ThingToShow = WeakPointer(obj.MyHUDOwner.SavedLookAtInventory)
        render.enable()
    return

build_mod(hooks=[UpdateCardPanel, OnClose, extEnableThumbnail], options=[WeaponParts, ItemParts, PartR, PartG, PartB, PartA])