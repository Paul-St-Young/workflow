def init_girder(api_key=None, api_url='https://girder.hub.yt/api/v1'):
  """Initialize girder client, rely on environment variable:
    GIRDER_API_KEY, connect to yt Hub.

  Args:
    api_key (str, optional): use GIRDER_API_KEY env. var. by default
    api_url (str, optional): use yt Hub v1 by default
  Return:
    GirderClient: initialized girder client
  """
  from girder_client import GirderClient
  if api_key is None:
    import os
    api_key = os.environ['GIRDER_API_KEY']
  gc = GirderClient(apiUrl=api_url)
  gc.authenticate(apiKey=api_key)
  return gc

def find_folder(gc, path, root_id):
  """Find folder starting from root folder with UUID root_id.

  Args:
    gc (GirderClient): initialized client
    path (str): relative path of target folder from root
    root_id (str): UUID of root folder
  Return:
    Folder: girder folder
  """
  tokens = path.split('/')
  # look for target folder
  target = None
  tokens1 = []
  folder_id = root_id
  for ilevel, tok in enumerate(tokens):
    folders = gc.listFolder(folder_id)
    for folder in folders:
      name = folder['name']
      folder_id = folder['_id']
      if name == tok:
        target = folder
        tokens1.append(name)
        break
  # check found target
  if len(tokens1) != len(tokens):
    path1 = '/'.join(tokens1)
    msg = 'found "%s" from "%s"' % (path1, path)
    raise RuntimeError(msg)
  return target

def upload_with_meta(gc, fname, meta, folder_id, **kwargs):
  """Upload file with meta data to target folder

  Args:
    gc (GirderClient): initialized client
    fname (str): file to upload
    meta (dict): meta data to add to file
    folder_id (str): UUID of target folder
  """
  def attach_meta(item, name):
    gc.addMetadataToItem(item['_id'], meta)
  gc.addItemUploadCallback(attach_meta)
  gc.upload(fname, folder_id, **kwargs)
