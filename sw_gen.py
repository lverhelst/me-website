import sys, getopt, os, glob, json
from distutils.dir_util import copy_tree


#params
## input_folder = source
## output_folder = output
## template_file = base.html
## overwrite_option = purge | overwrite
def main(argv):
    #defaults
    inputfolder = 'source'
    outputfolder = 'output'
    overwrite_option = 'purge'

    #try:
    opts, args = getopt.getopt(argv, "i:o:t:v:", ["inputfolder=", "outputfolder=", "templatefile=", "overwriteoption="])
    #except getopt.GetoptError:
    #    print('sw_gen.py needs the right arguments fool')
    #    sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--inputfolder"):
            inputfolder = arg
        elif opt in ("-o", "--outputfolder"):
            outputfolder = arg
        elif opt in ("-t", "--templatefile"):
            templatefile = arg
        elif opt in ("-v", "--overwriteoption"):
            overwrite_option = arg 
        else:
            print ("unknown argument-  %s: %s", opt, args)

    if overwrite_option == 'purge':
        os.system('rm -rf output')
        os.system('mkdir output')

    # for files in input_folder
    input_files = []
    for file in glob.glob(inputfolder + '/' +  "*.html"):
        print("found file: ", file)
        input_files.append(file)

    ## hold templates in memory
    templatecontents = {}
    for path in input_files:
        head, tail = os.path.split(path)
        if(tail[0] == "_"):
            templatecontents[tail.replace('_','').replace('.html','')] = open(path, 'r').read()        
        else:
            continue

    ## apply functions
    for path in input_files:
        head, tail = os.path.split(path)
        if(tail[0] == "_"):
            print("Skipping template file ", tail)
            continue
        else:
            print("applying template to " + path)
            inf = open(path, 'r').read()
            t_type = getextendtype(inf)
            if t_type in ('base', 'parallax'):
                nf = applytemplate(t_type, templatecontents, inf)
                ### TODO configure_titles (replace all the {{Title}})
                nf = nf.replace('{% title %}', tail.split('.')[0])
                #save to output folder
                of = open(outputfolder + '/' + tail, 'w')
                of.write(nf)
                of.close()
            elif t_type in ('imagelist'):
                applytemplate(t_type, templatecontents, inf)
            else:
                print('We should throw an error here')
    
#### copy css and javascript files over
    copy_tree(inputfolder + "/css", outputfolder + "/css")
    copy_tree(inputfolder + "/javascript", outputfolder + "/javascript")
    copy_tree(inputfolder + "/stories", outputfolder + "/stories")


def applytemplate(templatetype, templatefilecontents, inheritingfilecontents):
    if templatetype == "base":
        print("apply base template")
        return applybasetemplate(templatefilecontents[templatetype], inheritingfilecontents)
    elif templatetype == "parallax":
        print("apply parallax template")
        contents = applyparallaxtemplate(templatefilecontents[templatetype], inheritingfilecontents)
        #check if this template inherits from another template
        t_type = getextendtype(contents)
        if t_type is None:
            print('We found a parallax template that doesn''t extend base')
        else: 
            contents = applytemplate(t_type, templatefilecontents, contents)        
        return contents  
    elif templatetype == "imagelist":
        print("apply image list template")
        return applyimagelisttemplate(templatefilecontents, templatefilecontents[templatetype], inheritingfilecontents)
    else:
        print("unknown template type")
        return inheritingfilecontents
    return "" 

def applybasetemplate(templatefilecontents, inheritingfilecontents):
    tf_copy = templatefilecontents
    tf_copy = tf_copy.replace('{%block_content%}',
    inheritingfilecontents.split("{% block content %}")[1].split("{% endblock %}")[0])
    if("{%script%}" in inheritingfilecontents):
        tf_copy = tf_copy.replace('{%script%}',
        inheritingfilecontents.split("{%script%}")[1].split("{%endscript%}")[0])
    else:
        tf_copy = tf_copy.replace('{%script%}', '')
    return tf_copy

def applyparallaxtemplate(templatefilecontents,inheritingfilecontents):
    #load options from template
    options = inheritingfilecontents.split('{% options:')[1].split('%}')[0].split(';')
    folder = ''
    json_file = ''
    for opt in options:
        arg, val = opt.split("=")
        if(arg == "folder"):
            folder = val
        elif(arg == "dict"):
            json_file = val
        else:
            print("Unknown arg, val ", arg, val)

    #open json file for each item
        # generate a template line in the .html
    template_html = templatefilecontents.split('{%WHILE_IMG%}')[1].split('{%ENDWHILE_IMG%}')[0]
    template_stash = template_html 
    result = templatefilecontents.split('{%WHILE_IMG%}')[0] + '{%REPLACEME%}' + templatefilecontents.split('{%ENDWHILE_IMG%}')[1]
    #TODO: this line hardcode's source because inputfolder isn't available at this scope
    # either make inputfolder global or pass it through.
    json_contents = open('source/stories/' + folder + '/' + json_file, 'r').read()    
    j = json.loads(json_contents)
    

    for i, k in enumerate(j["pages"]):
        for attr, vl in k.items():
            template_html = template_html.replace('{%' + attr + '%}',vl)
        if(i != len(j["pages"]) -1):
            template_html = template_html.replace('{%style%}', '')
        else:
            template_html = template_html.replace('{%style%}','style="height:50vh;font-size:22px;"')
        template_html += template_stash
    
    #super lazy way to get rid of the last template_stash that gets added
    #a do...while would have been better
    template_html = template_html.replace(template_stash, '')

    return result.replace('{%REPLACEME%}',  template_html) 


def applyimagelisttemplate(templates, templatefilecontents,inheritingfilecontents):
    #load options from template
    options = inheritingfilecontents.split('{% options:')[1].split('%}')[0].split(';')
    folder = ''
    json_file = ''
    for opt in options:
        arg, val = opt.split("=")
        if(arg == "folder"):
            folder = val
        elif(arg == "dict"):
            json_file = val
        else:
            print("Unknown arg, val ", arg, val)

    #open json file for each item
        # generate a template line in the .html
    template_html = templatefilecontents.split('{%rinse%}')[1].split('{%repeat%}')[0]
    template_stash = template_html 
    result = templatefilecontents.split('{%rinse%}')[0] + '{%REPLACEME%}' + templatefilecontents.split('{%repeat%}')[1]
    result_stash = result 
    #TODO: this line hardcode's source because inputfolder isn't available at this scope
    # either make inputfolder global or pass it through.
    json_contents = open('source/stories/' + folder + '/' + json_file, 'r').read()    
    j = json.loads(json_contents)
    
    #here's where the image list get's a little different
    #we generate a new .html page per image
    #which also means we need to apply the base template here. 
    #I definitely need to re-architect the template application to be cleaner
    name = ''
    for k in j["pages"]:
        result = result_stash
        template_html = template_stash
        name = k["img"]
        head, tail = os.path.split(name)
        name = tail.replace('.jpg','')

        for attr, vl in k.items():
            template_html = template_html.replace('{%' + attr + '%}',vl)
        result = result.replace('{%REPLACEME%}',  template_html)         
        result = applytemplate('base', templates, result)
        ### TODO configure_titles (replace all the {{Title}})
        nf = result.replace('{% title %}', name)
        #save to output folder
        of = open('output/' + name + '.html', 'w')
        of.write(nf)
        of.close()

    return



#I really should write a parser
def getextendtype(contents):
    e_type  = contents.split("{% extends")[1].split("%}")[0].replace(" ","").replace("\"","")
    print(e_type)
    return e_type

if __name__ == "__main__":
    main(sys.argv)
