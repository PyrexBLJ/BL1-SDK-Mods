import unrealsdk
from typing import TypedDict
from mods_base import keybind, EInputEvent, get_pc, build_mod, ENGINE, hook, SliderOption, SETTINGS_DIR, BoolOption, DropdownOption
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from .maps import *
from .commands import *
import os, json

photomode: bool = False
myPawn = None
myPawnButForNoclip = None
noclip: bool = False
saveslot: int = 0
thirdperson: bool = False
wantstophasejump: bool = False


FOV: SliderOption = SliderOption("FOV", 110, 65, 180, 1, True)
NoclipSpeed: SliderOption = SliderOption("Noclip Speed", 5000, 500, 12000, 1, True)
MsgDisplayTime: SliderOption = SliderOption("Top Screen Message Time", 3.5, 0, 5, 0.1, False)
UseHLQNoclip: BoolOption = BoolOption("Use HLQ Noclip", True, "Yes", "No")
DesiredFPS: SliderOption = SliderOption("Desired FPS", 120, 30, 1024, 1, True, on_change = lambda _, new_value: setFPS(_, new_value))
MapforTravel: DropdownOption = DropdownOption("Map for Travel Keybind", "arid_p", maps.maplist)
PearlDetector: BoolOption = BoolOption("Pearl Item Detector", True, "On", "Off")


class location(TypedDict):
    coords: tuple[float, float, float]
    angles: tuple[int, int, int]

class maplocations(TypedDict):
    map: str
    locations: list[location]

savedlocations: list = []
def prepLocations() -> None:
    global savedlocations
    if not os.path.isfile(f"{SETTINGS_DIR}\\BonkLocations.json"):
        file = open(f"{SETTINGS_DIR}\\BonkLocations.json", "+a")
        for map in maps.maplist:
            newmap: maplocations = {
                "map": map,
                "locations": [],
            }
            savedlocations.append(newmap)
        json.dump(savedlocations, file)
        file.close()
        print(f"Locations file was not found so it was just created")
        locationsfile = open(f"{SETTINGS_DIR}\\BonkLocations.json", "+r")
        savedlocations = json.load(locationsfile)
        locationsfile.close()
    else:
        locationsfile = open(f"{SETTINGS_DIR}\\BonkLocations.json", "+r")
        savedlocations = json.load(locationsfile)
        locationsfile.close()

prepLocations()


def setFPS(_: SliderOption, new_value: int) -> None:
    ENGINE.MaxSmoothedFrameRate = new_value
    ENGINE.MinSmoothedFrameRate = new_value
    return None

def displaymessage(message: str) -> None:
    get_pc().myHUD.GetHUDMovie().AddCriticalText(0, message, MsgDisplayTime.value, get_pc().myHUD.WhiteColor, get_pc().myHUD.WPRI)


@keybind(identifier="Godmode", key=None, event_filter=EInputEvent.IE_Pressed)
def doGodmode():
    get_pc().bGodMode = not get_pc().bGodMode
    if get_pc().bGodMode:
        displaymessage("Godmode: <font color = \"#00FF00\">On</font>")
    else:
        displaymessage("Godmode: <font color = \"#FF0000\">Off</font>")

@keybind(identifier="Photomode", key=None, event_filter=EInputEvent.IE_Pressed)
def doPhotomode():
    global photomode, myPawn
    if photomode == False:
        myPawn = get_pc().Pawn
        ENGINE.GetCurrentWorldInfo().bPlayersOnly = True
        get_pc().ServerSpectate()
        photomode = True
    else:
        get_pc().Possess(myPawn, True)
        ENGINE.GetCurrentWorldInfo().bPlayersOnly = False
        photomode = False
        myPawn = None

@keybind(identifier="Noclip", key=None, event_filter=EInputEvent.IE_Pressed)
def doNoclip():
    global noclip, myPawnButForNoclip
    if UseHLQNoclip.value == True:
        get_pc().CheatManager.HLQNoClipToggle()
        displaymessage("Toggled HLQ Noclip")
    else:
        if noclip == False:
            myPawnButForNoclip = get_pc().Pawn
            get_pc().Pawn.AirSpeed = NoclipSpeed.value
            get_pc().Pawn.bCollideWorld = False
            get_pc().Pawn.CollisionType = 1
            get_pc().Pawn.LandMovementState = "PlayerFlying"
            get_pc().UnPossess()
            get_pc().Possess(myPawnButForNoclip, False)
            noclip = True
            displaymessage("Noclip: <font color = \"#00FF00\">On</font>")
        else:
            myPawnButForNoclip = get_pc().Pawn
            get_pc().Pawn.AirSpeed = 500.0
            get_pc().Pawn.bCollideWorld = True
            get_pc().Pawn.CollisionType = 6
            get_pc().Pawn.LandMovementState = "PlayerWalking"
            get_pc().UnPossess()
            get_pc().Possess(myPawnButForNoclip, False)
            noclip = False
            displaymessage("Noclip: <font color = \"#FF0000\">Off</font>")

@keybind(identifier="Self Revive", key=None, event_filter=EInputEvent.IE_Pressed)
def doSelfRevive():
    if get_pc().Pawn.bInjuredState > 0 and not get_pc().Pawn.bIsDead:
        get_pc().Pawn.GoFromInjuredToHealthy()
        displaymessage("Revived!")

@keybind(identifier="Save Location", key=None, event_filter=EInputEvent.IE_Pressed)
def doSaveLocation():
    global savedlocations, saveslot
    thismapsindex: int = -1
    for mapindex in savedlocations:
        if str(ENGINE.GetCurrentWorldInfo().CommittedPersistentLevelName).lower() == savedlocations[savedlocations.index(mapindex)]["map"]:
            thismapsindex = savedlocations.index(mapindex)
    
    if thismapsindex != -1:
        newslot: location = {
            "coords": (get_pc().Pawn.Location.X, get_pc().Pawn.Location.Y, get_pc().Pawn.Location.Z),
            "angles": (get_pc().Pawn.Controller.Rotation.Pitch, get_pc().Pawn.Controller.Rotation.Yaw, 0)
        }
        savedlocations[thismapsindex]["locations"].append(newslot)
        file = open(f"{SETTINGS_DIR}\\BonkLocations.json", "w")
        json.dump(savedlocations, file)
        file.close()
        saveslot = savedlocations[thismapsindex]["locations"].index(newslot)
        displaymessage(f"Saved location in slot <font color = \"#FFD700\">{savedlocations[thismapsindex]["locations"].index(newslot)}</font>")
    else:
        displaymessage("Did not find this map in the list, cannot save")

@keybind(identifier="Load Location", key=None, event_filter=EInputEvent.IE_Pressed)
def doLoadLocation():
    global savedlocations, saveslot
    thismapsindex: int = -1
    for mapindex in savedlocations:
        if str(ENGINE.GetCurrentWorldInfo().CommittedPersistentLevelName).lower() == savedlocations[savedlocations.index(mapindex)]["map"]:
            thismapsindex = savedlocations.index(mapindex)
    if thismapsindex == -1:
        displaymessage("Could not find this map in the list, error")
    else:
        pcon = get_pc()
        if len(savedlocations[thismapsindex]["locations"]) == 0 or len(savedlocations[thismapsindex]["locations"]) < saveslot:
            displaymessage(f"No Saved Location in slot <font color = \"#FFD700\">{saveslot}</font>")
        else:
            # why was this such a pain in the ass
            location = unrealsdk.make_struct("Vector", X=savedlocations[thismapsindex]["locations"][saveslot]["coords"][0], Y=savedlocations[thismapsindex]["locations"][saveslot]["coords"][1], Z=savedlocations[thismapsindex]["locations"][saveslot]["coords"][2])
            rotation = unrealsdk.make_struct("Rotator", Pitch=savedlocations[thismapsindex]["locations"][saveslot]["angles"][0], Yaw=savedlocations[thismapsindex]["locations"][saveslot]["angles"][1], Roll=savedlocations[thismapsindex]["locations"][saveslot]["angles"][2])
            pcon.NoFailSetPawnLocation(pcon.Pawn, location)
            get_pc().Pawn.ClientSetRotation(rotation)
            displaymessage(f"Loaded Location in slot <font color = \"#FFD700\">{saveslot}</font>")

@keybind(identifier="Increase Location Slot", key=None, event_filter=EInputEvent.IE_Pressed)
def increaseLocationSlot() -> None:
    global saveslot
    thismapsindex: int = -1
    for mapindex in savedlocations:
        if str(ENGINE.GetCurrentWorldInfo().CommittedPersistentLevelName).lower() == savedlocations[savedlocations.index(mapindex)]["map"]:
            thismapsindex = savedlocations.index(mapindex)
    
    saveslot += 1

    if saveslot > len(savedlocations[thismapsindex]["locations"]):
        saveslot = 0

    displaymessage(f"Using Slot: <font color = \"#FFD700\">{saveslot}</font>")

@keybind(identifier="Decrease Location Slot", key=None, event_filter=EInputEvent.IE_Pressed)
def decreaseLocationSlot() -> None:
    global saveslot
    thismapsindex: int = -1
    for mapindex in savedlocations:
        if str(ENGINE.GetCurrentWorldInfo().CommittedPersistentLevelName).lower() == savedlocations[savedlocations.index(mapindex)]["map"]:
            thismapsindex = savedlocations.index(mapindex)

    saveslot -= 1
    if saveslot < 0:
        saveslot = len(savedlocations[thismapsindex]["locations"])

    displaymessage(f"Using Slot: <font color = \"#FFD700\">{saveslot}</font>")

@keybind(identifier="Open Fast Travel Menu/Respec", key=None, event_filter=EInputEvent.IE_Pressed)
def doFastTravel():
    get_pc().PlayGfxMovieDefinition("ui_registration_station.Definitions.registration_station_def")

@keybind(identifier="Quit Without Saving", key=None, event_filter=EInputEvent.IE_Pressed)
def doQuitWithoutSaving():
    get_pc().ConsoleCommand("disconnect")

@keybind(identifier="Speed Up Time", key=None, event_filter=EInputEvent.IE_Pressed)
def doSpeedUpTime():
    if ENGINE.GetCurrentWorldInfo().TimeDilation >= 32:
        ENGINE.GetCurrentWorldInfo().TimeDilation = 1
    else:
        ENGINE.GetCurrentWorldInfo().TimeDilation = ENGINE.GetCurrentWorldInfo().TimeDilation * 2

@keybind(identifier="Slow Down Time", key=None, event_filter=EInputEvent.IE_Pressed)
def doSlowDownTime():
    if ENGINE.GetCurrentWorldInfo().TimeDilation <= 0.125:
        ENGINE.GetCurrentWorldInfo().TimeDilation = 1
    else:
        ENGINE.GetCurrentWorldInfo().TimeDilation = ENGINE.GetCurrentWorldInfo().TimeDilation / 2

@keybind(identifier="Reset Game Speed", key=None, event_filter=EInputEvent.IE_Pressed)
def doResetTime():
    ENGINE.GetCurrentWorldInfo().TimeDilation = 1.0

@keybind(identifier="Kill All", key=None, event_filter=EInputEvent.IE_Pressed)
def doKillAll():
    for pawn in get_pc().ThePawnList.FullPawnList:
        if pawn.Class.Name != "WillowPlayerPawn" and pawn.Allegiance not in ("gd_allegiance.Player.PlayerAllegiance", "gd_allegiance.Friendly.FriendlyAllegiance", "gd_allegiance.Settler.SettlerAllegiance"):
            pawn.SetHealth(-1)

@keybind(identifier="Delete Dropped Items", key=None, event_filter=EInputEvent.IE_Pressed)
def doDeleteItems():
    count: int = 0
    for drop in unrealsdk.find_all("WillowPickup")[1:]:
        if drop.bIsMissionItem == False:
            drop.Behavior_Destroy()
            count += 1
    displaymessage(f"{count} Items Deleted")

@keybind(identifier="Toggle HUD", key=None, event_filter=EInputEvent.IE_Pressed)
def doToggleHUD():
    get_pc().myHUD.ToggleHUD()

@keybind(identifier="Drop Weapon", key=None, event_filter=EInputEvent.IE_Pressed)
def doDropWeapon():
    get_pc().ThrowWeapon()

@keybind(identifier="Freeze Time", key=None, event_filter=EInputEvent.IE_Pressed)
def doFreezeTime():
    ENGINE.GetCurrentWorldInfo().bPlayersOnly = not ENGINE.GetCurrentWorldInfo().bPlayersOnly

@keybind(identifier="Refresh Vendor Inventories", key=None, event_filter=EInputEvent.IE_Pressed)
def doNewVendors():
    for vendor in unrealsdk.find_all("WillowVendingMachine")[1:]:
        vendor.ResetInventory()
    displaymessage("Shops have new inventory!")

@keybind(identifier="Toggle Camera Position", key=None, event_filter=EInputEvent.IE_Pressed)
def doCameraPos():
    global thirdperson
    if thirdperson == False:
        get_pc().ServerCamera("3rd")
        thirdperson = True
    else:
        get_pc().ServerCamera("1st")
        thirdperson = False

@keybind(identifier="Phasejump", key=None, event_filter=EInputEvent.IE_Pressed)
def doPhasejump():
    global wantstophasejump
    if get_pc().Pawn.PhaseWalkInfo.bIsPhaseWalking == True:
        wantstophasejump = True
        get_pc().ServerForcePhaseWalkExit()

@keybind(identifier="Travel to Selected Map", key=None, event_filter=EInputEvent.IE_Pressed)
def doTravel():
    get_pc().ConsoleCommand(f"openl {MapforTravel.value}")



@hook(hook_func="WillowGame.WillowPlayerController:SpawningProcessComplete", hook_type=Type.POST)
def finishedSpawning(obj: UObject, __args: WrappedStruct, __ret: any, __func: BoundFunction) -> None:
    get_pc().PlayerClass.FOV = FOV.value
    get_pc().SetFOV(get_pc().PlayerClass.FOV)
    get_pc().ClientSetProfileLoaded()
    ENGINE.MaxSmoothedFrameRate = DesiredFPS.value
    ENGINE.MinSmoothedFrameRate = DesiredFPS.value
    for point in unrealsdk.find_object("InterpTrackFloatProp", "weap_camera_animations.Melee.melee_lilith:InterpGroup_3.InterpTrackFloatProp_0").FloatTrack.Points:
        point.OutVal = FOV.value
    for point in unrealsdk.find_object("InterpTrackFloatProp", "weap_camera_animations.Melee.melee_mordacai:InterpGroup_2.InterpTrackFloatProp_0").FloatTrack.Points:
        point.OutVal = FOV.value
    if get_pc().CheatManager == None:
        get_pc().CheatManager = unrealsdk.construct_object("WillowGame.WillowCheatManager", get_pc())



@hook(hook_func="WillowGame.WillowPlayerController:Behavior_ExitPhaseWalk", hook_type=Type.PRE)
def exitPhasewalk(obj: UObject, __args: WrappedStruct, __ret: any, __func: BoundFunction) -> None:
    global wantstophasejump
    if wantstophasejump == True:
        unrealsdk.find_all("WillowPlayerInput")[-1].Jump()
        wantstophasejump = False
    return None
# 101-169 pearl rarity
@hook(hook_func="WillowGame.WillowPickup:InitializeFromInventory", hook_type=Type.POST)
def detectPearl(obj: UObject, __args: WrappedStruct, __ret: any, __func: BoundFunction) -> None:
    if obj.InventoryRarityLevel > 100 and obj.InventoryRarityLevel < 170 and PearlDetector.value == True:
        get_pc().myHUD.GetHUDMovie().AddCriticalText(0, "<font color = \"#00ffc8\" size = \"32\">Pearl Drop Detected!</font>", 5.0, get_pc().myHUD.WhiteColor, get_pc().myHUD.WPRI)
    return None

@hook(hook_func="WillowGame.WillowPickup:AdjustPickupPhysicsAndCollisionForBeingAttached", hook_type=Type.POST)
def detectPearlChest(obj: UObject, __args: WrappedStruct, __ret: any, __func: BoundFunction) -> None:
    if obj.InventoryRarityLevel > 100 and obj.InventoryRarityLevel < 170 and PearlDetector.value == True:
        get_pc().myHUD.GetHUDMovie().AddCriticalText(0, "<font color = \"#00ffc8\" size = \"32\">Pearl Drop Detected!</font>", 5.0, get_pc().myHUD.WhiteColor, get_pc().myHUD.WPRI)
    return None

build_mod()