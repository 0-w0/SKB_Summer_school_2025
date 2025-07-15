# О проекте

Данный репозиторий содержит код к занятиям по компьютерному зрению.
Файлы под именем lesson*.py содержат материялы к соответствующим лекциям.

# Что такое app.py
Файл app.py представляет собой paint от мира компьютерного зрения.

Запустите код, чтобы рисовать прямо на динамическом изображении с камеры.

Вы можете:
* Рисовать
* Использовать ластик
* Очищать весь холст
* Сохранять текущее изображение

Для того, чтобы использовать рисование/ластик просто соедините большой и указательный палец так, будто бы вы что-то держите.

### Установка

Для запуска необходимо установить некоторые библиотеки, названия и версии которых, находятся в файле requirements.py.
Для этого необходимо выполнить следующую команду в терминале:

```bash
pip3 install -r requirements.txt
```

Также необходимо загрузить файлы предобученных сетей:

* Каскады хаара для фронтальных лиц: <a href=https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml>ссылка</a>
* Распознавание рук: <a href=https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task>ссылка</a>
* Распознавание жестов: <a href=https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/latest/gesture_recognizer.task>ссылка</a>