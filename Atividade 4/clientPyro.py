import Pyro5.api as pyro
import base64
import os

def start_client():
  file_server = pyro.Proxy("PYRO:obj_aa52ec1c639e432fbc93f04bf812a0c1@localhost:55234")
  
  def upload_file_to_server(file_path):
    with open(file_path, 'rb') as f:
      file_data = f.read()
    file_data_base64 = base64.b64encode(file_data).decode('utf-8')
    file_name = os.path.basename(file_path)
    file_server.upload_file(file_name, file_data_base64)

  upload_file_to_server("./teste.txt")
  upload_file_to_server("./exemplo.txt")
  
  def get_file_info_from_server():
    files_info = file_server.get_file_info()
    for file in files_info:
      print(f"File: {file['name']} has size {len(base64.b64decode(file['data']['data']))} bytes")

  get_file_info_from_server()

if __name__ == "__main__":
  start_client()
