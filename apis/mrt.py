from flask import Blueprint, jsonify

from views.mrt import MrtDataProcessor
from models.mrt import MrtDataFetcher

mrt = Blueprint('mrt', __name__)

# 取得捷運站列表
@mrt.route('/api/mrts')
def api_mrts():
    response, status_code = MrtDataFetcher.get_mrt_data()
    if status_code != 200:
        return jsonify(response), status_code
    else:
        processed_data = MrtDataProcessor.process_mrt_data(response)
        return jsonify(processed_data)