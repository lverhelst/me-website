from os import walk 
import os
import math
import json

def rename_files(path, prefix):
    filenames = next(walk(path), (None, None, []))[2]  # [] if no file

    i = 1
    num_chars = int(math.log10(len(filenames)))+1
    suffix = '0' * num_chars

    for f in filenames:
        if(f[-4:] == '.jpg'):
            fname = prefix + (suffix + str(i))[-num_chars:] + f[-4:]
            print(f + " -> " + fname)
            i = i + 1
            os.rename(path + '/' + f, path+ '/' +fname)

def gen_imagelist_json(path):
    filenames = next(walk(path), (None, None, []))[2]  # [] if no file

    i = 1
    num_chars = int(math.log10(len(filenames)))+1
    json_list = []

    #FILTER
    filenames = [f for f in filenames if f[-4:] == ".jpg"]
    filenames.sort()
    
    f_first = filenames[0][:-4] + '.html'
    f_last = filenames[len(filenames) - 1][:-4] + '.html'

    i = 0
    
    for f in filenames:
        idict = {}
        if(f[-4:] == '.jpg'):
            idict["img"] = "/stories/flowers2021/" + f
            idict["img_prev"]= (f[:-4] + '.html' if i == 0 else filenames[i-1][:-4] + '.html')
            idict["img_next"]= (f[:-4] + '.html' if i == len(filenames) - 1 else filenames[i + 1][:-4] + '.html')
            idict["img_first"]= f_first
            idict["img_last"]= f_last
            idict["caption"]= ""
            idict["paragraph title"]= ""
            idict["paragraph text" ]= ""
            idict["title"]= "Flowers 2021"
            idict["alt_text"]= ":( sorry the image didn't load."
            i += 1
        json_list.append(idict)
    dic = {}
    dic["pages"] = json_list

    print(json.dumps(dic))


gen_imagelist_json('/home/lverhelst/Projects/me-website/source/stories/flowers2021')
#rename_files('/home/lverhelst/Projects/me-website/source/stories/flowers2021', 'flower2021')


