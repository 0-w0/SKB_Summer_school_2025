import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import time
import cv2
import mediapipe as mp


class VideoApp(tk.Tk):

    def __init__(self, window_title="Видео Приложение"):

        self.cords_to_draw = set()

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.recognizer = self.mp_hands.Hands(
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

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

        self.clean_button = tk.Button(
            self,
            text="Очистить",
            font=button_font,
            command=self.clean_board
        )

        self.clean_button.place(relx=0.98, y=90, anchor='ne')

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

    def clean_board(self):
        self.cords_to_draw = set()

    def on_closing(self):
        print("Закрытие приложения...")
        if self.vid.isOpened():
            self.vid.release()  # Освобождаем камеру
        self.destroy()  # Закрываем окно Tkinter

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_shape = frame.shape

        results = self.recognizer.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())

                landmarks_list = list(hand_landmarks.landmark)

                x_8 = int(landmarks_list[8].x * frame_shape[1])
                x_4 = int(landmarks_list[4].x * frame_shape[1])
                y_8 = int(landmarks_list[8].y * frame_shape[0])
                y_4 = int(landmarks_list[4].y * frame_shape[0])
                av_x = (x_4 + x_8) // 2
                av_y = (y_4 + y_8) // 2
                if abs(x_4-x_8)+abs(y_4-y_8) <= 35:
                    if self.is_drawing_mode == True:
                        self.cords_to_draw.add((av_x, av_y))
                    else:
                        cords_to_remove = set()
                        for x_r, y_r in self.cords_to_draw:
                            if abs(av_x - x_r) + abs(av_y - y_r) <= 15:
                                cords_to_remove.add((x_r, y_r))
                        for cord in cords_to_remove:
                            self.cords_to_draw.remove(cord)


        for cord in self.cords_to_draw:
            cv2.circle(frame, cord, radius=0, color=(255, 0, 255), thickness=15)

        return frame


if __name__ == "__main__":
    app = VideoApp(window_title="Tkinter Video App")
    app.mainloop()
