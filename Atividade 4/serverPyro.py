import Pyro5.api as pyro
import base64
import time

all_files = []
all_clients = []
all_interests = {}

@pyro.expose
class FileServer(object):
  def register_client(self, client_uri):
    all_clients.append(client_uri)
    print(f'Client: {client_uri} -> connected')

  def register_interest(self, file_name, client_uri, validity):
    if file_name not in all_interests:
      all_interests[file_name] = []
    all_interests[file_name].append({"client_uri": client_uri, "valid_until": time.time() + validity})
    print(f'Client Interested: {client_uri} interested in {file_name}')
    print(all_interests)

  def upload_file(self, file_name, file_data_base64):
    print('File upload requested')
    file_data = base64.b64decode(file_data_base64)
    file_obj = {"name": file_name, "data": file_data}
    all_files.append(file_obj)

    if file_name in all_interests:
      for interest in all_interests[file_name][:]:
        if time.time() <= interest["valid_until"]:
          client = pyro.Proxy(interest["client_uri"])
          client.notify(f"File '{file_name}' has been uploaded")
          print(f'Notification send to: {client}')
          all_interests[file_name].remove(interest)

  def get_file_info(self):
    print('File info requested')
    files_info = all_files
    return files_info
  
  def cancel_interest(self, file_name, client_uri):
    if file_name in all_interests:
      for interest in all_interests[file_name][:]:
        if client_uri == interest["client_uri"]:
          all_interests[file_name].remove(interest)
          print(f'Interest on file: {file_name} from {client_uri} has been cancelled.')
          return
    print("No interest found for this client and file.")
    
  def download_file(self, file_name):
    print('Download file   requested')
    for file_obj in all_files:
      if file_obj["name"] == file_name:
        return base64.b64encode(file_obj["data"]).decode('utf-8')
    return None
  
def start_server():
  daemon = pyro.Daemon()
  uri = daemon.register(FileServer)
  print(f'Server ready on: {uri}')
  daemon.requestLoop()
  
if __name__ == "__main__":
  start_server()
