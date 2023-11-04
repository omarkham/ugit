import os 
import hashlib

GIT_DIR = '.ugit' #Define the directory where the ugit repository will be stored

def init(): #Initialize a new ugit repository by creating necessary directories
    os.makedirs (GIT_DIR)
    os.makedirs(f'{GIT_DIR}/objects')

def hash_object(data, type_='blob'): #Compute the object ID (OID) for a data blob and store it in the repository
    obj = type_.encode() + b'\x00' + data #Prepare the object to be stored, combining type, null byte, and data
    oid = hashlib.sha1(data).hexdigest() #Compute the SHA-1 hash of the object to obtain the OID
    
    with open(f'{GIT_DIR}/objects/{oid}', 'wb') as out: #Write the object to the objects directory within the repository
        out.write(obj)
        
    return oid #Return the compute OID

def get_object(oid, expected='blob'): #Retrieve and return the content of an object by its OID
    with open(f'{GIT_DIR}/objects/{oid}', 'rb') as f:
        obj = f.read()
        
    type_,_, content = obj.partition(b'\x00') #Split the object into its type, null byte, and content
    type_ = type_.decode()
    
    if expected is not None: #Verify the expected type matches the actual type of the object
        assert type_ == expected, f'Expected {expected}, got {type_}'
        
    return content #Return the content of the object