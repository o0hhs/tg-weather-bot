import requests

def get():
	try:
		response = requests.get('https://api.thecatapi.com/v1/images/search')
		return response.json()[0]['url']
	except Exception as ex:
		print(f'Произошла ошибка: {ex}')