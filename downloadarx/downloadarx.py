import requests
import urllib.parse
#using scraping API as page API fails for more than 10000 records.
from internetarchive import get_item
import re
def getCollection(resfile):
    try:
        fo=open(resfile,"w")
        error_log = open('arxerrlog.txt', 'w+')
        url = "https://archive.org/services/search/v1/scrape?"
        basic_params={ 'q':'(collection%3Adigitallibraryindia+AND+(language%3Atel++OR+language%3ATelugu))', 'fields':'description'}
        params=basic_params.copy()
        while True:
            try:

                params_str= "&".join("%s=%s" % (k, v) for k, v in params.items())
                print (params_str)
                resp = requests.get(url+params_str, headers={})
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                error_log.write('Could not get search result' + url + params+' because of error: %s\n' % e)
                print ("There was an error; writing to log.")
                sys.exit(1)
            else:
                data= resp.json()
                #write results
                dlidict=data["items"]
                dlivalues = [i['description'] for i in dlidict]
                fo.writelines(["%s\n" % item for item in dlivalues])
                cursor = data.get('cursor', None)
                print(cursor)
                if cursor is None:
                    break
                else:
                    params = basic_params.copy()
                    params['cursor'] = cursor
        fo.close()
    except IOError:
        print ("Error: can\'t find file or read data")

def getFields(resfile,numitems):
    try:
        fo=open(resfile,"w")
# write headerfr
        fo.write( "identifier"+"\t"+"title"+"\t"+"creator"+"\t"+"date"+"\n")
        error_log = open('arxerrlog.txt', 'w+')
        url = "https://archive.org/services/search/v1/scrape?"
        basic_params = {'q': '(collection%3Adigitallibraryindia+AND+(language%3Atel++OR+language%3ATelugu))',
                        'fields': 'identifier,title,creator,date', 'output': 'json'}
        params = basic_params.copy()
        count=0
        while True:
            try:

                params_str= "&".join("%s=%s" % (k, v) for k, v in params.items())
                print (params_str)
                resp = requests.get(url+params_str, headers={})
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                error_log.write('Could not get search result' + url + params+' because of error: %s\n' % e)
                print ("There was an error; writing to log.")
                sys.exit(1)
            else:
                data= resp.json()
                #write results
                dlidict=data["items"]
                count+=data["count"]
                for i in dlidict:
                    length=len(i)
                    dliid = i['identifier']
                    dlititle=i['title']
                    dlicreator=""

                    if 'creator' in i:
                        dlicreator=i['creator']
                    dlidate=""
                    if 'date' in i:
                        dlidate=i['date'][0:10]
                    fo.write( dliid+"\t"+dlititle+"\t"+dlicreator+"\t"+dlidate+"\n" )
                cursor = data.get('cursor', None)
                print(cursor)
                if (numitems !=0) and (count > numitems):
                       break
                if cursor is None:
                    break
                else:
                    params = basic_params.copy()
                    params['cursor'] = cursor
        fo.close()
    except IOError:
        print ("Error: can\'t find file or read data")
# getCollection("arxdlicat.txt")
#getFields ("arxdlifields.txt", 200") numitems is zero for the whole data
#getFields ("arxdlifields.tsv", 0)
#
def getOrigMetaFields(inpfile,resfile,numitems):
    try:

        fo=open(resfile,"w")
# write headerfr
        fo.write( "id"+"\t"+"pubd"+"\t"+"totalpages"+"\n")
        error_log = open('arxerrlog.txt', 'w+')
        numline=0
        with open(inpfile) as fi:
            for line in fi:
                m=re.search(r"Book Source: Digital Library of India Item ([0-9]+\.[0-9]+)",line)
                if m:
                    id=m.group(1)
                else:
                    break

                datecite=""
                searchstr="dc.date.citation"+": "+"([0-9]+[/|-]?[0-9]+[/|-]?[0-9]+)"
                m = re.search(searchstr,line)
                if m:
                    datecite=m.group(1)

                totpages=""
                searchstr="dc.description.totalpages"+": "+"([0-9]+)"
                m = re.search(searchstr, line)
                if m:
                    totpages = m.group(1)
                fo.write(id+"\t"+datecite+"\t"+totpages+"\n")
                numline+=1
                if (numitems != 0) and (numline > numitems):
                    break
        fo.close()
    except IOError:
        print ("Error: can\'t find file or read data")

#gets archive item fields and DLI description subfields
def getCollection2(resfile,numitems):
    try:
        fo=open(resfile,"w")
        error_log = open('arxerrlog.txt', 'w+')
        url = "https://archive.org/services/search/v1/scrape?"
        basic_params={ 'q':'(collection%3Adigitallibraryindia+AND+(language%3Atel++OR+language%3ATelugu))',
                       'fields':'identifier,title,creator,date,description'}
        params=basic_params.copy()
        numline = 0
        fo.write( "id"+"\t"+"title"+"\t"+"creator"+"\t"+"pubd"+"\t"+"pages"+"\t"+"bc"+"\t"+"subject"+"\n")
        while True:
            try:

                params_str= "&".join("%s=%s" % (k, v) for k, v in params.items())
                print (params_str)
                resp = requests.get(url+params_str, headers={})
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                error_log.write('Could not get search result' + url + params+' because of error: %s\n' % e)
                print ("There was an error; writing to log.")
                sys.exit(1)
            else:
                data= resp.json()
                #write results
                iadict=data["items"]
                for i in iadict:
                    iaid=i['identifier']

                    iatitle=""
                    if 'title' in i:
                        iatitle=i['title']
                    iacreator=""
                    if 'creator' in i:
                        iacreator= i['creator']
                    iadate=""
                    if 'date' in i:
                        iadate= i['date']
                    iadesc=""
                    iadesc_totpages=""
                    iadesc_barcode=""
                    iadesc_sub=""
                    if 'description' in i:
                        iadesc=i['description']
                        
                        totpagessearchstr = "dc.description.totalpages" + ": " + "([0-9]+)"
                        m = re.search(totpagessearchstr,iadesc)
                        if m:
                            iadesc_totpages = m.group(1)
                        
                        # barcode search
                        bcsearchstr = "dc.identifier.barcode" + ": " + "([0-9]+)"
                        m = re.search(bcsearchstr,iadesc)
                        if m:
                            iadesc_barcode = m.group(1)

                        subsearchstr="(?<=dc.subject.classification: )(.+?)(?= dc\.|$)"
                        match=re.findall(subsearchstr, iadesc)
                        iadesc_sub='|'.join(match)

                    fo.writelines("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (iaid,iatitle,iacreator,iadate,
                                                                    iadesc_totpages,iadesc_barcode,iadesc_sub))
                    numline += 1
                    if (numitems != 0) and (numline > numitems):
                        break
                if (numitems != 0) and (numline > numitems):
                    break
                cursor = data.get('cursor', None)
                print(cursor)
                if cursor is None:
                    break
                else:
                    params = basic_params.copy()
                    params['cursor'] = cursor
        fo.close()
    except IOError:
        print ("Error: can\'t find file or read data")

getCollection2("arxtelnodup.tsv",0)


#getCollection3("arxtelsize.tsv",10)

# for duplicates csv file, get size, output duplicates,sizes,comparison status
def sizeCompareForDuplicates(inpfile,outpfile, numlines):
    import subprocess
    import json
    try:
        fo=open(outpfile,"w")
        error_log = open('arxerrlog.txt', 'w+')
        line=1
        result = []
        resultset=set()
        fi=open(inpfile,"r")
        for row in fi.readlines():
            row=row.strip("\n")
            idlist=row.split(sep=",")
            index=0
            result.clear()
            resultset.clear()
            for id in idlist:
                cmd1="ia"
                cmd2="metadata"
                cmd3=id
                #cmd4='|jq \".files[0].size\"'
                response=json.loads((subprocess.run([cmd1,cmd2,cmd3], stdout=subprocess.PIPE).stdout.decode('utf-8')))
                response2=response['files']
                size='0'
                for obj in response2:
                    if obj['name'].find(".pdf")!= -1:
                        size=obj['size']
                        break
                if(int(size)==0):
                    print("Error, Did not find pdf file for determining size")
                    exit(-1)
                result.append(size)
                index+=1
            #compare resulting sizes
            resultset=set(result)
            if len(resultset)==1:
                 compare="Success"
            else:
                compare="Fail"
            #write resultline
            index=0;
            for id in idlist:
                fo.write(id+"("+result[index]+")")
                index+=1
            fo.write("("+compare+")"+"\n")
            print(line,compare)
            line += 1
            if (numlines != 0) and (line > numlines):
                break

    except IOError:
        print("Error: can\'t find file or read data")
#sizeCompareForDuplicates("flagdupset.csv","flagdupsetresult.csv",0)

# for duplicates csv file, get size, output duplicates,sizes,comparison status using api call for speedup
def sizeCompareForDuplicates2(inpfile,outpfile, numlines):
    import subprocess
    import json
    url = "https://archive.org/metadata/"
    try:
        fo=open(outpfile,"w")
        error_log = open('arxerrlog.txt', 'w+')
        line=1
        result = []
        resultset=set()
        fi=open(inpfile,"r")
        for row in fi.readlines():
            row=row.strip("\n")
            idlist=row.split(sep=",")
            index=0
            result.clear()
            resultset.clear()
            for id in idlist:
                params_str = "%s/files" % id
                print(params_str)
                try:
                    resp = requests.get(url + params_str, headers={})
                except requests.exceptions.RequestException as e:  # This is the correct syntax
                    error_log.write('Could not get search result' + url + params + ' because of error: %s\n' % e)
                    print("There was an error; writing to log.")
                    sys.exit(1)
                else:
                    data = resp.json()['result']

                size='0'
                for obj in data:
                    if obj['name'].find(".pdf")!= -1:
                        size=obj['size']
                        break
                if(int(size)==0):
                    print("Error, Did not find pdf file for determining size")
                    exit(-1)
                result.append(size)
                index+=1
            #compare resulting sizes
            resultset=set(result)
            if len(resultset)==1:
                 compare="Success"
            else:
                compare="Fail"
            #write resultline
            index=0;
            for id in idlist:
                fo.write(id+","+result[index]+",")
                index+=1
            fo.write(compare+"\n")
            line += 1
            print(line,compare)
            if (numlines != 0) and (line > numlines):
                break

    except IOError:
        print("Error: can\'t find file or read data")
#sizeCompareForDuplicates2("flagdupset.csv","flagdupsetresult2.csv",0)

# Read from the duplicates size comparison output, when there is success, write the ids, when there is a fail,
# find subsets which have samesize, write their ids, and also write uniques if exist() using csv module
def splitdup_size(inpfile, outfile,numlines):
    import pandas as pd
    import numpy as np
    import csv

    line = 0
    fi = open(inpfile, 'r')
    csvfile = open(outfile, 'w', newline="")
    writer = csv.writer(csvfile, delimiter=",")
    for row in fi.readlines():
        line += 1
        if row.find("Fail") != -1:
            row = row.replace(",Fail\n", "")
            info = row.split(",")
            ids = []
            sizes = []
            for i, j in zip(info[0::2], info[1::2]):
                ids.append(i)
                sizes.append(j)
            isf = pd.DataFrame({'id': pd.Series(ids), 'size': sizes})
            isfg = isf.groupby(['size'], sort=False)

            for name, group in isfg:
                duplist = group['id'].tolist()
                writer.writerow(duplist)
        else:
            row = row.replace(",Success\n", "")
            info = row.split(",")
            ids = []
            sizes = []
            for i, j in zip(info[0::2], info[1::2]):
                ids.append(i)
                sizes.append(j)
            isf = pd.DataFrame({'id': pd.Series(ids), 'size': sizes})
            isfg = isf.groupby(['size'], sort=False)
            for name, group in isfg:
                duplist = group['id'].tolist()
                writer.writerow(duplist)
        print(line)
        if (numlines != 0) and (line > numlines):
            break

    csvfile.close()

#splitdup_size('flagdupsetresult2trans.csv','flagduprevised.csv',0)

#getCollection("arxdlicat.txt")
#getFields ("arxdlifields.txt", 200") numitems is zero for the whole data
#getFields ("""arxdlifields.tsv", 0)
#getOrigMetaFields("arxdlicat.txt", "idfields.tsv",0)

