# -*- coding: windows-1252 -*-

import glob, re, os, csv

## Get a list of all text files containing data from the directory where I store it.
## Create a list of all file names, with a full path (to be used later for file opening), and 
full_file_list = []
bare_file_list = []
for file_name in glob.glob("C:/Users/Agata/Dropbox/5vuosi/METH4DH/*.txt"):
    ## It is important to change the path above if the program is run elsewhere. The .txt files and the program may be in the same directory.
    full_file_list.append(file_name)
    name = os.path.splitext(os.path.basename(file_name))[0]
    bare_file_list.append(name)

list_dict = dict(zip(full_file_list, bare_file_list))
    
## Operations are executed for one file at a time, because I am interested in the content of each separate file.
## Open each file, read its content, close the file.

results_per_file = [] ## Empty list where results will be stored.
for file in full_file_list:
    f = open(file)
    content = f.read() 
    f.close()
    
    ## Short name for file. Split the file names at underscore, because all file names in the dataset are in the format
    ## SCHOOL_COURSE_DATE_PACKAGE_TASK_PARTICIPANTid_PARTICIPANTgender.txt.
    ## For each file that is in the long file list, strip the file paths so that there is only the file name without the extension.

    for k in list_dict.keys():
            if file == k:
                myfile = list_dict[k] 
                file =(myfile.split("_")) 

    ## Printing is useful for testing if the right forms have been found and if there are any wrong ones.
    ## It may be left out, but I left it here for clarity.
                
    ## Find all forms of pronoun "te": substring "te" is always at the beginning of the string,
    ## all other forms except nominative have "i" as the next character,
    ## not followed by any of the following: "k", "r", "h", "e", "l" - to exclude e.g. "terve", "tehdä", "tekee", "tee", "televisio". Could be expanded.    
    p = re.findall(r"\btei?[^krhel]", content)
    if p:
        print("Found the following plural personal pronouns \"te\": {} in file {}, occurring {} times".format(p, file, len(p)))

    ## Find all forms of pronoun "sinä", also including "sä", "sinua", "sinut".
    s = re.findall(r"\b(si?n?ä|sinua|sinut)\b", content)
    if s:
        print("Found the following singular personal pronouns \"sinä\": {} in file {}, occurring {} times".format(s, file, len(s)))

    ## Find all verb forms with substring "tte", which marks 2nd Pl, except when it is followed by "e" (to exclude "anteeksi").
    ## Imperative including -kaa tai -kää ending.
    t = re.findall(r"\w+t{2}e[^e]k?o?|\w+[aoieyöh]k[aä]{2}\!", content)
    if t:
        print("Found the following plural 2nd person verb forms: {} in file {}, occurring {} times".format(t, file, len(t)))

    ## Find all names of occupations in nominative case. The pattern excludes forms such as "tarjoilijalle".
    o = re.findall(r"tarjoilija\b", content)
    if o:
        print("Found the following address forms (occupation names): {} in file {}, occurring {} times".format(o, file, len(o)))

    ## Find all explicit politeness words such as "anteeks(i)" and "kiitos".
    a = re.findall(r"anteeksi?|kiitos", content)
    if a:
        print("Found the following politeness forms: {} in file {}, occurring {} times".format(a, file, len(a)))

    ## Find all verb forms that belong to 2nd person Sg, also including 2 Sg imperative, excluding -kaa/-kää forms characteristic for 2nd Pl and -nut/nyt verb forms.
    ## Imperative is arbitrarily marked with "!" in the dataset.
    ## The verb form is not ideal as the form will also catch plural noun forms such as "koirat" unless marked otherwise,
    ## so another arbitrary way of marking is that words ending with t, unless a verb form, have "x" attached at the end.
    y = re.findall(r"\w+(?<!kaa)\!|\w+(?<!nu|ny)tk?o?\b", content)
    if y:
        print("Found the following singular second verb forms incl. imperative: {} in file {}, occurring {} times".format(y, file, len(y)))

    ## Add (append) the results found to the list of results. If no form is found, add "0".
    results_per_file.append((file,
                            "TE+Pron", len(p) if p else "0", 
                            "SINÄ+Pron", len(s) if s else "0",
                            "TE+V+2Pl", len(t) if t else "0",
                            "SINÄ+V+2Sg", len(y) if y else "0",
                            "occupation_name", len(o) if o else "0",
                            "politeness_form", len(a) if a else "0"))


## Export content of each file to one .txt file: all text for topic modelling/collocation analysis.
## As of now, the programme opens all files twice, so it should be optimized. 
with open('C:/Users/Agata/Dropbox/5vuosi/combined.txt', 'w') as outfile:
    ## It is important to change the path above if the program is run elsewhere. It should NOT be in the same directory as the other .txt files,
    ## because each time the program is run, it would add this file to the analysis and duplicate the data.
    for fname in full_file_list:
        with open(fname) as infile:
            outfile.write(infile.readline()+"\n")
                        
## Export results to .csv.
with open('output_per_file.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(results_per_file)


