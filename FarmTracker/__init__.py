from argparse import Namespace
import unrealsdk #type: ignore
from typing import TypedDict
from mods_base import command, keybind, EInputEvent, get_pc, build_mod, hook, SETTINGS_DIR, BoolOption #type: ignore
from unrealsdk.hooks import Type #type: ignore
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction #type: ignore
from .filestuff import *
import os, json

#from GooberLog import log

initFarmTracker()

doTracking: BoolOption = BoolOption("Enable Tracking", True, "Yes", "No")

grabnextenemy: bool = False
grabnextobject: bool = False
objlist: list[str, str] = ["None", "None"]

class farm(TypedDict):
    farmname: str
    enemyname: str
    enemykills: int
    trackeditem: str
    trackeditemcount: int
    pearlcount: int
    legendarycount: int
    trackedobject: str
    trackedobjectcount: int

currentfarm: farm = {
    "farmname": "None",
    "enemyname": "None",
    "enemykills": 0,
    "trackeditem": "None",
    "trackeditemcount": 0,
    "pearlcount": 0,
    "legendarycount": 0,
    "trackedobject": "None",
    "trackedobjectcount": 0,
}

def save() -> None:
    global currentfarm
    file = open(f"{SETTINGS_DIR}\\FarmTracker\\Farms\\{currentfarm['farmname']}.json", "w")
    json.dump(currentfarm, file)
    file.close()
    return None

def load(farmname: str) -> None:
    if len(farmname) < 5 or farmname[-5] != ".":
        filename = farmname + ".json"
    else:
        filename = farmname
    if not os.path.isfile(f"{SETTINGS_DIR}\\FarmTracker\\Farms\\{filename}"):
        print(f"cannot find {filename} in FarmTracker/Farms folder, check to make sure the name is correct")
        return None
    file = open(f"{SETTINGS_DIR}\\FarmTracker\\Farms\\{filename}", "+r")
    global currentfarm
    currentfarm = json.load(file)
    file.close()
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\FarmName.txt", currentfarm["farmname"])
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyKills.txt", currentfarm["enemykills"])
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemCount.txt", currentfarm["trackeditemcount"])
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\PearlCount.txt", currentfarm["pearlcount"])
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCount.txt", currentfarm["legendarycount"])
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\PearlCountWithText.txt", f"Pearl Drops: {currentfarm["pearlcount"]}")
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCountWithText.txt", f"Legendary Drops: {currentfarm["legendarycount"]}")
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyWithCount.txt", f"{currentfarm["enemyname"]}: {currentfarm["enemykills"]}")
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemWithCount.txt", f"{currentfarm["trackeditem"]}: {currentfarm["trackeditemcount"]}")
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\FarmNameAndTrackedObjectCount.txt", f"{currentfarm["farmname"]}: {currentfarm["trackedobjectcount"]}")
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedObjectCount.txt", currentfarm["trackedobjectcount"])

    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\AutoLoad.txt", f"{currentfarm["farmname"]}.json")
    return None


if getValuestr(f"{SETTINGS_DIR}\\FarmTracker\\AutoLoad.txt") != "None":
    print(f"Loading: {getValuestr(f"{SETTINGS_DIR}\\FarmTracker\\AutoLoad.txt")}")
    load(getValuestr(f"{SETTINGS_DIR}\\FarmTracker\\AutoLoad.txt"))

@command("farmhelp", description="List available commands for the farm tracker")
def farmHelp(args: Namespace) -> None:
    print("Commands: do [command name] -h on any of these for more info\nnewfarm\nlistfarms\nsavefarm\nloadfarm\ntrackitem\nsetenemy\nsetkills\nsetitemcount\nsetlegendaries\nsetpearls\nwherefarm")
    return None

@command("newfarm", description="create a new tracked farm by name")
def newfarm(args: Namespace) -> None:
    global currentfarm
    currentfarm["farmname"] = str(args.farmname)
    currentfarm["enemyname"] = "None"
    currentfarm["enemykills"] = 0
    currentfarm["trackeditem"] = "None"
    currentfarm["trackeditemcount"] = 0
    currentfarm["pearlcount"] = 0
    currentfarm["legendarycount"] = 0
    currentfarm["trackedobject"] = "None"
    currentfarm["trackedobjectcount"] = 0
    save()
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\FarmName.txt", currentfarm["farmname"])
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyKills.txt", currentfarm["enemykills"])
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemCount.txt", currentfarm["trackeditemcount"])
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\PearlCount.txt", currentfarm["pearlcount"])
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCount.txt", currentfarm["legendarycount"])
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\PearlCountWithText.txt", f"Pearl Drops: {currentfarm["pearlcount"]}")
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCountWithText.txt", f"Legendary Drops: {currentfarm["legendarycount"]}")
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyWithCount.txt", f"{currentfarm["enemyname"]}: {currentfarm["enemykills"]}")
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemWithCount.txt", f"{currentfarm["trackeditem"]}: {currentfarm["trackeditemcount"]}")
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\FarmNameAndTrackedObjectCount.txt", f"{currentfarm["farmname"]}: {currentfarm["trackedobjectcount"]}")
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedObjectCount.txt", currentfarm["trackedobjectcount"])

    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\AutoLoad.txt", f"{currentfarm["farmname"]}.json")
    return None
        
newfarm.add_argument("farmname", help="the name to save the farm by")

@command("listfarms", description="print out a list of previously saved farms")
def farmList(args: Namespace) -> None:
    if not os.path.exists(f"{SETTINGS_DIR}\\FarmTracker\\Farms"):
        print("FarmTracker/Farms folder does not exist, there are no saved farms")
        return None
    print("Saved farms:")
    for file in os.listdir(f"{SETTINGS_DIR}\\FarmTracker\\Farms"):
        print(f"{file}")
    return None

@command("savefarm", description="force save the current farm")
def saveFarm(args: Namespace) -> None:
    save()
    return None

@command("loadfarm", description="load a previously made farm file")
def loadfarm(args: Namespace) -> None:
    load(str(args.farmname))
    return None
        
loadfarm.add_argument("farmname", help="the name of the farm to load")

@command("trackitem", description="name of the item you want to track drops for")
def itemDrop(args: Namespace) -> None:
    global currentfarm
    currentfarm["trackeditem"] = str(args.itemname)
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemCount.txt", currentfarm["trackeditemcount"])
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemWithCount.txt", f"{currentfarm["trackeditem"]}: {currentfarm["trackeditemcount"]}")
    return None
        
itemDrop.add_argument("itemname", help="the name to search for when item drop")

@command("setkills", description="Set the number of kills for the tracked enemy in the current farm")
def setKills(args: Namespace) -> None:
    global currentfarm
    currentfarm["enemykills"] = int(args.kills)
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyKills.txt", currentfarm["enemykills"])
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyWithCount.txt", f"{currentfarm["enemyname"]}: {currentfarm["enemykills"]}")
    return None

setKills.add_argument("kills", help="the number of kills to set the tracker to")

@command("setitemcount", description="Set the number of drops for the tracked item in the current farm")
def setDrops(args: Namespace) -> None:
    global currentfarm
    currentfarm["trackeditemcount"] = int(args.drops)
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemCount.txt", currentfarm["trackeditemcount"])
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemWithCount.txt", f"{currentfarm["trackeditem"]}: {currentfarm["trackeditemcount"]}")
    return None

setDrops.add_argument("drops", help="the number of drops to set the tracker to")

@command("setlegendaries", description="Set the number of legendary drops in the current farm")
def setLegendaries(args: Namespace) -> None:
    global currentfarm
    currentfarm["legendarycount"] = int(args.drops)
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCount.txt", currentfarm["legendarycount"])
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCountWithText.txt", f"Legendary Drops: {currentfarm["legendarycount"]}")
    return None

setLegendaries.add_argument("drops", help="the number of legendaries to set the tracker to")

@command("setpearls", description="Set the number of pearl drops in the current farm")
def setPearls(args: Namespace) -> None:
    global currentfarm
    currentfarm["pearlcount"] = int(args.drops)
    setValue(f"{SETTINGS_DIR}\\FarmTracker\\PearlCount.txt", currentfarm["pearlcount"])
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\PearlCountWithText.txt", f"Pearl Drops: {currentfarm["pearlcount"]}")
    return None

setPearls.add_argument("drops", help="the number of pearls to set the tracker to")

@command("wherefarm", description="print the directory where the files live to use them in obs/capture program")
def whereFarm(args: Namespace) -> None:
    print(f"{SETTINGS_DIR}\\FarmTracker")
    return None

@command("setenemy", description="Manual override for setting what enemy you want to track, instead of using the keybind & autotrack. useful for a more generic farm.")
def setEnemy(args: Namespace) -> None:
    global currentfarm
    currentfarm["enemyname"] = str(args.enemyname)
    setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyWithCount.txt", f"{currentfarm["enemyname"]}: {currentfarm["enemykills"]}")
    return None

setEnemy.add_argument("enemyname", help="the name you want to check for when killing an enemy")



@keybind(identifier="Track Next Damaged Enemy", key=None, event_filter=EInputEvent.IE_Pressed)
def doTrack():
    global grabnextenemy
    grabnextenemy = not grabnextenemy
    #displaymessage("Shoot the enemy you want to start tracking")

@keybind(identifier="Track Next Used Object", key=None, event_filter=EInputEvent.IE_Pressed, description="open a chest or something")
def doTrackObject():
    global grabnextobject
    grabnextobject = not grabnextobject
    #displaymessage("Shoot the enemy you want to start tracking")








@hook(hook_func="Engine.Pawn:TakeDamage", hook_type=Type.PRE)
def pickEnemy(obj: UObject, __args: WrappedStruct, __ret: any, __func: BoundFunction) -> None:
    global grabnextenemy, currentfarm
    if doTracking.value == False:
        return None
    if obj.Class.Name == "WillowVehicle_WheeledVehicle":
        return None
    if obj.Class.Name != "WillowPlayerPawn":
        if "WillowPlayerController" in str(__args.InstigatedBy):
            if grabnextenemy == True:
                currentfarm["enemyname"] = obj.BalanceDefinitionState.BalanceDefinition.Grades[0].GradeModifiers.DisplayName
                grabnextenemy = False
                setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyKills.txt", currentfarm["enemykills"])
                setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyWithCount.txt", f"{currentfarm["enemyname"]}: {currentfarm["enemykills"]}")
    return None

@hook(hook_func="Engine.Pawn:Died", hook_type=Type.PRE)
def killEnemy(obj: UObject, __args: WrappedStruct, __ret: any, __func: BoundFunction) -> None:
    global grabnextenemy, currentfarm
    if doTracking.value == False:
        return None
    if obj.Class.Name == "WillowVehicle_WheeledVehicle":
        return None
    if obj.Class.Name != "WillowPlayerPawn":
        if obj.BalanceDefinitionState.BalanceDefinition.Grades[0].GradeModifiers.DisplayName == currentfarm["enemyname"]:
            currentfarm["enemykills"] += 1
            setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyKills.txt", currentfarm["enemykills"])
            setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\TrackedEnemyWithCount.txt", f"{currentfarm["enemyname"]}: {currentfarm["enemykills"]}")
            save()
    return None

@hook(hook_func="WillowGame.WillowPickup:InitializeFromInventory", hook_type=Type.POST)
def trackDrop(obj: UObject, __args: WrappedStruct, __ret: any, __func: BoundFunction) -> None:
    global currentfarm
    if doTracking.value == False:
        return None
    if get_pc().GetInventoryPawn() == None:
        return None
    for item in get_pc().GetInventoryPawn().EquippedItems:
        if obj == item:
            return None
    equippedweaps: list = [None, None, None, None]
    get_pc().GetInventoryPawn().InvManager.GetEquippedWeapons(equippedweaps[0], equippedweaps[1], equippedweaps[2], equippedweaps[3])
    for weapon in equippedweaps:
        if obj == weapon:
            return None
    if currentfarm["trackeditem"].lower() in obj.Inventory.GetHumanReadableName().lower():
        currentfarm["trackeditemcount"] += 1
        setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemCount.txt", currentfarm["trackeditemcount"])
        setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\TrackedItemWithCount.txt", f"{currentfarm["trackeditem"]}: {currentfarm["trackeditemcount"]}")

    if obj.InventoryRarityLevel > 100 and obj.InventoryRarityLevel < 170:
        currentfarm["pearlcount"] += 1
        setValue(f"{SETTINGS_DIR}\\FarmTracker\\PearlCount.txt", currentfarm["pearlcount"])
        setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\PearlCountWithText.txt", f"Pearl Drops: {currentfarm["pearlcount"]}")
    if obj.InventoryRarityLevel > 49 and obj.InventoryRarityLevel < 101:
        currentfarm["legendarycount"] += 1
        setValue(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCount.txt", currentfarm["legendarycount"])
        setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\LegendaryCountWithText.txt", f"Legendary Drops: {currentfarm["legendarycount"]}")
    save()
    return None



@hook(hook_func="WillowGame.WillowInteractiveObject:UseObject", hook_type=Type.POST)
def useInteractiveObject(obj: UObject, __args: WrappedStruct, __ret: any, __func: BoundFunction) -> None:
    global grabnextobject, currentfarm
    if doTracking.value == False:
        return None
    if grabnextobject == True:
        currentfarm["trackedobject"] = str(obj.InteractiveObjectDefinition)
        grabnextobject = False
    if str(obj.InteractiveObjectDefinition) == currentfarm["trackedobject"]:
        currentfarm["trackedobjectcount"] += 1
        setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedObjectCount.txt", currentfarm["trackedobjectcount"])
        setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\FarmNameAndTrackedObjectCount.txt", f"{currentfarm["farmname"]}: {currentfarm["trackedobjectcount"]}")
        save()
    return None

@hook(hook_func="WillowGame.WillowInteractiveObject:TakeDamage", hook_type=Type.PRE)
def damageInteractiveObject(obj: UObject, __args: WrappedStruct, __ret: any, __func: BoundFunction) -> None:
    global grabnextobject, currentfarm, objlist
    if doTracking.value == False:
        return None
    if grabnextobject == True and obj.bCanBeUsed and obj.InteractiveObjectDefinition.bCanTakeDirectDamage and obj.InteractiveObjectDefinition.bCanTakeRadiusDamage:
        currentfarm["trackedobject"] = str(obj.InteractiveObjectDefinition)
        grabnextobject = False
    if str(obj.InteractiveObjectDefinition) == currentfarm["trackedobject"] and obj.bCanBeUsed and obj.InteractiveObjectDefinition.bCanTakeDirectDamage and obj.InteractiveObjectDefinition.bCanTakeRadiusDamage:
        currentfarm["trackedobjectcount"] += 1
        setValue(f"{SETTINGS_DIR}\\FarmTracker\\TrackedObjectCount.txt", currentfarm["trackedobjectcount"])
        setValuestr(f"{SETTINGS_DIR}\\FarmTracker\\FarmNameAndTrackedObjectCount.txt", f"{currentfarm["farmname"]}: {currentfarm["trackedobjectcount"]}")
        save()
    return None

@hook(hook_func="Engine.GameViewportClient:PostRender", hook_type=Type.POST)
def render(obj: UObject, __args: WrappedStruct, __ret: any, __func: BoundFunction) -> None:
    global grabnextenemy, grabnextobject, currentfarm
    __args.Canvas.Font = unrealsdk.find_object("Font", "ui_fonts.font_willowbody_18pt")
    if grabnextenemy == True:
        __args.Canvas.DrawColor = unrealsdk.make_struct("Color", R=255, G=0, B=0, A=255)
        __args.Canvas.SetPos(50, 100)
        __args.Canvas.DrawText(f"Shoot the enemy you want to start tracking", False, 2.5, 2.5)
    if grabnextobject == True:
        __args.Canvas.DrawColor = unrealsdk.make_struct("Color", R=255, G=0, B=0, A=255)
        __args.Canvas.SetPos(50, 150)
        __args.Canvas.DrawText(f"Use/shoot the object you want to track", False, 2.5, 2.5)
    if currentfarm["farmname"] == "None":
        __args.Canvas.DrawColor = unrealsdk.make_struct("Color", R=255, G=0, B=0, A=255)
        __args.Canvas.SetPos(50, 50)
        __args.Canvas.DrawText(f"There is no farm loaded, use the newfarm command to create one", False, 2.5, 2.5)
    return None

build_mod()