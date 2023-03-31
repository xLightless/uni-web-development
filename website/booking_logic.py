from website.database import Database
from datetime import datetime


database = Database(database="ht_database", user="root", password="Password1")

# {
#   'location_from': 'Newcastle',
#   'location_to': 'Bristol',
#   'passengers_amount': '5',
#   'seat_class_type': 'Business',
#   'date_from': '2023-03-31',
#   'date_to': '2023-03-31',
#   'departure_time': datetime.timedelta(seconds=60300),
#   'return_time': datetime.timedelta(seconds=64800)
# }

### Booking cancellation logic
# cancellation_grace_period(60 days) - day_of_purchase = time_difference
# time_difference >= 30 and time_difference <= cancellation_grace_period = 0.50% cancellation charge
# time_difference < 30 = 100% cancellation charge

### Price logic for non-special locations
# if not special location
# discounted_days = date_from - day_of_purchase
# discount_percentage = 
#
#   if (discounted_days >= 45) and (discounted_days <= 59) = 0.05%
#   if (discounted_days >= 60) and (discounted_days <= 79) = 0.10%
#   if (discounted_days >= 80) and (discounted_days <= 90) = 0.15%
#
# total_price = journey_price * passengers * seat_type - discount_percentage

class Booking(object):
    """
    
    This booking object is designed to handle payment pre-processing and update the user about important information.

    Args:
        booking_data (dict): a dictionary of data to process
    """

    def __init__(
        self,
        booking_data:dict
    ):
        # Place booking search into dict object
        self.booking_data = booking_data
        self.return_trip = False
        
        # Format date time
        today = str(datetime.now().date()).replace('-','/')
        travel_day = str(self.booking_data['date_from']).replace('-', '/')
        todays_date = datetime.strptime(today, "%Y/%m/%d")
        travel_date = datetime.strptime(travel_day, "%Y/%m/%d")
        
        # Discounted time difference. discounted_days = date_of_travel - day_of_purchase
        self.timedelta = travel_date - todays_date
    
    def get_booking_discount(self):
        """ Number of days in advance booking Discount % on total booking price:
            
            - Between 80 and 90 days 20%
            - Between 60 and 79 days 10%
            - Between 45 and 59 days 5%
            - Under 45 days No discount
        
        """
        
        if (self.timedelta.days >= 45) and (self.timedelta.days <= 59):
            discount = 0.05
        elif (self.timedelta.days >= 60) and (self.timedelta.days <= 79):
            discount = 0.10
        elif (self.timedelta.days >= 80) and (self.timedelta.days <= 90):
            discount = 0.20
        else:
            discount = 0
            
        return discount
            
    def get_price(self):
        """ Get the total price of the booking
        
            Also, Air travel uses a fixed fare for each journey. Standard seat fares are:
            
            - Dundee-Portsmouth (or v.v.) £100
            - Bristol-Manchester (or v.v.) £60
            - Bristol-Newcastle (or v.v.) £80
            - Bristol-Glasgow (or v.v.) £90
            - Bristol-London (or v.v.) £60
            - Manchester-Southampton £70
            - Cardiff-Edinburgh £80
            - All other routes are charged at: £75
            
            If the trip is a return then the price would be the 'route * 2 = price'

        """
        
        # total_price = journey_price * passengers * seat_type - discount_percentage
        
        passengers = int(self.booking_data['passengers_amount'])
        seat_type = self.booking_data['seat_class_type']
        location_from = self.booking_data['location_from']
        location_to = self.booking_data['location_to']
        
        self.journey_price = 75 # GBP
        
        # Check if user is going to these locations
        if (location_from == 'Dundee') and (location_to == 'Portsmouth'):self.journey_price         = 100.00
        elif (location_from == 'Bristol') and (location_to == 'Manchester'): self.journey_price     = 60.00
        elif (location_from == 'Bristol') and (location_to == 'Newcastle'): self.journey_price      = 80.00
        elif (location_from == 'Bristol') and (location_to == 'Glasgow'): self.journey_price        = 90.00
        elif (location_from == 'Bristol') and (location_to == 'London'): self.journey_price         = 60.00
        elif (location_from == 'Manchester') and (location_to == 'Southampton'): self.journey_price = 70.00
        elif (location_from == 'Cardiff') and (location_to == 'Edinburgh'): self.journey_price      = 80.00
        
        # If user is business class fare is twice as much
        if (seat_type == 'Business'): self.journey_price = self.journey_price * 2
        
        # Multiply price by number of passengers
        self.journey_price = self.journey_price * passengers
        
        # Apply discount if advanced booked
        discount = self.get_booking_discount() * self.journey_price
        self.journey_price = self.journey_price - discount
        
        return self.journey_price if self.return_trip == False else self.journey_price * 2
        
    
    def get_time_difference(self): pass
    
    
# data = {
#     'location_from': 'Bristol',
#     'location_to' : 'Manchester',
#     'passengers_amount' : '1',
#     'seat_class_type' : 'Economy',
#     'date_from' : '2023-06-27'
# }
# b = Booking(data)

# b.return_trip = False

# print(b.get_price())
# # print(b.return_trip)