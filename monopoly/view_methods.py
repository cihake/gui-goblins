"""Event handler for space landing"""
def respond_to_space(game, board, property_deck, player, response):
    space = board.get_space(player.space)
    
    if space.type == "tax":
        response['space_type'] = "tax"
        tax_player(player, space, response)
    elif space.type == "property":
        
        landed_property = property_deck.properties.get(name=space.name)
        respond_to_property(game, landed_property, player, response)
        landed_property.save()


"""Charge a tax to the player"""
def tax_player(player, space, response):
    tax = 0
    if space.name == "Income Tax": tax = 200
    elif space.name == "Luxury Tax": tax = 100
    player.money -= tax
    response['announcement'] = space.name + ": pay $" + str(tax)


"""Either offer to buy the property or charge rent"""
def respond_to_property(game, landed_property, player, response):
    if landed_property.player != player.ordinal:
        buy_price = int(landed_property.prices.split(',')[0])
        player.money -= buy_price
        landed_property.player = player.ordinal
        landed_property.save()
        response['announcement'] += landed_property.name + " bought for $" + str(buy_price) + "\n"
    else:
        rent_price = int(landed_property.rents.split(',')[0])
        player.money += rent_price
        response['announcement'] += "Collected $" + str(rent_price) + " rent on " + landed_property.name + "\n"