import cv2
import matplotlib.pyplot as plt

image_path = 'img/Lenna_(test_image).png'
image_bgr = cv2.imread(image_path)

print("Попытка 1: Выводим BGR картинку в RGB-окне. Цвета неправильные!")
plt.imshow(image_bgr)
plt.title('BGR изображение (неправильные цвета)')
plt.show()

image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
print("\nПопытка 2: Конвертируем в RGB. Теперь все отлично!")
plt.imshow(image_rgb)
plt.title('RGB изображение (правильные цвета)')
plt.show()

y1, y2 = 50, 250
x1, x2 = 100, 300
cropped_image = image_rgb[y1:y2, x1:x2]

print(f"\nВырезали кусок картинки от y=({y1}:{y2}) и x=({x1}:{x2})")
plt.imshow(cropped_image)
plt.title('Обрезанное изображение')
plt.show()


height, width, _ = image_rgb.shape
new_width_small = width // 2
new_height_small = height // 2
resized_small = cv2.resize(image_rgb, (new_width_small, new_height_small))

new_width_large = int(width * 1.5)
new_height_large = int(height * 1.5)
resized_large = cv2.resize(image_rgb, (new_width_large, new_height_large), interpolation=cv2.INTER_CUBIC)

print("\nИзменили размер. Слева - уменьшенная, справа - увеличенная.")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(resized_small)
axes[0].set_title('Уменьшенная в 2 раза')
axes[1].imshow(resized_large)
axes[1].set_title('Увеличенная в 1.5 раза')
plt.show()


center = (width // 2, height // 2)
angle = 45
scale = 1.0
M = cv2.getRotationMatrix2D(center, angle, scale)
rotated_image = cv2.warpAffine(image_rgb, M, (width, height))
print(f"\nПовернули картинку на {angle} градусов")
plt.imshow(rotated_image)
plt.title(f'Поворот на {angle} градусов')
plt.show()

image_to_draw_on = image_bgr.copy()
blue_bgr = (255, 0, 0)
green_bgr = (0, 255, 0)
red_bgr = (0, 0, 255)
cv2.line(image_to_draw_on, (50, 50), (250, 50), red_bgr, 5)
cv2.rectangle(image_to_draw_on, (280, 100), (400, 250), green_bgr, 3)
cv2.circle(image_to_draw_on, (150, 180), 50, blue_bgr, -1)
final_drawing_rgb = cv2.cvtColor(image_to_draw_on, cv2.COLOR_BGR2RGB)
print("\nНарисовали фигуры на картинке. Не забыли про BGR!")
plt.imshow(final_drawing_rgb)
plt.title('Рисуем фигуры')
plt.show()

# ЗАДАНИЯ
# 1. Вырезать часть изображения (желательно осмысленную)
# 2. Вырезать квадрат
#
# 3. Сплющить или растянуть исходную картинку
# 4. Повернуть картинку из произвольной точки на произвольный градус
#
# 5. Перекрасить нарисованные фигуры
# 6. Нарисовать закрашенный прямоугольник
# 7. нарисовать очки
#
# 8. Сделать "рамку" вокруг обрезанного ранее квадрата
# 9. Поместить текст на изображение
