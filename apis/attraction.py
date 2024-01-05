from flask import Blueprint, request, jsonify

from views.attraction import AttractionDataProcessor
from models.attraction import AttractionDataFetcher

attraction = Blueprint('attraction', __name__)

# 首頁取得景點資訊
@attraction.route('/api/attractions')
def api_attractions():
	keyword = request.args.get('keyword', '')
	try:
		page = int(request.args.get('page', 0))
	except ValueError:
		return jsonify({'error': True, 'message': 'invalid page number'}), 400
	response, status_code = AttractionDataFetcher.get_index_attractions(keyword, page)
	if status_code != 200:
		return jsonify(response), status_code
	else:
		processed_data = AttractionDataProcessor.process_index_attractions_data(page, response)
		return jsonify(processed_data)

# 取得特定id的景點資訊
@attraction.route('/api/attraction/<attractionId>')
def api_attraction_id(attractionId):
	try:
		attraction_id = int(attractionId)
	except ValueError:
		return jsonify({'error': True, 'message': 'invalid attraction number'}), 400
	response, status_code = AttractionDataFetcher.get_specific_attraction(attraction_id)
	if status_code != 200:
		return jsonify(response), status_code
	else:
		processed_data = AttractionDataProcessor.process_specific_attraction_data(response)
		return jsonify(processed_data)