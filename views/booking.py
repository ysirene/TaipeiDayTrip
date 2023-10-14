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