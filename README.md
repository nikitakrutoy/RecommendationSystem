# Desciption
Recomendation system for https://vc.ru. 
System could crawl, parse and save posts.
Uses linear classification model(SGD) to find intersting posts. 

## Crawler
Has a command line interface
Available commands:
update [--from][--to][--print] Refresh list of pages to download
--from - sets from date
--to - sets for date
--print - prints new posts links
download [-all][url..] download pages
-all - download all pages
urls.. - download pages with specified urls
clean - Parses html pages

## Classifier
ROC-AUC Score on ~200 samples: 0.78
Article classification/marker.py - GUI for marking news posts



# Рекомендательная система
Учебный проект.
clone of bitbucket repo https://bitbucket.org/nikitakrutoy/recommndersystem


## Описание
Целью проекта является создание рекомедательной системы для ресурса vc.ru.
Система должна:
Скачивать, обрабатывать и сохранять статьи из архива ресурса

Обладать веб интерфейсом

При помощи методов машинного обучение предлагать пользователю новые интересные для него статьи

## План разработки
### 1. crawler
Скачивает страницы с ресурса и обрабатывает их для сохранения текста статьи. Реализован на языке Python.
Используемые модули:
urllib

threading

html.parser

logging

os

glob

Доступные команды:
update [--from][--to][--print] Обновляет список страницы, которые нужно скачать
--from - устанавливает дату начала загрузки
--to - устанавливает дату конца загрузки
--print - печатает обновленные ссылки
download [-all][url..] Скачивает страницы
-all - скачивает все обновленные страницы
urls.. - скачивает представленные старницы
clean Парсит страницы
### 2. Линейный Классификатор на Python
Классифиатор будет реализован при помощи методов и функции библиотеки sklearn
### 3-4. Разметка статей и обучение классификатора. Простой сервер.
Предполагается наличие веб страницы, на которой можно будет читать новые статьи и сразу же помечать их для дальнейшего обучение классификатора.
