import Pyro5.api as pyro
import base64
import os

from tkinter import *
import customtkinter

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


@pyro.expose
class Client(object):
  def __init__(self):
    self.file_server = pyro.Proxy(
        "PYRO:obj_0e4b0ce6e3864e7b8429b679fa2012e0@localhost:49973")
    self.interest_files = []

  def notify(self, message):
    showinfo(
      title='Notificação',
      message=message
    )

  def express_interest(self, file_name, validity_period):
    self.file_server.register_interest(
        file_name, self.uri, validity_period)
    self.interest_files.append(file_name)
    showinfo(
        title='Marcar Interesse',
        message=f'Interesse marcado para o arquivo: {file_name}'
    )

  def cancel_interest(self, file_name):
    self.file_server.cancel_interest(file_name, self.uri)
    self.interest_files.remove(file_name)
    showinfo(
        title='Desmarcar Interesse',
        message=f'Interesse removido para o arquivo: {file_name}'
    )

  def download_file(self, file_name):
    file_data_base64 = self.file_server.download_file(file_name)
    file_data = base64.b64decode(file_data_base64)
    with open(file_name, 'wb') as f:
      f.write(file_data)
    showinfo(
        title='Download com sucesso!',
        message=f'Download feito com sucesso para o arquivo: {file_name}'
    )

  def upload_file_to_server(self, file_path):
    with open(file_path, 'rb') as f:
      file_data = f.read()
    file_data_base64 = base64.b64encode(file_data).decode('utf-8')
    file_name = os.path.basename(file_path)
    self.file_server.upload_file(file_name, file_data_base64)
    print(f'"{file_name}" uploaded successfully')

  def get_file_info(self):
    files_info = self.file_server.get_file_info()
    return files_info


def start_client():
  daemon = pyro.Daemon()
  client = Client()
  client.uri = daemon.register(client)
  client.file_server.register_client(client.uri)

  def select_file():
    filetypes = (
      ('text files', '*.txt'),
      ('All files', '*.*')
    )

    filenames = fd.askopenfilenames(
      title='Abrir arquivo',
      initialdir='/Downloads',
      filetypes=filetypes)

    for filename in filenames:
      client.upload_file_to_server(filename)

    showinfo(
      title='Arquivos Enviados',
      message=f'O(s) Arquivo(s):\n{filenames}\n foram enviados com sucesso!'
    )

  def show_file_list():
    files_info = client.get_file_info()

    file_list_window = tk.Toplevel(window)
    file_list_window.title('Lista de Arquivos')
    file_list_window.geometry('300x400')  # Aumenta a altura da janela

    # Cria um widget de lista para exibir os nomes dos arquivos
    listbox = tk.Listbox(file_list_window)
    listbox.pack(fill=tk.BOTH, expand=True)

    # Adiciona cada nome de arquivo na lista (ordem reversa)
    for file_info in reversed(files_info):
      frame = ttk.Frame(file_list_window)
      frame.pack(side='top', pady=5)  # Empilha verticalmente os itens

      label = ttk.Label(frame, text=file_info['name'])
      label.pack(side='left', padx=10)

      button = ttk.Button(
          frame, text='Download', command=lambda file=file_info: client.download_file(file["name"]))
      button.pack(side='left', padx=10)

    file_list_window.mainloop()

  def show_interest_files():
    interest_files_window = tk.Toplevel(window)
    interest_files_window.title('Arquivos com Interesse')
    interest_files_window.geometry('300x200')

    # Cria um widget de lista para exibir os arquivos com interesse
    listbox = tk.Listbox(interest_files_window)
    listbox.pack(fill=tk.BOTH, expand=True)

    # Adiciona cada arquivo com interesse na lista
    for file_name in client.interest_files:
      frame = ttk.Frame(interest_files_window)
      frame.pack(side='top', pady=5)  # Empilha verticalmente os itens

      label = ttk.Label(frame, text=file_name)
      label.pack(side='left', padx=10)

      button = ttk.Button(frame, text='Desmarcar Interesse',
                          command=lambda file=file_name: client.cancel_interest(file))
      button.pack(side='left', padx=10)

    interest_files_window.mainloop()

  
  window = ThemedTk(theme='yaru')
  window.title('Servidor RMI')
  window.geometry('500x350')

  title_label = ttk.Label(
    master=window, text='Bem-vindo Server Side :)', font='Ubuntu 20 bold')
  title_label.pack()

  input_frame = ttk.Frame(master=window)
  search_frame = ttk.Frame(master=window)
  interest_frame = ttk.Frame(master=window)
  interest_files_frame = ttk.Frame(master=window)

  title_label_file = ttk.Label(
    master=input_frame, text='Fazer Upload', font='Ubuntu 10 bold')
  title_label_file.pack(side='left', padx=10)
  button_upload_file = ttk.Button(
    master=input_frame, text='Selecionar arquivo(s)', command=select_file)
  button_upload_file.pack(side='left', expand=True)

  title_label_search_file = ttk.Label(
    master=search_frame, text='Consultar Arquivos', font='Ubuntu 10 bold')
  title_label_search_file.pack(side='left', padx=10)
  button_search_file = ttk.Button(
    master=search_frame, text='Ver arquivo(s)', command=show_file_list)
  button_search_file.pack(side='left', expand=True)

  title_label_interest_file = ttk.Label(
    master=interest_frame, text='Marcar Interesse', font='Ubuntu 10 bold')
  title_label_interest_file.pack(side='left', padx=10)
  input_interest_file = ttk.Entry(master=interest_frame)
  input_interest_file.pack(side='left')
  button_confirm_interest_file = ttk.Button(
    master=interest_frame, text='Confirmar Interesse',
    command=lambda: client.express_interest(input_interest_file.get(), 60*60*2))
  button_confirm_interest_file.pack(side='left')

  title_label_interest_files = ttk.Label(
    master=interest_files_frame, text='Arquivos com Interesse:')
  title_label_interest_files.pack()

  button_show_interest_files = ttk.Button(
    master=interest_files_frame, text='Exibir Arquivos com Interesse',
    command=show_interest_files)
  button_show_interest_files.pack()

  input_frame.pack(pady=10)
  search_frame.pack(pady=10)
  interest_frame.pack(pady=10)
  interest_files_frame.pack(pady=20)

  window.mainloop()

  daemon.requestLoop()


if __name__ == "__main__":
  start_client()
