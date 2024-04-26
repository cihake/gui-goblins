"""Game setup; players place their starter buildings"""
def handle_setup(game, board, player, yindex, xindex, response):
    response['build_type'] = "settlement"
    build_attempt(board, yindex, xindex, response)
    # Respond to successful build
    if response['build_success'] == 1:
        player.starting_settlements -= 1
        player.save()
        # Try to progress
        if player.starting_settlements > 0:
            response['announcement'] += "Remaining settlements: " + str(player.starting_settlements) + "\n"
        else:
            game.setup_flag = 0
            response['announcement'] += "Setup finished, all settlements are placed.\n"
    # Respond to unsuccessful build
    else:
        response['announcement'] += "Remaining settlements: " + str(player.starting_settlements) + "\n"
    print(response['announcement'])


"""The corner is buildable if it isn't build, its corner neighbors aren't built,
and at least one of its neighbors is a land tile"""
def build_attempt(board, yindex, xindex, response):
    corner_to_build = board.corners.get(yindex=yindex, xindex=xindex)
    # Check if already built
    if corner_to_build.building == 1:
        response['build_success'] = -1
        response['announcement'] += "That corner already has a building on it.\n"
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
        response['announcement'] += "The building must be near land.\n"
        return
    
    # Neighbors check
    neighbor_corners = board.get_neighbor_corners(corner_to_build)
    for Corner in neighbor_corners:
        building = Corner.building
        if building != 0:
            response['build_success'] = -3
            response['announcement'] += "The building cannot be adjacent to another building.\n"
            return
    
    # Successful build
    corner_to_build.building = 1
    corner_to_build.save()
    response['build_success'] = 1
    response['announcement'] += "Built successfully\n"
    return


"""A road must be along the edge next to a land tile and not overlap another road.
Additionally, it must start at one of the player's own buildings or roads.
The road is built in two phases: start and end, which are across user interactions,
requiring data to be stored."""
def handle_road_build (game, board, player, yindex, xindex, response):
    # Land check
    corner_to_build = board.corners.get(yindex=yindex, xindex=xindex)
    neighbor_tiles = board.get_neighbor_tiles(corner_to_build)
    touching_land = False
    for Tile in neighbor_tiles:
        terrain = Tile.terrain
        if (terrain == "forest" or terrain == "pasture" or terrain == "fields" or terrain == "hills" or terrain == "mountains"):
            touching_land = True
    if touching_land == False:
        response['build_success'] = -1
        response['announcement'] += "The road must begin and end along a land tile.\n"
        return

    # Road start
    if game.build_flag == 2:
        response['build_type'] = "road_start"
        response['build_success'] = 0
        # Building check
        if corner_to_build.building != 0:
             response['build_success'] = 1
        # Road check
        elif len(corner_to_build.roads) > 0:
            response['build_success'] = 1
        # Successful build
        if response['build_success'] == 1:
            board.road_start = str(yindex) + "," + str(xindex)
            game.build_flag = 3
            response['announcement'] = "Where to?"
            return
        else: # Unsuccessful build
            response['build_success'] = -2
            response['announcement'] += "The road must begin at one of your own buildings or roads.\n"
            return
        
    
    # Road end
    elif game.build_flag == 3:
        # Successful build
        response['build_type'] = "road_end"
        response['road_start'] = board.road_start
        response['build_success'] = 1
        # Save road on corners
        road_start = board.road_start.split(',')
        starting_corner = board.corners.get(yindex=road_start[0], xindex=road_start[1])
        starting_corner.roads += str(player.ordinal) + ","
        print(starting_corner.__str__())
        starting_corner.save()
        corner_to_build.roads += str(player.ordinal) + ","
        print(corner_to_build.__str__())
        corner_to_build.save()
        game.build_flag = 0
        response['announcement'] += "Built successfully\n"
        return
    """if game.build_flag == 2:
        if corner_to_build.building == 0: # Check building
            if corner_to_build"""


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
                        response['announcement'] += "Wool gathered\n"
                    elif terrain == "fields":
                        player.grain += 1
                        print("Grain gathered")
                        response['announcement'] += "Grain gathered\n"
                    elif terrain == "forest":
                        player.lumber += 1
                        print("Lumber gathered")
                        response['announcement'] += "Lumber gathered\n"
                    elif terrain == "hills":
                        player.brick += 1
                        print("Brick gathered")
                        response['announcement'] += "Brick gathered\n"
                    elif terrain == "mountains":
                        player.ore += 1
                        print("Ore gathered")
                        response['announcement'] += "Ore gathered\n"
    print(player.__str__())


"""Check for if a player can afford to build / buy something.
A settlement costs wool, grain, lumber, and brick, a road costs lumber and brick."""
def can_afford(player, input, response):
    if input == "build_settlement":
        if (player.wool > 0 and player.grain > 0 and player.lumber > 0 and player.brick > 0):
            return True
        else: return False
    elif input == "build_road":
        if (player.lumber > 0 and player.brick > 0):
            return True
        else: return False