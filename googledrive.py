import sys
import requests
from tqdm import tqdm

def download_file_from_google_drive(id, destination):
  def get_confirm_token(response):
    for key, value in response.cookies.items():
      if key.startswith('download_warning'):
        return value
    return None

  def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
      for chunk in tqdm(response.iter_content(CHUNK_SIZE)):
       if chunk: # filter out keep-alive new chunks
         f.write(chunk)

  URL = "https://docs.google.com/uc?export=download"

  session = requests.Session()

  response = session.get(URL, params = { 'id' : id }, stream = True)
  token = get_confirm_token(response)

  if token:
    params = { 'id' : id, 'confirm' : token }
    response = session.get(URL, params = params, stream = True)

  save_response_content(response, destination)

if __name__ == '__main__':

  def usage():
    print('usage: {} id [outfile]'.format(sys.argv[0]), file=sys.stderr)
    return 1

  if (len(sys.argv)) <= 1:
    sys.exit(usage())

  id = sys.argv[1]
  if (len(sys.argv)) > 2:
    dest = sys.argv[2]
  else:
    dest = id
  download_file_from_google_drive(id, dest)
