import os, shutil

# def mycopyfile(srcfile,dstfile):
#     if not os.path.isfile(srcfile):
#         print("%s not exist!" % srcfile)
#     else:
#         fpath,fname=os.path.split(dstfile)    #分离文件名和路径
#         if not os.path.exists(fpath):
#             os.makedirs(fpath)                #创建路径
#         shutil.copyfile(srcfile,dstfile)      #复制文件
#         print "copy %s -> %s"%( srcfile,dstfile)


def copy_demo(srcfile, dstfile):
    fpath, fname = os.path.split(dstfile)
    print("fpath:", fpath)
    print("fname:", fname)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    shutil.copyfile(srcfile, dstfile)
    print("success")


if __name__ == '__main__':
    srcfile = "/Users/liushuochen/Desktop"
    dstfile = "/Users/liushuochen/Desktop/桌面/20190825.jpeg"
    copy_demo(srcfile, dstfile)