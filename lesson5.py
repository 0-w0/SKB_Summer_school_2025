# --- ШАГ 1: ПОДКЛЮЧЕНИЕ БИБЛИОТЕК ---
import cv2
import mediapipe as mp # Подключаем "коробку с нейросетями" MediaPipe

# --- ШАГ 2: ИНИЦИАЛИЗАЦИЯ MEDIAPIPE ---
# MediaPipe предоставляет готовые "инструменты". Мы берем два:
# 1. Инструмент для поиска лиц
mp_face_detection = mp.solutions.face_detection
# 2. Инструмент для рисования результатов
mp_drawing = mp.solutions.drawing_utils

# Подключаемся к веб-камере
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Ошибка: не удалось открыть веб-камеру.")
    exit()

# --- ШАГ 3: ЗАПУСКАЕМ НЕЙРОСЕТЬ В ЦИКЛЕ ---
# Создаем "экземпляр" нашего детектора лиц.
# min_detection_confidence=0.5 означает, что мы считаем лицом только то,
# в чем нейросеть уверена как минимум на 50%.
with mp_face_detection.FaceDetection(
    min_detection_confidence=0.5) as face_detection:

    # Наш знакомый "бесконечный конвейер"
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр с камеры.")
            break

        # 1. ПОДГОТОВКА КАДРА
        # MediaPipe лучше работает с RGB-изображениями, а OpenCV дает нам BGR.
        # Конвертируем цвета перед отправкой в нейросеть.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 2. ДЕТЕКЦИЯ!
        # Отправляем кадр в нейросеть. Это самая главная строка.
        results = face_detection.process(rgb_frame)

        # 3. ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ
        # Проверяем, нашла ли нейросеть что-нибудь.
        if results.detections:
            # Если да, то для каждого найденного лица...
            for detection in results.detections:
                # ...используем готовый инструмент MediaPipe для рисования.
                # Он сам нарисует и рамку, и ключевые точки (глаза, нос, рот, уши).
                mp_drawing.draw_detection(frame, detection)

        # Показываем результат в окне.
        cv2.imshow('MediaPipe Face Detection', frame)

        # Выход по нажатию 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Освобождаем камеру и закрываем окна
cap.release()
cv2.destroyAllWindows()

# ЗАДАНИЯ
#
# 1. Поменять min_detection_confidence. Что происходит?
#
# 2. Нарисовать рамку (код прилагается)
# 3. Нарисовать ключевые точки (код прилагается)
#
# 4. Нарисовать "нос"
#
# 5. Поменять FaceDetection на FaceMesh
