import requests
import urllib.parse
#using scraping API as page API fails for more than 10000 records.
def getCollection(resfile):
    try:
        fo=open(resfile,"w+")
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
        fo.write( "identifier"+"\t"+"title"+"\t"+"creator"+"\n")
        error_log = open('arxerrlog.txt', 'w+')
        url = "https://archive.org/services/search/v1/scrape?"
        basic_params = {'q': '(collection%3Adigitallibraryindia+AND+(language%3Atel++OR+language%3ATelugu))',
                        'fields': 'identifier,title,creator,Publication Date', 'output': 'csv'}
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
                    if length>2 :
                        dlicreator=i['creator']
                    fo.write( dliid+"\t"+dlititle+"\t"+dlicreator+"\n" )
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
getFields ("arxdlifields.tsv", 0)