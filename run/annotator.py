import base64
import io
import json
import os
from tkinter import (Button, Canvas, Checkbutton, Frame, IntVar, Scrollbar, Tk,
                     filedialog, messagebox)

from PIL import Image, ImageTk


class ImageAnnotator:
    def __init__(self, root, image_folder):
        self.root = root
        self.image_folder = image_folder
        self.image_files = [f for f in os.listdir(image_folder) if f.endswith('.json')]
        self.current_index = 0
        self.artifacts = {
            "crack": "закольная трещина", 
            "overexposure": "Засветы", 
            "shadow": "Тени", 
            "light_beam": "Пучки света",
            "metal_structure": "Металлические конструкции, арматура", 
            "pipe": "Трубы",
            "wire": "Провода", 
            "equipment": "Техника", 
            "camera_shadow": "Тени от камеры (планшет / телефон)", 
            "through_tunnel": "Сквозные туннели"
        }
        self.check_vars = {artifact: IntVar() for artifact in self.artifacts.keys()}

        if not self.image_files:
            messagebox.showerror("Ошибка", "В выбранной папке нет файлов JSON.")
            self.root.destroy()
            return

        self.setup_ui()

    def setup_ui(self):
      # Menu frame at the top
      self.menu_frame = Frame(self.root)
      self.menu_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

      Button(self.menu_frame, text="Назад", command=self.prev_image, width=10, height=2).pack(side="left", padx=5, pady=5)
      Button(self.menu_frame, text="Вперед", command=self.next_image, width=10, height=2).pack(side="left", padx=5, pady=5)
      Button(self.menu_frame, text="Сохранить", command=self.save_annotations, width=10, height=2).pack(side="left", padx=5, pady=5)

      # Checkboxes frame on the left
      self.checkboxes_frame = Frame(self.root)
      self.checkboxes_frame.grid(row=1, column=0, sticky="ns")

      for artifact, label in self.artifacts.items():
          Checkbutton(self.checkboxes_frame, text=label, variable=self.check_vars[artifact]).pack(anchor="w", padx=5, pady=2)

      # Canvas frame for the image on the right
      self.canvas_frame = Frame(self.root, relief="sunken")
      self.canvas_frame.grid(row=1, column=1, sticky="nsew")
      self.root.grid_rowconfigure(1, weight=1)
      self.root.grid_columnconfigure(1, weight=1)
      self.canvas_frame.pack_propagate(False)  # Prevent the frame from resizing to the canvas size

      self.canvas = Canvas(self.canvas_frame, bg="white")
      self.canvas.pack(side="left", fill="both", expand=True)

      self.v_scroll = Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
      self.v_scroll.pack(side="right", fill="y")
      self.h_scroll = Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
      self.h_scroll.pack(side="bottom", fill="x")

      self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
      
      self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
      self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)
      # self.canvas.bind("<Control-MouseWheel>", self.zoom)
      # Create Zoom In and Zoom Out buttons
      # zoom_in_button = Button(self.menu_frame, text="Zoom In", command=self.zoom_in)
      # zoom_out_button = Button(self.menu_frame, text="Zoom Out", command=self.zoom_out)
      # zoom_in_button.pack(side='left')
      # zoom_out_button.pack(side='left')

      # Bind mouse wheel events for zooming
      # self.canvas.bind("<Button-4>", self.zoom_in)
      # self.canvas.bind("<Button-5>", self.zoom_out)
      self.current_scale = 1.0

      self.load_image()

    def zoom_in(self, event=None):
        # Increase the image size by a factor (e.g., 1.2)
        self.image = self.image.resize((int(self.image.width * 1.2), int(self.image.height * 1.2)), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)

    def zoom_out(self, event=None):
        # Decrease the image size by a factor (e.g., 0.8)
        self.image = self.image.resize((int(self.image.width * 0.8), int(self.image.height * 0.8)), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)
    
    
    def zoom(self, event):
      """Zoom in and out with Control + MouseWheel"""
      x = self.canvas.canvasx(event.x)
      y = self.canvas.canvasy(event.y)
      factor = 1.1 if event.delta > 0 else 0.9
      
      self.current_scale *= factor
      self.canvas.scale('all', x, y, factor, factor)
      self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_shift_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    
    def load_image(self):
        if self.current_index < 0 or self.current_index >= len(self.image_files):
            messagebox.showinfo("Конец", "Вы достигли конца списка изображений.")
            return

        json_file = os.path.join(self.image_folder, self.image_files[self.current_index])
        with open(json_file, 'r') as file:
            data = json.load(file)

        if 'imageData' in data:
            image_data = base64.b64decode(data['imageData'])
            image = Image.open(io.BytesIO(image_data))
            self.tkimage = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.tkimage, anchor="nw")
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Сброс чекбоксов
        for var in self.check_vars.values():
            var.set(0)

        # Установка чекбоксов из файла
        if 'flags' in data:
            for flag, value in data['flags'].items():
                if flag in self.check_vars:
                    self.check_vars[flag].set(value)

    def save_annotations(self):
        flags = {artifact: bool(self.check_vars[artifact].get()) for artifact, label in self.artifacts.items()}
        json_file = os.path.join(self.image_folder, self.image_files[self.current_index])
        with open(json_file, 'r') as file:
            data = json.load(file)

        data['flags'] = flags

        with open(json_file, 'w') as file:
            json.dump(data, file, indent=2)

        messagebox.showinfo("Сохранено", "Аннотации сохранены.")

    def next_image(self):
        self.current_index += 1
        self.load_image()

    def prev_image(self):
        self.current_index -= 1
        self.load_image()

def main():
    root = Tk()
    root.title("Аннотация изображений")
    root.state('zoomed')  # Открыть окно на весь экран
    folder_selected = filedialog.askdirectory()

    if not folder_selected:
        messagebox.showerror("Ошибка", "Папка не выбрана.")
        root.destroy()
        return

    app = ImageAnnotator(root, folder_selected)
    root.mainloop()

if __name__ == "__main__":
    main()
