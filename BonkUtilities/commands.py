from argparse import Namespace
from mods_base import command, get_pc
import unrealsdk

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