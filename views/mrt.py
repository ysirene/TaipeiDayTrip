class MrtDataProcessor:

    @staticmethod
    def process_mrt_data(data):
        processed_data = [item[0] for item in data]
        return {'data': processed_data}