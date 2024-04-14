import gzip
import os.path
import tarfile
import shutil

def ungzip_file(gz_filename, tagpath):
    ungz_filename = gz_filename.replace('.tgz', '').replace('.tar.gz', '').replace('.gem', '')

    tmp = ungz_filename.split('/')
    name = tmp[-1]
    ungz_filename = tagpath + '/' + name

    shutil.copy(gz_filename, tagpath)

    if os.path.exists(ungz_filename):
        shutil.rmtree(ungz_filename)
    try:
        f_gz = tarfile.open(gz_filename)  
        f_gz.extractall(ungz_filename)

    except Exception as e:
        print('error')
    finally:

        f_gz.close()
        
    print("success")
    return ungz_filename



def un_gz(file_name):
    f_name = file_name.replace(".gz", "")
    
    g_file = gzip.GzipFile(file_name)
    
    f = open(f_name, "wb+")
    f.write(g_file.read())
    
    g_file.close()  
    f.close()
    return f_name
