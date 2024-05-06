"""Event handler for space landing"""
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

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

        if player.money < buy_price:
            # Player doesn't have enough money, display message using the announcer and automatically pass
            response['announcement'] += f"You don't have enough money to buy {landed_property.name}.\n"
            return False        
        # Create a Tkinter window
        root = tk.Tk()
        root.title("Property Decision")
        root.configure(bg="ivory")  # Set background color

        # Set the size of the window
        root.geometry("400x300")  # Set the width and height

        # Define custom fonts
        title_font = ("Arial", 18, "bold")
        text_font = ("Arial", 12)
        button_font = ("Arial", 14, "bold")

        # Display information about the property with custom fonts and colors
        label = tk.Label(root, text=f"You landed on {landed_property.name}.\nBuy price: ${buy_price}\nRent price: ${rent_price}", font=text_font, bg="ivory")
        label.pack(pady=20)  # Add padding

        # Function to buy the property
        def buy_property_func():
            root.destroy()  # Close the window
            return buy_property(game, landed_property, player, buy_price, response)

        # Function when player chooses not to buy
        def pass_property_func():
            root.destroy()  # Close the window
            print("You chose not to buy this property.")
            return False

        # Create buttons for buying or passing with custom fonts and colors
        buy_button = tk.Button(root, text="Buy", command=buy_property_func, font=button_font, bg="green", fg="white")
        buy_button.pack(pady=10, padx=20, ipadx=10, ipady=5)  # Add padding and internal padding
        pass_button = tk.Button(root, text="Pass", command=pass_property_func, font=button_font, bg="red", fg="white")
        pass_button.pack(pady=10, padx=20, ipadx=10, ipady=5)  # Add padding and internal padding

        # Run the Tkinter event loop
        root.mainloop()

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
