# Лабораторна робота #2

## Завдання
1. Розробити схему бази даних на основі предметної галузі з ЛР№2-Ч1 у
спосіб, що застосовується в СУБД MongoDB.
2. Розробити модуль роботи з базою даних на основі пакету PyMongo.
3. Реалізувати дві операції на вибір із використанням паралельної обробки
даних Map/Reduce.
4. Реалізувати обчислення та виведення результату складного агрегативного
запиту до бази даних з використанням функції aggregate() сервера
MongoDB.

### Варіант
Основна сутність - фото. Є додаткові сутності фотограф (окрема коллекція), камера та локація (вкладені в фото).

## Коди функцій Map/Reduce та aggregate()
Перший Map/Reduce: середній діаметр діафрагми у кожного фотографа:
```{javascript}
map:
      function() {
        if ("aperture" in this) {
          emit(this.photographer, this.aperture);
        }
      }
reduce:
      function(k, vs) {
        return Array.sum(vs) / vs.length;
      }
```
Другий Map/Reduce: кількість фото у кожного фотографа:
```{javascript}
map:
      function() {
        emit(this.photographer, 1);
      }
reduce:
      function(k, vs) {
        return Array.sum(vs);
      }
```
Агрегація: фотоапарати, якими користувалися хоча б 2 рази, відсортовані за кількістю фотографів, які їми користувалися.
```{python}
      { "$group": { "_id" : "$photographer", "cameras": {"$addToSet": "$camera"} } },
      { "$project": { "_id": 1, "cameras": 1, "ccount": { "$gt" : [ { "$size" : "$cameras" }, 1 ] } } },
      { "$match": { "ccount" : True } },
      { "$unwind": "$cameras" },
      { "$group": { "_id": "$cameras", "phs": {"$addToSet": "$_id"} } },
      { "$project": { "_id": 1, "phs": 1, "phcount": {"$size": "$phs"} } },
      { "$sort": SON([("phcount", -1), ("_id.name", 1)]) }
```

# Лабораторна робота #3

## Завдання
1. Встановити сервер redis.
2. Розробити модуль кешування на основі пакету redis-py.
3. Підготувати тестові дані (50-100тис. документів MongoDB).
4. Реалізувати збереження результатів пошуку в базі даних redis (створити
кеш).
5. Реалізувати функцію отримання результатів пошуку з кешу, у випадку,
коли основна база даних не оновлювалась до створення кешу

## Реалізація
### Пошук
В базі зберігаються 2 колекції, пошук реалізован для `photo` через текстовий індекс:
```{javascript}
    {
        "v" : 1,
        "key" : {
            "_fts" : "text",
            "_ftsx" : 1
        },
        "name" : "name_text_camera.name_text_location.name_text",
        "ns" : "photo.photo",
        "weights" : {
            "camera.name" : 1,
            "location.name" : 1,
            "name" : 1
        },
        "default_language" : "english",
        "language_override" : "language",
        "textIndexVersion" : 3
    }
```
Тобто шукається співпадіння серед назв фотографії, камери та локації.

В redis зберігаються результати запитів користувача, які мають форму `?search=...&page=...`. Тому ключ у redis має форму ```{python} 'search: &%s& page: %d' % (search_query, page)```. При зміні або видаленні елемента виконується пошук серед ключів, в яких пошуковий запит задовільняє цьому елементу, і інвалідується кеш для них.
```{python}
  @staticmethod
  def _invalidate_item(str_id):
    for rkey in redis_instance.keys('search:*'):
      search = rkey.split('&')[1]
      if mongo_client.photo.photo.find_one({'_id': ObjectId(str_id),
                                            '$text': {'$search': search}}):
        redis_instance.delete(rkey)
```

### Сторінки в даних
Також redis використовується для кешування запитів сторінок у нефільтрованих даних для зменшення часу відгуку при великих значеннях `skip()` у MongoDB. У разі будь-якої зміни в базі даних весь сторінковий кеш інвалідується.
```{python}
    pages = redis_instance.keys('page:*')
    redis_instance.delete(*pages)
```
