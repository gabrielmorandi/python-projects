import Pyro5.api as pyro
import base64
import os

@pyro.expose
class Client(object):
  def notify(self, message):
    print(f"Notification received: {message}")

  def express_interest(self, file_name, validity_period, file_server):
    file_server.register_interest(file_name, self.uri, validity_period)
  
  def cancel_interest(self, file_name, file_server):
    file_server.cancel_interest(file_name, self.uri)
    
  def download_file(self, file_name, file_server):
    file_data_base64 = file_server.download_file(file_name)
    file_data = base64.b64decode(file_data_base64)
    with open(file_name, 'wb') as f:
      f.write(file_data)
    print(f'"{file_name}" downloaded successfully')

def start_client():
  daemon = pyro.Daemon()
  client = Client()
  client.uri = daemon.register(client)
  
  file_server = pyro.Proxy("PYRO:obj_cd1aee92095d4a2daffb5bb36cd47373@localhost:52865")
  file_server.register_client(client.uri)
  
  def upload_file_to_server(file_path):
    with open(file_path, 'rb') as f:
      file_data = f.read()
    file_data_base64 = base64.b64encode(file_data).decode('utf-8')
    file_name = os.path.basename(file_path)
    file_server.upload_file(file_name, file_data_base64)
    print(f'"{file_name}" uploaded successfully')

  upload_file_to_server("./interesse.txt")
  # upload_file_to_server("./teste.txt")
  # upload_file_to_server("./exemplo.txt")
  
  def get_file_info_from_server():
    files_info = file_server.get_file_info()
    for file in files_info:
      print(f"File: {file['name']} has size {len(base64.b64decode(file['data']['data']))} bytes")

  get_file_info_from_server()
  
  def register_interest(file_interest, validity_period):
    client.express_interest(file_interest, validity_period, file_server)
    print(f'Interest on archive: {file_interest} has been marked')

  register_interest('interesse.txt', 60*60*2)
  
  def unregister_interest(file_interest):
    client.cancel_interest(file_interest, file_server)
    print(f'Interest on archive: {file_interest} has been unmarked')

  unregister_interest('interesse.txt')
  
  def download_file_from_server(file_name):
    client.download_file(file_name, file_server)

  download_file_from_server('teste.txt')
  
  daemon.requestLoop()

if __name__ == "__main__":
  start_client()
