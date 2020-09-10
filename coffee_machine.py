from dataclasses import dataclass

# instead of doing this Coffee = namedtuple('Coffee', 'water milk beans price'),
# we can use dataclasses:


@dataclass
class Coffee:
    water: int = 0
    milk: int = 0
    beans: int = 0
    price: int = 0


espresso = Coffee(250, 0, 16, 4)
latte = Coffee(350, 75, 20, 7)
cappuccino = Coffee(200, 100, 12, 6)


@dataclass
class CoffeeMachine:
    water: int = 0
    milk: int = 0
    beans: int = 0
    money: int = 0
    cups: int = 0

    # this is handled by @dataclass:
    # def __init__(self, water=0, milk=0, beans=0, money=0, cups=0):
    #     self.water = water
    #     self.milk = milk
    #     self.beans = beans
    #     self.money = money
    #     self.cups = cups

    def print_resources(self):
        print(f'The coffee machine has:\n'
              f'{self.water} of water\n'
              f'{self.milk} of milk\n'
              f'{self.beans} of coffee beans\n'
              f'{self.cups} of disposable cups\n'
              f'${self.money} of money')

    def has_resources(self, type_coffee):
        return {'water': self.water >= type_coffee.water,
                'milk': self.milk >= type_coffee.milk,
                'beans': self.beans >= type_coffee.beans,
                'cups': self.cups >= 1,
                }

    def refill_machine(self):
        self.water += int(input('Write how many ml of water do you want to add: ') or 0)
        self.milk += int(input('Write how many ml of milk do you want to add: ') or 0)
        self.beans += int(input('Write how many grams of coffee beans do you want to add: ') or 0)
        self.cups += int(input('Write how many disposable cups of coffee do you want to add:') or 0)

    def make_coffee(self, codes_coffee, ordered_coffee_code):
        ordered_coffee = codes_coffee[ordered_coffee_code]
        resources = self.has_resources(ordered_coffee)
        if all(resources.values()):
            print('I have enough resources, making you a coffee!')
            self.money += ordered_coffee.price
            self.water -= ordered_coffee.water
            self.milk -= ordered_coffee.milk
            self.beans -= ordered_coffee.beans
            self.cups -= 1
        else:
            for resource, enough in resources.items():
                if not enough:
                    print(f'Sorry, not enough {resource}!')

    def take_money(self):
        print(f'I gave you ${self.money}')
        self.money = 0

    def power_on(self):
        while True:
            action = input('Write action (buy, fill, take, remaining, exit): ')
            if action == 'exit':
                break
            if action == 'buy':
                codes_coffee = {'1': espresso, '2': latte, '3': cappuccino}
                ordered_coffee_code = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, '
                                            'back - to main menu: ')
                if ordered_coffee_code not in codes_coffee:
                    continue
                else:
                    self.make_coffee(codes_coffee, ordered_coffee_code)
            elif action == 'fill':
                self.refill_machine()
            elif action == 'take':
                self.take_money()
            else:
                self.print_resources()


if __name__ == '__main__':
    coffee_machine = CoffeeMachine(400, 540, 120, 550, 9)
    coffee_machine.power_on()
