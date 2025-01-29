
from fileops import fast_copy_all
from upaths import idpath,odpath

if __name__ == '__main__':
    fast_copy_all(idpath,odpath, max_workers=50)