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
        rent_price = int(landed_property.rents.split(',')[0])

        print(f"You landed on {landed_property.name}.")
        print(f"Buy price: ${buy_price}")
        print(f"Rent price: ${rent_price}")

        # Ask the player if they want to buy the property
        choice = input("Do you want to buy this property? (yes/no): ").lower()
        if choice == "yes":
            return buy_property(game, landed_property, player, buy_price, response)
        else:
            print("You chose not to buy this property.")
            return False
    else:
        rent_price = int(landed_property.rents.split(',')[0])
        player.money += rent_price
        response['announcement'] += f"Collected ${rent_price} rent on {landed_property.name}\n"
    
    return False

def buy_property(game, landed_property, player, buy_price, response):
    if player.money >= buy_price:
        player.money -= buy_price
        landed_property.player = player.ordinal
        landed_property.save()
        response['announcement'] += f"{landed_property.name} bought for ${buy_price}\n"
        return True
    else:
        print("You don't have enough money to buy this property.")
        return False
