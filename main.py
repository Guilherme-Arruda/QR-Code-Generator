import customtkinter
import qrcode
import base64
from io import BytesIO
from PIL import Image
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename

customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme('blue')

class ImageFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    self.img_label = customtkinter.CTkLabel(self, text = 'EMPTY')
    self.img_label.pack(padx = 20, pady = 15, expand = True)

class ColorFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    self.fill_color_value = 'black'
    self.back_color_value = 'white'

    self.fill_label = customtkinter.CTkLabel(self, text = 'Fill Color:')
    self.fill_label.pack(padx = 20, pady = 15, side = 'left')

    self.fill_pick_frame = customtkinter.CTkFrame(self, width = 50, height = 29, fg_color = 'black', cursor = 'hand2')
    self.fill_pick_frame.bind('<Button-1>', self.fill_color_pick)
    self.fill_pick_frame.pack(padx = (0, 20), pady = 15, side = 'left', fill = 'x', expand = True)

    self.back_label = customtkinter.CTkLabel(self, text = 'Back Color:')
    self.back_label.pack(padx = (0, 20), pady = 15, side = 'left')

    self.back_pick_frame = customtkinter.CTkFrame(self, width = 50, height = 29, fg_color = 'white', cursor  = 'hand2')
    self.back_pick_frame.bind('<Button-1>', self.back_color_pick)
    self.back_pick_frame.pack(padx = (0, 20), pady = 15, side = 'left', fill = 'x', expand = True)

  def fill_color_pick(self, event):
    color = askcolor(title = 'Fill Color')

    if color[1] != None:
      self.fill_pick_frame.configure(fg_color = color[1])
      self.fill_color_value = color[1]

  def back_color_pick(self, event):
    color = askcolor(title = 'Back Color')

    if color[1] != None:
      self.back_pick_frame.configure(fg_color = color[1])
      self.back_color_value = color[1]

  def get(self):
    return self.fill_color_value, self.back_color_value

class App(customtkinter.CTk):
  def __init__(self):
    super().__init__()

    self.title('QR Code Generator')
    self.geometry('720x620')

    self.grid_columnconfigure((1), weight = 1)
    self.grid_rowconfigure((3), weight = 1)

    self.qr_code = ''

    self.title_label = customtkinter.CTkLabel(self, text = 'QR Code Generator', font = ('Helvetica', 20))
    self.title_label.grid(row = 0, column = 0, columnspan = 3, pady = 15)

    self.text_label = customtkinter.CTkLabel(self, text = 'Content:')
    self.text_label.grid(row = 1, column = 0, padx = 15)

    self.text_entry = customtkinter.CTkEntry(self, placeholder_text = 'Enter or Paste the Content here')
    self.text_entry.grid(row = 1, column = 1, columnspan = 2, padx = (0, 15), sticky = 'ew')

    self.color_frame = ColorFrame(self)
    self.color_frame.grid(row = 2, column = 0, columnspan = 3, padx = 15, pady = (20, 0), sticky = 'ew')

    self.img_frame = ImageFrame(self)
    self.img_frame.grid(row = 3, column = 0, columnspan = 3, padx = 15, pady = (20, 0), sticky = 'nsew')

    self.generate_button = customtkinter.CTkButton(self, text = 'Generate QR Code', command = self.generate_qr)
    self.generate_button.grid(row = 4, column = 0, columnspan = 2, padx = 15, pady = 20, sticky = 'ew')

    self.save_button = customtkinter.CTkButton(self, text = 'Save QR Code', width = 170, command = self.save_as)
    self.save_button.grid(row = 4, column = 2, padx = (0, 15), pady = 20, sticky = 'ew')

  def generate_qr(self):
    text = self.text_entry.get().strip()

    if len(text) == 0:
      messagebox.showwarning('Warning', 'Please enter a text')

    else:
      qr = qrcode.QRCode(version = 1, error_correction = qrcode.constants.ERROR_CORRECT_L, box_size = 20, border = 2)
      qr.add_data(text)
      qr.make()

      fill_color, back_calor = self.color_frame.get()
      img = qr.make_image(fill_color = fill_color, back_color = back_calor)

      self.qr_code = img

      buffered = BytesIO()
      img.save(buffered, format = 'JPEG')
      img_str = base64.b64encode(buffered.getvalue())

      new_img = Image.open(BytesIO(base64.b64decode(img_str)))

      ctk_image = customtkinter.CTkImage(new_img, size = (300, 300))

      self.img_frame.img_label.configure(text = '')
      self.img_frame.img_label.configure(image = ctk_image)

  def save_as(self):
    text = self.img_frame.img_label.cget('text')

    if text == 'EMPTY':
      messagebox.showwarning('Warning', 'No QR Code to save')

    else:
      file_path = asksaveasfilename(defaultextension = ".png", filetypes = [("PNG files", "*.png")])

      if file_path:
        self.qr_code.save(file_path, format = 'PNG')
        messagebox.showinfo('Info', 'QR Code saved successfully')

if __name__ == "__main__":
  app = App()
  app.resizable(False, False)
  app.mainloop()
