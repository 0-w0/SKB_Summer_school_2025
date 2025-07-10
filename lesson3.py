import cv2
import numpy as np
import matplotlib.pyplot as plt

# Загружаем яркую, цветную картинку. Например, с цветами или попугаями.
image_path = 'img/Lenna_(test_image).png' # Убедитесь, что такой файл есть
image_bgr = cv2.imread(image_path)
# Сразу конвертируем в RGB для удобного отображения в Matplotlib
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

print("Наше исходное изображение:")
plt.imshow(image_rgb)
plt.title('Исходное RGB изображение')
plt.show()


# --- ШАГ 1: ПРЕОБРАЗОВАНИЕ В GRAYSCALE (ОТТЕНКИ СЕРОГО) ---
# Для многих задач компьютерному зрению не нужен цвет, важна только яркость.
# Превратим нашу BGR картинку в Grayscale. Это делается одной командой!
gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

# Посмотрим на результат.
# ВАЖНО: Matplotlib может отображать Grayscale картинки в "тепловой карте".
# Чтобы она была черно-белой, нужно указать cmap='gray'.
print("\nПревратили картинку в черно-белую (Grayscale):")
plt.imshow(gray_image, cmap='gray')
plt.title('Grayscale изображение')
plt.show()

# Давайте посмотрим на "форму" (shape) матриц
print("Форма исходной RGB картинки:", image_rgb.shape)
print("Форма Grayscale картинки:", gray_image.shape)
print("Видите? У черно-белой картинки нет третьего измерения для каналов!")


# --- ШАГ 2: РАБОТА С ЦВЕТОВЫМ ПРОСТРАНСТВОМ HSV ---
# HSV (Hue, Saturation, Value) - Оттенок, Насыщенность, Яркость.
# Это позволяет нам изменять цвет более "по-человечески".

# 1. Конвертируем нашу BGR картинку в HSV
hsv_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

# ВАЖНО: OpenCV хранит HSV в таких диапазонах:
# H: 0-179 (не 0-360!)
# S: 0-255
# V: 0-255

# Создадим копию, чтобы не менять оригинал
hsv_modified = hsv_image.copy()

# 2. Увеличим НАСЫЩЕННОСТЬ (Saturation) всех пикселей на 50.
# Канал S находится по индексу 1.
# Мы не можем просто прибавить 50, так как значения не должны превысить 255.
# Используем специальную функцию cv2.add()
s_channel = hsv_modified[:, :, 1] # Выделяем канал насыщенности
new_s = cv2.add(s_channel, 50) # Прибавляем 50 ко всем значениям
hsv_modified[:, :, 1] = new_s  # Возвращаем измененный канал на место

# 3. Конвертируем измененную HSV картинку ОБРАТНО в BGR, а потом в RGB для вывода.
bgr_more_saturated = cv2.cvtColor(hsv_modified, cv2.COLOR_HSV2BGR)
rgb_more_saturated = cv2.cvtColor(bgr_more_saturated, cv2.COLOR_BGR2RGB)

print("\nУвеличили насыщенность цветов:")
plt.imshow(rgb_more_saturated)
plt.title('Изображение с повышенной насыщенностью')
plt.show()


# --- ШАГ 3: ПРИМЕНЕНИЕ ФИЛЬТРОВ (ЯДЕР) ---
# Фильтры изменяют пиксель, смотря на его соседей.

# 1. Размытие (Blur)
# Мы просто усредняем пиксели в окне (ядре) размером, например, 7x7.
# Чем больше размер ядра, тем сильнее размытие.
kernel_size = (7, 7)
blurred_image = cv2.blur(image_rgb, kernel_size)

print("\nПрименили фильтр размытия:")
plt.imshow(blurred_image)
plt.title('Размытое изображение (ядро 7x7)')
plt.show()


# 2. Повышение резкости (Sharpening)
# Для этого мы создадим свое собственное ядро (матрицу свертки).
# Эта матрица говорит "сделать центральный пиксель в 5 раз ярче,
# а из его яркости вычесть яркость четырех соседей".
sharpen_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])

# Применяем фильтр с нашим ядром к картинке
sharpened_image = cv2.filter2D(image_rgb, -1, sharpen_kernel)

print("\nПрименили фильтр повышения резкости:")
plt.imshow(sharpened_image)
plt.title('Изображение с повышенной резкостью')
plt.show()

# ЗАДАНИЯ
# 1. Сделать картинку темнее (измените value)
# 2. Сделать картинку светлее
#
# 3. Изменить оттенок (Hue). Понаблюдать, как меняются цвета
#
# 4. Усилить размытие
# 5. Использовать GaussianBlur
# 6. Создать свой фильтр, например
# edge_kernel = np.array([
#     [0,  1, 0],
#     [1, -4, 1],
#     [0,  1, 0]
# ])
#
# 7. Выделить один цвет
