class AttractionDataProcessor:

    @staticmethod
    def process_index_attractions_data(page, data):
        processed_data = []
        next_page = page + 1 if len(data) == 13 else None
        loop_len = 12 if len(data) >= 12 else len(data)
        for i in range(loop_len):
                tmp_dic = {}
                tmp_dic['id'] = data[i][0]
                tmp_dic['name'] = data[i][1]
                tmp_dic['category'] = data[i][9]
                tmp_dic['description'] = data[i][3]
                tmp_dic['address'] = data[i][4]
                tmp_dic['transport'] = data[i][5]
                tmp_dic['mrt'] = None if data[i][10]=='None' else data[i][10]
                tmp_dic['lat'] = data[i][7]
                tmp_dic['lng'] = data[i][8]
                tmp_dic['images'] = data[i][11].split(',')
                processed_data.append(tmp_dic)
        return {'nextPage': next_page, 'data': processed_data}
    
    @staticmethod
    def process_specific_attraction_data(data):
        processed_data = {}
        processed_data['id'] = data[0]
        processed_data['name'] = data[1]
        processed_data['category'] = data[9]
        processed_data['description'] = data[3]
        processed_data['address'] = data[4]
        processed_data['transport'] = data[5]
        processed_data['mrt'] = data[10]
        processed_data['lat'] = data[7]
        processed_data['lng'] = data[8]
        processed_data['images'] = data[11].split(',')
        return {'data': processed_data}