import datetime, os, random

def upload_file_name(instance, filename): #instance is coming object
    _, ext = os.path.splitext(filename)
    folders = {"jpg":'img',"jpeg":"img","png":"img","svg":'img'}
    return "{}-{}/{:%Y-%m-%d-%H-%M-%S}-{}{}".format(
        folders.get(ext[1:],ext[0]), # instance.upload_for>>>we use classes atribute here! calling via object!
        datetime.datetime.now().strftime("%Y-%m"),datetime.datetime.now(),random.randint(1000,9999),ext
    )