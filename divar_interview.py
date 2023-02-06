import json
from datetime import datetime, timedelta
import operator


class Food:
    def __init__(self, id, price, cook_duration):
        self.__id = id
        self.__price = price
        self.__cook_duration = cook_duration
        print(id, price, cook_duration)

    @property
    def get_id(self):
        return self.__id

    @property
    def get_price(self):
        return self.__price

    @property
    def get_cook_duration(self):
        return self.__cook_duration


class Order:
    def __init__(self, customer_id: int, food: Food, submit_time: datetime):
        self.__customer_id = customer_id
        self.__food = food
        self.__submit_time = submit_time
        self.__ready_time = submit_time + timedelta(minutes=self.__food.get_cook_duration)

    @property
    def get_ready_order_time(self):
        return self.__ready_time

    @property
    def get_price(self):
        return self.__food.get_price


class Customer:
    def __init__(self, id, arrive_time, orders):
        self.__id = id
        self.__orders = orders
        self.order = []
        l = str(arrive_time).split()
        date = str(l[0]).split('-')
        times = str(l[1]).split(':')
        self.__arrive_time = datetime(int(date[0]), int(date[1]), int(date[2]),
                                      int(times[0]), int(times[1]), int(times[2]))

    def get_dict(self):
        return {'id': self.__id, 'spent_amount': self.__price,
                'arrival_time': str(self.__arrive_time), 'leaving_time': str(self.__leaving_time)}

    @property
    def get_orders(self):
        return self.order
    @property
    def get_foods_id(self):
        return self.__orders
    @property
    def get_id(self):
        return self.__id

    def set_price(self, price):
        self.__price = price

    @property
    def get_arrive_time(self):
        return self.__arrive_time

    def add_order(self, order: Order):
        self.order.append(order)

    def set_leaving_time(self, leaving_time):
        self.__leaving_time = leaving_time


class Chef:
    def __init__(self, id):
        self.__id = id
        self.__ready_time = None
        self.orders = []

    def init_ready_time_by_base_time(self, base_time: datetime):
        self.__ready_time = base_time

    @property
    def get_ready_time(self):
        return self.__ready_time

    # def add_food(self, customer_id, duration_time):
    #     self.__work_time += duration_time
    #     self.customers.add(customer_id)

    def submit_order(self, order: Order):
        self.orders.append(order)
        self.__ready_time = order.get_ready_order_time


    def is_contain_this_customer_id(self, customer_id):
        if customer_id in self.customers:
            return True
        return False

    def reset(self):
        self.__work_time = 0
        self.customers.clear()


class Restaurant:
    def __init__(self):
        self.__foods = {}
        self.__chefs = {}
        self.__consumers = []

    def get_menu(self, data_of_menu):
        for v in data_of_menu:
            self.__foods[v['id']] = Food(v['id'], v['price'], v['cook_duration'])

    def get_chefs(self, data_of_chefs):
        for v in data_of_chefs:
            self.__chefs[v['id']] = Chef(v['id'])

    def get_consumers(self, data_of_consumers):
        for v in data_of_consumers:
            self.__consumers.append(Customer(v['id'], v['arrival_time'], v['orders']))

    def get_sorted_customers_by_arrive_time(self):
        return sorted(self.__consumers, key=operator.attrgetter('get_arrive_time'))

    def find_ready_chef(self):
        return min(self.__chefs.values(), key=operator.attrgetter('get_ready_time'))

    def get_customer_data_for_output(self):
        output = []
        for i in self.__consumers:
            output.append(i.get_dict())

        return output

    def init_all_chef_starting_time(self, start_time):
        for chef in self.__chefs.values():
            chef.init_ready_time_by_base_time(start_time)

    def submit_orders(self):
        customers = self.get_sorted_customers_by_arrive_time()
        self.init_all_chef_starting_time(customers[0].get_arrive_time)
        for customer in customers:
            for food_id in customer.get_foods_id:
                ready_chef = self.find_ready_chef()
                chef_ready_time = ready_chef.get_ready_time
                if customer.get_arrive_time > chef_ready_time:
                    chef_ready_time = customer.get_arrive_time
                order = Order(customer.get_id, self.__foods[food_id], chef_ready_time)
                ready_chef.submit_order(order)
                customer.add_order(order)

    def calculate_price(self):
        for customer in self.__consumers:
            spend_amount = sum(order.get_price for order in customer.get_orders)
            customer.set_price(spend_amount)

    def calculate_living_time(self):
        for customer in self.__consumers:
            order = max(customer.get_orders, key=operator.attrgetter('get_ready_order_time'))
            customer.set_leaving_time(order.get_ready_order_time)

class UserInterface:
    def __init__(self):
        data = self.__read_input()
        self.restuarant = Restaurant()
        self.restuarant.get_menu(data['menu'])
        self.restuarant.get_chefs(data['chefs'])
        self.restuarant.get_consumers(data['customers'])
        self.restuarant.submit_orders()
        self.restuarant.calculate_price()
        self.restuarant.calculate_living_time()
        # self.restuarant.calcute_all_consumers_price() # must delete
        # self.restuarant.calcute_leaving_duration() # must delete
        # print(self.Restuarant.get_customer_data_for_output())
        # self.Restuarant.sort_customers_by_arrive_time()

    def __read_input(self):
        return json.load(open('input.json'))

    def write_output_in_file(self):
        output={}
        output["customers"] = self.restuarant.get_customer_data_for_output()
        with open('data.json', 'w') as f:
            json.dump(output, f)


if __name__ == '__main__':
    UI = UserInterface()
    UI.write_output_in_file()