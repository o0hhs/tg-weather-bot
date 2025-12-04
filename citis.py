from app.db.requests import create_new_city
import asyncio

cities = [
  {
    "title_en": "Abakan",
    "title_ru": "Абакан",
    "longitude": 91.4292,
    "latitude": 53.7224
  },
  {
    "title_en": "Angarsk",
    "title_ru": "Ангарск",
    "longitude": 103.886,
    "latitude": 52.5317
  },
  {
    "title_en": "Armavir",
    "title_ru": "Армавир",
    "longitude": 41.1194,
    "latitude": 45.0015
  },
  {
    "title_en": "Arkhangelsk",
    "title_ru": "Архангельск",
    "longitude": 40.5158,
    "latitude": 64.5459
  },
  {
    "title_en": "Astrakhan",
    "title_ru": "Астрахань",
    "longitude": 48.0336,
    "latitude": 46.3497
  },
  {
    "title_en": "Balašiha",
    "title_ru": "Балашиха",
    "longitude": 37.9581,
    "latitude": 55.8094
  },
  {
    "title_en": "Balakovo",
    "title_ru": "Балаково",
    "longitude": 47.7821,
    "latitude": 52.039
  },
  {
    "title_en": "Balashikha",
    "title_ru": "Балашиха",
    "longitude": 37.9581,
    "latitude": 55.8094
  },
  {
    "title_en": "Barnaul",
    "title_ru": "Барнаул",
    "longitude": 83.7699,
    "latitude": 53.347
  },
  {
    "title_en": "Belgorod",
    "title_ru": "Белгород",
    "longitude": 36.5802,
    "latitude": 50.5975
  },
  {
    "title_en": "Berezniki",
    "title_ru": "Березники",
    "longitude": 56.8084,
    "latitude": 59.4081
  },
  {
    "title_en": "Biysk",
    "title_ru": "Бийск",
    "longitude": 85.2072,
    "latitude": 52.5393
  },
  {
    "title_en": "Bratsk",
    "title_ru": "Братск",
    "longitude": 101.614,
    "latitude": 56.1514
  },
  {
    "title_en": "Bryansk",
    "title_ru": "Брянск",
    "longitude": 34.3638,
    "latitude": 53.2434
  },
  {
    "title_en": "Cheboksary",
    "title_ru": "Чебоксары",
    "longitude": 47.2511,
    "latitude": 56.1463
  },
  {
    "title_en": "Chelyabinsk",
    "title_ru": "Челябинск",
    "longitude": 61.4026,
    "latitude": 55.1644
  },
  {
    "title_en": "Cherepovets",
    "title_ru": "Череповец",
    "longitude": 37.9063,
    "latitude": 59.1274
  },
  {
    "title_en": "Chita",
    "title_ru": "Чита",
    "longitude": 113.501,
    "latitude": 52.0339
  },
  {
    "title_en": "Dmitrov",
    "title_ru": "Дмитров",
    "longitude": 37.5217,
    "latitude": 56.3469
  },
  {
    "title_en": "Dzerzhinsk",
    "title_ru": "Дзержинск",
    "longitude": 43.4628,
    "latitude": 56.2377
  },
  {
    "title_en": "Engels",
    "title_ru": "Энгельс",
    "longitude": 46.1256,
    "latitude": 51.4989
  },
  {
    "title_en": "Grozny",
    "title_ru": "Грозный",
    "longitude": 45.6949,
    "latitude": 43.3178
  },
  {
    "title_en": "Irkutsk",
    "title_ru": "Иркутск",
    "longitude": 104.281,
    "latitude": 52.2864
  },
  {
    "title_en": "Ivanovo",
    "title_ru": "Иваново",
    "longitude": 40.9766,
    "latitude": 57.0004
  },
  {
    "title_en": "Izhevsk",
    "title_ru": "Ижевск",
    "longitude": 53.2048,
    "latitude": 56.8528
  },
  {
    "title_en": "Kaliningrad",
    "title_ru": "Калининград",
    "longitude": 20.5109,
    "latitude": 54.7104
  },
  {
    "title_en": "Kaluga",
    "title_ru": "Калуга",
    "longitude": 36.2615,
    "latitude": 54.5136
  },
  {
    "title_en": "Kamensk-Uralsky",
    "title_ru": "Каменск-Уральский",
    "longitude": 61.9329,
    "latitude": 56.4149
  },
  {
    "title_en": "Kazan",
    "title_ru": "Казань",
    "longitude": 49.1088,
    "latitude": 55.7963
  },
  {
    "title_en": "Kemerovo",
    "title_ru": "Кемерово",
    "longitude": 86.0873,
    "latitude": 55.3547
  },
  {
    "title_en": "Khabarovsk",
    "title_ru": "Хабаровск",
    "longitude": 135.072,
    "latitude": 48.4802
  },
  {
    "title_en": "Khasavyurt",
    "title_ru": "Хасавюрт",
    "longitude": 46.588,
    "latitude": 43.2505
  },
  {
    "title_en": "Khimki",
    "title_ru": "Химки",
    "longitude": 37.4386,
    "latitude": 55.897
  },
  {
    "title_en": "Kirov",
    "title_ru": "Киров",
    "longitude": 49.668,
    "latitude": 58.6035
  },
  {
    "title_en": "Kolomna",
    "title_ru": "Коломна",
    "longitude": 38.7686,
    "latitude": 55.0794
  },
  {
    "title_en": "Komsomolsk-on-Amur",
    "title_ru": "Комсомольск-на-Амуре",
    "longitude": 137.015,
    "latitude": 50.5503
  },
  {
    "title_en": "Kopeysk",
    "title_ru": "Копейск",
    "longitude": 61.6798,
    "latitude": 55.1172
  },
  {
    "title_en": "Korolyov",
    "title_ru": "Королёв",
    "longitude": 37.8256,
    "latitude": 55.9163
  },
  {
    "title_en": "Kostroma",
    "title_ru": "Кострома",
    "longitude": 40.9269,
    "latitude": 57.7677
  },
  {
    "title_en": "Krasnodar",
    "title_ru": "Краснодар",
    "longitude": 38.975,
    "latitude": 45.0355
  },
  {
    "title_en": "Krasnoyarsk",
    "title_ru": "Красноярск",
    "longitude": 92.8678,
    "latitude": 56.0153
  },
  {
    "title_en": "Kurgan",
    "title_ru": "Курган",
    "longitude": 65.3136,
    "latitude": 55.441
  },
  {
    "title_en": "Kursk",
    "title_ru": "Курск",
    "longitude": 36.1933,
    "latitude": 51.7304
  },
  {
    "title_en": "Lipetsk",
    "title_ru": "Липецк",
    "longitude": 39.5704,
    "latitude": 52.6088
  },
  {
    "title_en": "Magnitogorsk",
    "title_ru": "Магнитогорск",
    "longitude": 58.9798,
    "latitude": 53.4071
  },
  {
    "title_en": "Makhachkala",
    "title_ru": "Махачкала",
    "longitude": 47.5047,
    "latitude": 42.9831
  },
  {
    "title_en": "Maykop",
    "title_ru": "Майкоп",
    "longitude": 40.1064,
    "latitude": 44.6078
  },
  {
    "title_en": "Moscow",
    "title_ru": "Москва",
    "longitude": 37.6173,
    "latitude": 55.7558
  },
  {
    "title_en": "Murmansk",
    "title_ru": "Мурманск",
    "longitude": 33.0827,
    "latitude": 68.9707
  },
  {
    "title_en": "Mytishchi",
    "title_ru": "Мытищи",
    "longitude": 37.7337,
    "latitude": 55.9116
  },
  {
    "title_en": "Naberezhnye Chelny",
    "title_ru": "Набережные Челны",
    "longitude": 52.4289,
    "latitude": 55.7436
  },
  {
    "title_en": "Nalchik",
    "title_ru": "Нальчик",
    "longitude": 43.6185,
    "latitude": 43.4853
  },
  {
    "title_en": "Nizhnevartovsk",
    "title_ru": "Нижневартовск",
    "longitude": 76.5696,
    "latitude": 60.9397
  },
  {
    "title_en": "Nizhny Novgorod",
    "title_ru": "Нижний Новгород",
    "longitude": 44.002,
    "latitude": 56.2965
  },
  {
    "title_en": "Nizhny Tagil",
    "title_ru": "Нижний Тагил",
    "longitude": 59.9675,
    "latitude": 57.9101
  },
  {
    "title_en": "Norilsk",
    "title_ru": "Норильск",
    "longitude": 88.2027,
    "latitude": 69.349
  },
  {
    "title_en": "Novocherkassk",
    "title_ru": "Новочеркасск",
    "longitude": 40.0939,
    "latitude": 47.418
  },
  {
    "title_en": "Novokuznetsk",
    "title_ru": "Новокузнецк",
    "longitude": 87.115,
    "latitude": 53.7596
  },
  {
    "title_en": "Novorossiysk",
    "title_ru": "Новороссийск",
    "longitude": 37.7773,
    "latitude": 44.7235
  },
  {
    "title_en": "Novosibirsk",
    "title_ru": "Новосибирск",
    "longitude": 82.9346,
    "latitude": 55.0084
  },
  {
    "title_en": "Odintsovo",
    "title_ru": "Одинцово",
    "longitude": 37.2757,
    "latitude": 55.678
  },
  {
    "title_en": "Omsk",
    "title_ru": "Омск",
    "longitude": 73.3686,
    "latitude": 54.9893
  },
  {
    "title_en": "Orenburg",
    "title_ru": "Оренбург",
    "longitude": 55.0968,
    "latitude": 51.7872
  },
  {
    "title_en": "Orsk",
    "title_ru": "Орск",
    "longitude": 58.4582,
    "latitude": 51.2049
  },
  {
    "title_en": "Penza",
    "title_ru": "Пенза",
    "longitude": 45.0004,
    "latitude": 53.1951
  },
  {
    "title_en": "Perm",
    "title_ru": "Пермь",
    "longitude": 56.2294,
    "latitude": 58.0105
  },
  {
    "title_en": "Petropavlovsk-Kamchatsky",
    "title_ru": "Петропавловск-Камчатский",
    "longitude": 158.651,
    "latitude": 53.0377
  },
  {
    "title_en": "Petrozavodsk",
    "title_ru": "Петрозаводск",
    "longitude": 34.3468,
    "latitude": 61.7849
  },
  {
    "title_en": "Podolsk",
    "title_ru": "Подольск",
    "longitude": 37.5446,
    "latitude": 55.4311
  },
  {
    "title_en": "Pskov",
    "title_ru": "Псков",
    "longitude": 28.3417,
    "latitude": 57.8194
  },
  {
    "title_en": "Pyatigorsk",
    "title_ru": "Пятигорск",
    "longitude": 43.0594,
    "latitude": 44.0416
  },
  {
    "title_en": "Rostov-on-Don",
    "title_ru": "Ростов-на-Дону",
    "longitude": 39.7139,
    "latitude": 47.2357
  },
  {
    "title_en": "Rubtsovsk",
    "title_ru": "Рубцовск",
    "longitude": 81.233,
    "latitude": 51.5147
  },
  {
    "title_en": "Ryazan",
    "title_ru": "Рязань",
    "longitude": 39.7126,
    "latitude": 54.6269
  },
  {
    "title_en": "Saint Petersburg",
    "title_ru": "Санкт-Петербург",
    "longitude": 30.3359,
    "latitude": 59.9343
  },
  {
    "title_en": "Salavat",
    "title_ru": "Салават",
    "longitude": 55.9077,
    "latitude": 53.3616
  },
  {
    "title_en": "Samara",
    "title_ru": "Самара",
    "longitude": 50.2212,
    "latitude": 53.2415
  },
  {
    "title_en": "Saratov",
    "title_ru": "Саратов",
    "longitude": 46.0342,
    "latitude": 51.5924
  },
  {
    "title_en": "Severodvinsk",
    "title_ru": "Северодвинск",
    "longitude": 39.8302,
    "latitude": 64.5635
  },
  {
    "title_en": "Shakhty",
    "title_ru": "Шахты",
    "longitude": 40.2054,
    "latitude": 47.7085
  },
  {
    "title_en": "Smolensk",
    "title_ru": "Смоленск",
    "longitude": 32.0453,
    "latitude": 54.7826
  },
  {
    "title_en": "Sochi",
    "title_ru": "Сочи",
    "longitude": 39.7303,
    "latitude": 43.5855
  },
  {
    "title_en": "Stary Oskol",
    "title_ru": "Старый Оскол",
    "longitude": 37.8416,
    "latitude": 51.2981
  },
  {
    "title_en": "Stavropol",
    "title_ru": "Ставрополь",
    "longitude": 41.9693,
    "latitude": 45.0428
  },
  {
    "title_en": "Sterlitamak",
    "title_ru": "Стерлитамак",
    "longitude": 55.944,
    "latitude": 53.6303
  },
  {
    "title_en": "Surgut",
    "title_ru": "Сургут",
    "longitude": 73.3964,
    "latitude": 61.2541
  },
  {
    "title_en": "Syktyvkar",
    "title_ru": "Сыктывкар",
    "longitude": 50.8364,
    "latitude": 61.6688
  },
  {
    "title_en": "Syzran",
    "title_ru": "Сызрань",
    "longitude": 48.4682,
    "latitude": 53.1585
  },
  {
    "title_en": "Taganrog",
    "title_ru": "Таганрог",
    "longitude": 38.9007,
    "latitude": 47.2362
  },
  {
    "title_en": "Tambov",
    "title_ru": "Тамбов",
    "longitude": 41.4335,
    "latitude": 52.7212
  },
  {
    "title_en": "Tolyatti",
    "title_ru": "Тольятти",
    "longitude": 49.3468,
    "latitude": 53.5088
  },
  {
    "title_en": "Tomsk",
    "title_ru": "Томск",
    "longitude": 84.948,
    "latitude": 56.4846
  },
  {
    "title_en": "Tula",
    "title_ru": "Тула",
    "longitude": 37.6184,
    "latitude": 54.193
  },
  {
    "title_en": "Tver",
    "title_ru": "Тверь",
    "longitude": 35.9119,
    "latitude": 56.8587
  },
  {
    "title_en": "Tyumen",
    "title_ru": "Тюмень",
    "longitude": 65.5343,
    "latitude": 57.1613
  },
  {
    "title_en": "Ufa",
    "title_ru": "Уфа",
    "longitude": 55.9865,
    "latitude": 54.7351
  },
  {
    "title_en": "Ulan-Ude",
    "title_ru": "Улан-Удэ",
    "longitude": 107.58,
    "latitude": 51.8345
  },
  {
    "title_en": "Ulyanovsk",
    "title_ru": "Ульяновск",
    "longitude": 48.3896,
    "latitude": 54.3142
  },
  {
    "title_en": "Ussuriysk",
    "title_ru": "Уссурийск",
    "longitude": 131.952,
    "latitude": 43.7974
  },
  {
    "title_en": "Veliky Novgorod",
    "title_ru": "Великий Новгород",
    "longitude": 31.2758,
    "latitude": 58.5256
  },
  {
    "title_en": "Vladikavkaz",
    "title_ru": "Владикавказ",
    "longitude": 44.6674,
    "latitude": 43.0305
  },
  {
    "title_en": "Vladimir",
    "title_ru": "Владимир",
    "longitude": 40.3966,
    "latitude": 56.129
  },
  {
    "title_en": "Vladivostok",
    "title_ru": "Владивосток",
    "longitude": 131.885,
    "latitude": 43.1155
  },
  {
    "title_en": "Volgodonsk",
    "title_ru": "Волгодонск",
    "longitude": 42.1514,
    "latitude": 47.5165
  },
  {
    "title_en": "Volgograd",
    "title_ru": "Волгоград",
    "longitude": 44.5168,
    "latitude": 48.708
  },
  {
    "title_en": "Volzhsky",
    "title_ru": "Волжский",
    "longitude": 44.7794,
    "latitude": 48.7858
  },
  {
    "title_en": "Voronezh",
    "title_ru": "Воронеж",
    "longitude": 39.2003,
    "latitude": 51.672
  },
  {
    "title_en": "Yekaterinburg",
    "title_ru": "Екатеринбург",
    "longitude": 60.6122,
    "latitude": 56.8389
  },
  {
    "title_en": "Yaroslavl",
    "title_ru": "Ярославль",
    "longitude": 39.8931,
    "latitude": 57.6261
  },
  {
    "title_en": "Yoshkar-Ola",
    "title_ru": "Йошкар-Ола",
    "longitude": 47.8907,
    "latitude": 56.632
  },
  {
    "title_en": "Yuzhno-Sakhalinsk",
    "title_ru": "Южно-Сахалинск",
    "longitude": 142.738,
    "latitude": 46.9591
  },
  {
    "title_en": "Zelenograd",
    "title_ru": "Зеленоград",
    "longitude": 37.1815,
    "latitude": 55.9825
  },
  {
    "title_en": "Zlatoust",
    "title_ru": "Златоуст",
    "longitude": 59.6508,
    "latitude": 55.1711
  }
]
number = 1
async def main():
  for city in cities:
    global number
    number =+ 1
    print(number)
    await create_new_city(title_en=city['title_en'], title_ru=city["title_ru"], longitude=city["longitude"], latitude=city['latitude'])
    
if __name__ == '__main__':
  asyncio.run(main())