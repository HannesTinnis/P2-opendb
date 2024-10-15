import csv
import os
import locale
from msvcrt import getwch

def load_data(filename):
    products = [] 
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append(
                {                   
                    "id": id,       
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products


def view_products(products):
    product_list = []
    for product in products:
        product_info = f"(#{product['id']}) {product['name']} \t {product['desc']} \t {locale.currency(product['price'], grouping=True)}"
        product_list.append(product_info)
    
    return "\n".join(product_list)


def add_product(products, name, desc, price, quantity):
    max_id = max(products, key=lambda p: p["id"])["id"] if products else 0
    new_id = max_id + 1
    products.append(
        {
            "id": new_id,
            "name": name,
            "desc": desc,
            "price": float(price),
            "quantity": int(quantity),
        }
    )
    return f"Lade till produkt med id: {new_id}"


def get_product_by_id(products, product_id):
    for product in products:
        if product['id'] == product_id:
            return product
    return None


def remove_product(products, product_id):
    product_to_remove = get_product_by_id(products, product_id)
    if product_to_remove:
        products.remove(product_to_remove)
        return f"Produkt med id {product_id} togs bort."
    else:
        return f"Produkt med id {product_id} hittades inte."


def update_product(products, product_id, name=None, desc=None, price=None, quantity=None):
    product = get_product_by_id(products, product_id)
    if product:
        if name: product['name'] = name
        if desc: product['desc'] = desc
        if price: product['price'] = float(price)
        if quantity: product['quantity'] = int(quantity)
        return f"Uppdaterade produkt med id {product_id}."
    else:
        return f"Produkt med id {product_id} hittades inte."


locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  

# Ladda produkterna från CSV-filen en gång
products = load_data('db_products.csv')  

while True:
    os.system('cls')  # Rensa konsolen (anpassa för ditt system om det behövs)
    print(view_products(products))  # Visa produkter vid start

    print("\nVad vill du göra? \nL = Lägg till \nV = Visa \nT = Ta bort \nF = Ändra \nQ = Avsluta")
    choice = getwch().lower()

    if choice == 'l':  # Lägg till produkt
        name = input("Produktnamn: ")
        desc = input("Produktbeskrivning: ")
        price = input("Pris: ")
        quantity = input("Antal: ")
        message = add_product(products, name, desc, price, quantity)
        print(message)

        # Visa de uppdaterade produkterna
        print("\nUppdaterade produkter:")
        print(view_products(products))

    elif choice == 't':  # Ta bort produkt
        product_id = int(input("Ange produktens ID som ska tas bort: "))
        message = remove_product(products, product_id)
        print(message)

        # Visa de uppdaterade produkterna
        print("\nUppdaterade produkter:")
        print(view_products(products))

    elif choice == 'f':  # Ändra produkt
        product_id = int(input("Ange produktens ID som ska ändras: "))
        name = input("Nytt namn (tryck enter för att behålla): ")
        desc = input("Ny beskrivning (tryck enter för att behålla): ")
        price = input("Nytt pris (tryck enter för att behålla): ")
        quantity = input("Nytt antal (tryck enter för att behålla): ")
        message = update_product(products, product_id, name, desc, price, quantity)
        print(message)

        # Visa de uppdaterade produkterna
        print("\nUppdaterade produkter:")
        print(view_products(products))

    elif choice == 'q':  # Avsluta programmet
        break

    input("\nTryck på enter för att fortsätta...")  # Paus innan nästa iteration
