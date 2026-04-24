from argparse import Namespace
from mods_base import command, get_pc
from mods_base.settings import SETTINGS_DIR

@command("buhelp", description="Lists available commands from bonk utilities")
def BUHelp(args: Namespace) -> None:
    print("Commands:\n\ndropitem [pool] [amount]\ncrawkills [kill count]\npearlcount [drop count]\nlastpearl [run number]\naddcustomitem [string to search for]\ndeletecustomitem [string to remove]\nlistcustomitems\nsetlancechests [number of chests]")
    return None

@command("dropitem", description="spawns the specified number of items from a loot pool: spawnitem pool amount")
def spawnItems(args: Namespace) -> None:
    numofitems = 1
    if args.amount == None:
        numofitems = 1
    else:
        numofitems = int(args.amount)
    
    while numofitems > 0:
        get_pc().CheatManager.SpawnItemPool(str(args.pool))
        numofitems -= 1
        
spawnItems.add_argument("pool", help="what pool the items come from")
spawnItems.add_argument("amount", help="how many to spawn")

@command("crawkills", description="set the number of craw kills for the counter")
def crawKills(args: Namespace) -> None:
    file = open(f"{SETTINGS_DIR}\\CrawKills.txt", "+w")
    file.write(str(args.kills))
    file.close()
    return None
        
crawKills.add_argument("kills", help="the number of kills to set")

@command("pearlcount", description="the total number of pearl drops for the craw farm")
def pearlDrops(args: Namespace) -> None:
    file = open(f"{SETTINGS_DIR}\\PearlCount.txt", "+w")
    file.write(str(args.pearls))
    file.close()
    return None
        
pearlDrops.add_argument("pearls", help="the number of pearls to set")

@command("lastpearl", description="the run number you got the last pearl on")
def lastPearl(args: Namespace) -> None:
    file = open(f"{SETTINGS_DIR}\\LastPearlRun.txt", "+w")
    file.write(str(args.runnumber))
    file.close()
    return None
        
lastPearl.add_argument("runnumber", help="the run you got the drop on")

@command("setlancechests", description="Set the number of opened lance chests for the lance chest tracker")
def SetLanceChests(args: Namespace) -> None:
    file = open(f"{SETTINGS_DIR}\\lancechests.txt", "+w")
    file.write(str(args.numberofchests))
    file.close()
    return None

SetLanceChests.add_argument("numberofchests", help="the value to set the tracker to")