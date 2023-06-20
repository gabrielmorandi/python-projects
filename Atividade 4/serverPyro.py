import Pyro5.api as pyro
import base64

all_files = []

@pyro.expose
class FileServer(object):
  def __init__(self):
    self.files = []
    self.interests = {}

  def upload_file(self, file_name, file_data_base64):
    print('File upload requested')
    file_data = base64.b64decode(file_data_base64)
    file_obj = {"name": file_name, "data": file_data}
    self.files.append(file_obj)
    all_files.append(file_obj)
    # print(f'File "{file_name}" uploaded successfully')
    pass
  
  def get_file_info(self):
    print('File info requested')
    # print(all_files)
    files_info = all_files
    return files_info
  
  def download_file(self, file_name):
    print('Conectado')
    # logic
    pass
  
  def register_interest(self, file_name, client_reference, validity):
    print('Conectado')
    # logic
    pass
  
  def cancel_interest(self, file_name, client_reference):
    print('Conectado')
    # logic
    pass
  
def start_server():
  daemon = pyro.Daemon()
  uri = daemon.register(FileServer)
  print(f'Server ready on: {uri}')
  daemon.requestLoop()
  
if __name__ == "__main__":
  start_server()