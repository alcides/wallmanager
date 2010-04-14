import threading

from appman.utils.unzip import unzip

class UncompressThread(threading.Thread):
    """ Thread that uncompresses a certain zip file."""
    def __init__(self, model, instance, path):
        self.model = model
        self.instance = instance
        self.path = str(path)
        threading.Thread.__init__(self)

    def run(self):
        try:
            un = unzip()
            un.extract( str(self.instance.zipfile.path) , self.path)
            extracted = True            
        except IOError:
            extracted = False
    
        if extracted:
            self.model.objects.filter(id=self.instance.id).update(extraction_path=self.path)