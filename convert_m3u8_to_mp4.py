import os
import sys
import shutil

target = "output"

def prepare():
    try:
        os.mkdir(target)
    except:
        pass

def get_all_ts(path):
    all = []
    tss = []

    for fl in os.listdir(path):
        if os.path.isdir(fl):
            all.extend(get_all_ts(os.path.join(path, fl)))
        elif fl.isdigit():
            tss.append(int(fl))

    tss.sort()
    all.append([os.path.join(path, str(x)) for x in tss])
    return all

def combine_ts(source):
    def combine(tss, target):
        with open(target, 'wb') as f:
            for ts_file in tss:
                with open(ts_file, "rb") as ts:
                    f.write(ts.read())

    count = 0
    for mov in source:
        if len(mov) == 0:
            continue
        combine(mov, os.path.join(target, str(count)+".mp4"))
        count += 1
        
        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Oach!!!! Wrong")
        exit(1)

    path = sys.argv[1]

    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    prepare()
    all_tss = get_all_ts(path)
    combine_ts(all_tss)
