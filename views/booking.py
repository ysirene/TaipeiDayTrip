from datetime import date

class BookingDataProcessor:

    @staticmethod
    def process_booking_data(data):
        if data == None:
            return {'data': None}
        else:
            attraction_data = {
                'id': data[2],
                'name': data[6],
                'address': data[7],
                'image': data[8]
            }
            data = {
                'attraction': attraction_data,
                'date': data[3],
                'time': data[4],
                'price': data[5]
            }
            return {'data': data}
        
class BookingDataChecker:

    @staticmethod
    def _is_booking_date_later_then_today(booking_date):
        booking_date = [int(i) for i in booking_date.split('-')]
        booking_date = date(booking_date[0], booking_date[1], booking_date[2])
        today = date.today()
        if booking_date > today:
            return True
        else:
            return False

    @staticmethod
    def _is_time_correct(booking_time):
        valid_time = ['forenoon', 'afternoon']
        if booking_time in valid_time:
            return True
        else:
            return False
        
    @staticmethod
    def _is_price_correct(booking_time, booking_price):
        menu = {
            'forenoon': 2000,
            'afternoon': 2500
        }
        if booking_price == menu[booking_time]:
            return True
        else:
            return False
        
    @staticmethod
    def check_input_data(date, time, price):
        check_date = BookingDataChecker._is_booking_date_later_then_today(date)
        check_time = BookingDataChecker._is_time_correct(time)
        check_price = BookingDataChecker._is_price_correct(time, price)
        if check_date and check_time and check_price:
            return {'ok': True}, 200
        else:
            return {'error': True, 'message': 'incorrect input'}, 400
