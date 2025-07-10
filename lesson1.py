import cv2

image_path = 'img/Lenna_(test_image).png'

image = cv2.imread(image_path)
cv2.imshow('test image', image)

height, width, channels = image.shape
print(f"Размеры изображения: Ширина = {width} пикселей, Высота = {height} пикселей")

px_y, px_x = 50, 100
pixel_color = image[px_y, px_x]

# Выводим его цвет
print(f"Цвет пикселя в точке (x={px_x}, y={px_y}) это [R, G, B]: {pixel_color}")

image_modified = image.copy()
new_color = [0, 255, 0]
image_modified[px_y, px_x] = new_color
print(f"Мы изменили цвет пикселя в точке (x={px_x}, y={px_y}) на {new_color}")

image_modified[10:60, 10:60] = [255, 0, 0]
print("Мы нарисовали красный квадрат в левом верхнем углу.")

print("А вот что у нас получилось:")

cv2.imshow('image modified', image_modified)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ЗАДАНИЯ
# 1. Загрузить другую картинку
# 2. Узнать цвет другого пикселя
# 3. Нарисовать точку другого цвета
#
# 4. Переместить квадрат
# 5. Нарисовать несколько квадратов
# 6. Нарисовать рамку
#
# 7. Обесцветить изображение ("удалить" один из каналов)
# 8. Найти самый яркий пиксель
#
# 9. Нарисовать свою картинку
