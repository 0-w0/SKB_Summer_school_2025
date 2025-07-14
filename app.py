import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import time
import cv2
import mediapipe as mp
from mediapipe import solutions
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2


class VideoApp(tk.Tk):

    def __init__(self, window_title="Видео Приложение"):

        self.cords_to_draw = set()
        self.base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
        self.options = vision.GestureRecognizerOptions(base_options=self.base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(self.options)
        print(self.recognizer)

        super().__init__()
        self.title(window_title)
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            raise ValueError("Не удается получить доступ к камере")

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.geometry(f"{int(self.width)}x{int(self.height)}")

        self.is_drawing_mode = True
        self.current_frame = None

        self.video_label = tk.Label(self)
        self.video_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_font = font.Font(family="Helvetica", size=12)

        self.toggle_button = tk.Button(
            self,
            text="Ластик",
            font=button_font,
            command=self.toggle_draw_mode
        )

        self.toggle_button.place(relx=0.98, y=10, anchor='ne')

        self.save_button = tk.Button(
            self,
            text="Сохранить",
            font=button_font,
            command=self.save_image
        )

        self.save_button.place(relx=0.98, y=50, anchor='ne')

        self.update_frame()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def update_frame(self):
        ret, frame = self.vid.read()
        if ret:

            # OpenCV использует BGR, а Pillow/Tkinter - RGB
            frame = self.process_frame(frame)
            self.current_frame = frame.copy()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Конвертируем массив NumPy в изображение PIL
            pil_image = Image.fromarray(rgb_frame)

            # Конвертируем изображение PIL в формат для Tkinter
            tk_image = ImageTk.PhotoImage(image=pil_image)

            # Обновляем изображение в Label
            self.video_label.imgtk = tk_image  # Важно: сохраняем ссылку, чтобы изображение не было удалено сборщиком мусора
            self.video_label.config(image=tk_image)

        # Повторяем эту функцию через 15 миллисекунд
        self.after(15, self.update_frame)

    def toggle_draw_mode(self):
        """
        Переключает режим между рисованием и ластиком.
        """
        self.is_drawing_mode = not self.is_drawing_mode
        if self.is_drawing_mode:
            self.toggle_button.config(text="Ластик")
            print("Режим: Рисование")
            # Здесь можно добавить логику для активации рисования
        else:
            self.toggle_button.config(text="Рисовать")
            print("Режим: Ластик")
            # Здесь можно добавить логику для активации ластика

    def save_image(self):
        if self.current_frame is not None:
            filename = f"capture_{int(time.time())}.png"
            cv2.imwrite(filename, self.current_frame)
            print(f"Изображение сохранено как {filename}")
        else:
            print("Не удалось сохранить изображение, кадр отсутствует.")

    def on_closing(self):
        print("Закрытие приложения...")
        if self.vid.isOpened():
            self.vid.release()  # Освобождаем камеру
        self.destroy()  # Закрываем окно Tkinter

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        frame_shape = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        recognition_result = self.recognizer.recognize(image)
        if len(recognition_result.gestures):
            top_gesture = recognition_result.gestures[0][0]
            hand_landmarks = recognition_result.hand_landmarks

            if top_gesture.category_name == 'Pointing_Up' and self.is_drawing_mode == True:
                x = int(hand_landmarks[0][8].x * frame_shape[1])
                y = int(hand_landmarks[0][8].y * frame_shape[0])
                self.cords_to_draw.add((x, y))
            elif top_gesture.category_name == 'Pointing_Up' and self.is_drawing_mode == False:
                cords_to_remove = set()
                x = int(hand_landmarks[0][8].x * frame_shape[1])
                y = int(hand_landmarks[0][8].y * frame_shape[0])
                for x_r, y_r in self.cords_to_draw:
                    if abs(x - x_r) + abs(y - y_r) <= 15:
                        cords_to_remove.add((x_r, y_r))
                for cord in cords_to_remove:
                    self.cords_to_draw.remove(cord)

            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y,
                                                z=landmark.z) for landmark in
                hand_landmarks[0]
            ])
            solutions.drawing_utils.draw_landmarks(
                frame,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_styles.get_default_hand_landmarks_style(),
                solutions.drawing_styles.get_default_hand_connections_style())

        for cord in self.cords_to_draw:
            cv2.circle(frame, cord, radius=0, color=(255, 0, 255), thickness=15)

        return frame


if __name__ == "__main__":
    app = VideoApp(window_title="Tkinter Video App")
    app.mainloop()
