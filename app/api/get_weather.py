import requests
import db.requests as requ

class HaveNotCoordinates(Exception):
    pass

def get_weather_description(weather_code):
    weather_codes = {
        # Чистое небо
        0: 'Чистое небо',
        
        # Преимущественно ясно, переменная облачность, пасмурно
        1: 'Преимущественно ясно',
        2: 'Переменная облачность',
        3: 'Пасмурно',
        
        # Туман и отложенный изморозный туман
        45: 'Туман',
        48: 'Изморозный туман',
        
        # Морось
        51: 'Морось: легкая интенсивность',
        53: 'Морось: умеренная интенсивность',
        55: 'Морось: плотная интенсивность',
        
        # Ледяной дождь
        56: 'Ледяной дождь: легкий',
        57: 'Ледяной дождь: плотный',
        
        # Дождь
        61: 'Дождь: небольшая интенсивность',
        63: 'Дождь: умеренная интенсивность',
        65: 'Дождь: сильная интенсивность',
        
        # Ледяной дождь (дополнительные)
        66: 'Ледяной дождь: легкий',
        67: 'Ледяной дождь: сильный',
        
        # Снегопад
        71: 'Снегопад: небольшая интенсивность',
        73: 'Снегопад: умеренная интенсивность',
        75: 'Снегопад: сильная интенсивность',
        
        # Град
        77: 'Град',
        
        # Ливневые дожди
        80: 'Ливневые дожди: слабые',
        81: 'Ливневые дожди: умеренные',
        82: 'Ливневые дожди: сильные',
        
        # Снегопад (дополнительные)
        85: 'Снегопад: слабый',
        86: 'Снегопад: сильный',
        
        # Гроза
        95: 'Гроза: слабая или умеренная',
        96: 'Гроза с небольшим градом',
        99: 'Гроза с сильным градом'
    }
    
    return weather_codes.get(weather_code, 'Неизвестный код погоды')

async def get_weather_forecast(user):
    # Surgut
	# longitude = 73.4177
	# latitude = 61.2576
    coordinates = await requ.get_user_coordinates(user)
    longitude = coordinates['longitude']
    latitude = coordinates['latitude']
    if latitude or longitude:
        try:
            response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=Europe%2FMoscow&forecast_days=1')
            weather_code = int(response.json()['daily']['weather_code'][0])
            weather_code_to_name = get_weather_description(weather_code)
            # и так далее
            weather = {'min_temp': response.json()['daily']['temperature_2m_min'][0],
                    'max_temp': response.json()['daily']['temperature_2m_max'][0],
                    'name': weather_code_to_name}
            return weather
        except Exception as e:
            print(f'Ошибка при получении погоды {e}')
            raise HaveNotCoordinates('У нас произошла ошибка, наши разработчики уже были оповещены об этом, желаем вам удачного использования нашего продукта и просим прощения')
    else:
        raise HaveNotCoordinates('У вас не указаны координаты, в связи с этим мы не можем получить для вас погоду...')

