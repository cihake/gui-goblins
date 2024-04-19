"""The corner is buildable if it isn't build, its corner neighbors aren't built,
and at least one of its neighbors is a land tile"""
def build_attempt(board, yindex, xindex, response):
    corner_to_build = board.corners.get(yindex=yindex, xindex=xindex)
    
    # Check if already built
    if corner_to_build.building == 1:
        response['build_success'] = -1
        response['build_response'] = "That corner already has a building on it."
        return
    
    # Land check
    neighbor_tiles = board.get_neighbor_tiles(corner_to_build)
    touching_land = False
    for Tile in neighbor_tiles:
        terrain = Tile.terrain
        if (terrain == "forest" or terrain == "pasture" or terrain == "fields"
        or terrain == "hills" or terrain == "mountains"):
            touching_land = True
    if touching_land == False:
        response['build_success'] = -2
        response['build_response'] = "The building must be near land."
        return
    
    # Neighbors check
    neighbor_corners = board.get_neighbor_corners(corner_to_build)
    for Corner in neighbor_corners:
        building = Corner.building
        if building != 0:
            response['build_success'] = -3
            response['build_response'] = ("You must build at least two intersections"
            "away from another building, as per the neighbor rule.")
            return
    
    # Successful build
    corner_to_build.building = 1
    corner_to_build.save()
    response['build_success'] = 1
    response['build_response'] = "Built successfully"
    return


"""At the start of a turn, for every corner that is built, check the adjacent tiles.
If the tile's dice value matches the dice roll, add the corresponding terrain resource
to the corresponding player."""
def gather_resources(board, player, dice_value, response):
    for Corner in board.corners.all():
        if Corner.building > 0:
            for Tile in board.get_neighbor_tiles(Corner):
                if Tile.dice == dice_value:
                    terrain = Tile.terrain
                    if terrain == "pasture":
                        player.wool += 1
                        print("Wool gathered")
                    elif terrain == "fields":
                        player.grain += 1
                        print("Grain gathered")
                    elif terrain == "forest":
                        player.lumber += 1
                        print("Lumber gathered")
                    elif terrain == "hills":
                        player.brick += 1
                        print("Brick gathered")
                    elif terrain == "mountains":
                        player.ore += 1
                        print("Ore gathered")
    print(player.__str__())