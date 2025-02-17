from fileops import create_tarball
import os
import time 


from_dpath = "/media/ljp238/12TBWolf/RSPROX/TANDEMX_EDEM_GLOBAL/TANDEMX_EDEM_BATCHES"
to_dpath = "/media/ljp238/12TBWolf/RSPROX/TANDEMX_EDEM_GLOBAL/TANDEMX_EDEM_BATCHES_TAR/"
if __name__ == '__main__':
    ti = time.perf_counter()
    os.makedirs(to_dpath,exist_ok=True)
    tilenames = os.listdir(from_dpath)
    for i, tilename in enumerate(tilenames):
        #if i > 2: break
        fpath = os.path.join(from_dpath, tilename)
        tpath = os.path.join(to_dpath, tilename+'.tar.gz')
        print(tpath)

        ta =  time.perf_counter()
        if not os.path.isfile(tpath):
            create_tarball(fpath,tpath)
        else:
            print(f'already created {tpath}')
        tb =  time.perf_counter() - ta
        print(f'run.time {tb/60} min(s)')
        print(f'tilename::{tilename}')


    tf = time.perf_counter() - ti 
    print(f'run.time {tf/60} min(s)')
    print('Done')