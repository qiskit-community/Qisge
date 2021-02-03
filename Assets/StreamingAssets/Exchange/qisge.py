import json
from os.path import dirname, abspath, join


def _read(filename):
    filename=join( dirname(abspath(__file__)), filename)
    with open(filename,'r') as file:
        return file.read()
      
def _write(filename,message):
    filename=join( dirname(abspath(__file__)), filename)
    with open(filename,'w') as file:
        file.write(message)

def _scrub():     
    _write('sprite.txt','')
    _write('input.txt','')

def _get_input():
    raw_input = _read('input.txt')
    _write('input.txt','')
    if raw_input:
        input = eval(raw_input)
    else:
        input = {'key_presses': [], 'clicks': []}
    return input

def _update_screen():
    changes = _engine.get_changes()
    if changes:
        _write('sprite.txt',changes)
        _write('dump.txt',changes)

def _val_change(key,value,dictionary):
    if key in dictionary:
        val_change = dictionary[key]!=value
    else:
        val_change = True
    return val_change

def update():
    _update_screen()
    return _get_input()


class _Engine():
    
    def __init__(self):
        self.image_changes = []
        self.sprite_changes = []
        self.camera_changes = {}
        self.text_changes = []
        self.sound_changes = []
                
    def get_changes(self):
        # read in any changes that have not yet been acted upon
        changes = _read('sprite.txt')
        if changes:
            changes = eval(changes)
        # otherwise construct from changes recorded in this object
        else:
            changes = {}
            for attr in self.__dict__:
                changes[attr] = self.__dict__[attr]
        # empty the record of changes
        self.image_changes = []
        self.camera_changes = {}
        for attr in ['sprite_changes','camera_changes','text_changes','sound_changes']:
            self.__dict__[attr] = [{} for _ in range(len(self.__dict__[attr]))]
        # output the string of changes
        return json.dumps(changes)


class ImageList(list):
    
    def __init__(self,filenames):
        for filename in filenames:
            self.append(filename)
            
    def _record(self,image_id,filename):
        _engine.image_changes.append({'image_id':image_id,'filename':filename})
        
    def __setitem__(self,image_id,filename):
        super().__setitem__(image_id,filename)
        self._record(image_id,filename)
        
    def append(self,filename):
        image_id = len(self)
        super().append(filename)
        self._record(image_id,filename)


class Camera():

    def __init__(self,x=0,y=0,z=0,zoom=1,angle=0):
        self.x = x
        self.y = y
        self.z = z
        self.zoom = zoom
        self.angle = angle

    def __setattr__(self,name,val):
        # only do something if the value actually changes
        if _val_change(name,val,self.__dict__):
            # record all values whenever something changes (remove once issue is fixed on Unity side)
            for attr in self.__dict__:
                _engine.camera_changes[attr] = self.__dict__[attr]
            # record the updated value for the thing that's changed
            _engine.camera_changes[name] = val
        self.__dict__[name] = val

 
class Sprite():
    def __init__(self,image_id,x=0,y=0,z=0,size=1,angle=0):
        
        self.sprite_id = len(_engine.sprite_changes)
        _engine.sprite_changes.append({})
        
        self.image_id = image_id
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.angle = angle
        
    def __setattr__(self,name,val):
        # only do something if the value actually changes
        if _val_change(name,val,self.__dict__):
            if name!='sprite_id':
                # record all values whenever something changes (remove once issue is fixed on Unity side)
                for attr in self.__dict__:
                    _engine.sprite_changes[self.sprite_id][attr] = self.__dict__[attr]
                # record the updated value for the thing that's changed
                _engine.sprite_changes[self.sprite_id][name] = val
            self.__dict__[name] = val


class Text():
    def __init__(self,text,x=0,y=0,z=0,size=1,angle=0):

        self._text_id = len(_engine.text_changes)
        _engine.text_changes.append({})
        
        self.text = text
        self.x = x
        self.y = y
        self.z = z
        self.font_size = size
        self.line_width
        self.angle = angle

    def __setattr__(self,name,val):
        # only do something if the value actually changes
        if _val_change(name,val,self.__dict__):
            if name!='text_id':
                # record all values whenever something changes (remove once issue is fixed on Unity side)
                for attr in self.__dict__:
                    _engine.text_changes[self.text_id][attr] = self.__dict__[attr]
                # record the updated value for the thing that's changed
                _engine.text_changes[self.text_id][name] = val
            self.__dict__[name] = val


_scrub()
_engine = _Engine()
camera = Camera()

