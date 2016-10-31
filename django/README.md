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
