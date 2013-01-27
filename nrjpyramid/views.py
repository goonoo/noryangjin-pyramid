from pyramid.view import view_config
import json
import datetime
import pymongo

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
	today = datetime.date.today()
	pricesTable = request.db['prices']
	#list = prices.find()

	config_data = open('nrjpyramid/config.json')
	config = json.load(config_data)
	fishes = config["fishes"]
	fishList = []

	for fishItem in fishes:
		dataList = list(pricesTable.find({"name": fishItem["alias"]}).sort("ymd,pymongo.DESCENDING").limit(6))
		dataSize = len(dataList)
		if dataSize >= 2:
			changes = dataList[0]['price'] - dataList[1]['price']
			dataChanges = (changes > 0 and '+' or '') + str(changes)
		else:
			dataChanges = ''

		fishList.append({
			'info': fishItem,
			'dataList': dataList,
			'changes': dataChanges
		})

	return {
		'today': today,
		'fishList': fishList
	}

@view_config(route_name='sise', renderer='templates/sise.pt')
def sise(request):
	name = request.matchdict['name']
	today = datetime.date.today()
	pricesTable = request.db['prices']
	prices = pricesTable.find({"name": name}, sort=[("ymd", pymongo.DESCENDING)]).limit(10)
	price = prices[0]
	prevPrice = prices[1]
	priceChange = price["price"] - prevPrice["price"]

	config_data = open('nrjpyramid/config.json')
	config = json.load(config_data)
	fishes = config["fishes"]

	for fishItem in fishes:
		if fishItem["alias"] == name:
			fish = fishItem
			break

	return {
		'name': price["name"],
		'today': today,
		'prices': prices,
		'price': price["price"],
		'priceChange': (priceChange > 0 and '+' or '') + str(priceChange),
		'fihses': fishes,
		'fish': fish
	}
