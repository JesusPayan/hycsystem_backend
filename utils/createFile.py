import os,tempfile

def createFile(file_name):
        """Function to create file for saving"""
        fileName = file_name
        if os.path.exists(tempfile.gettempdir()+"\\"+fileName):
            os.remove(os.path.join(tempfile.gettempdir(),fileName))
        fpath = os.path.join(tempfile.gettempdir(), fileName)
        print(fpath)
        f = open(fpath, mode='w', encoding='ascii')

        print('infoExtractor: archivo creado')
        return f, fpath, fileName, fpath