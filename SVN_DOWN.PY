import urllib2,os,re,sys

argvs=sys.argv
url=argvs[1]
path=argvs[2]

listurl=[]
def getpath(url):
    try:
        c=urllib2.urlopen(url+'/.svn/entries').read()
    except:
        return None,None
    get=c.split('\n')
    #print get
    dir=[get[i-1] for i in range(len(get)) if get[i]=='dir' and get[i-1]!='']
    file=[get[i-1] for i in range(len(get)) if get[i]=='file' and get[i-1]!='']
    return dir,file
    
def getfile(url):
    dir,file=getpath(url)
    if not dir and not file:return
    for i in file:
        listurl.append(url+'/.svn/text-base/%s.svn-base'%i)
    for k in dir:
        v=url+'/%s'%k
        getfile(v)
    return
    
def download(url):
    v=url.split('/')
    s=v.index('.svn')
    ps='/'.join(v[0:s]).replace('http://%s'%domain[0],'')
    name=v[-1].replace('.svn-base','')
    fp=path+ps+'/%s'%name
    print fp
    try:
        data = urllib2.urlopen(url).read()
    except:
        return 
    try:
        f = file(fp,'wb')
    except:
        try:
            os.makedirs(path+ps)
        except:
            pass
        f = file(fp,'wb')
    f.write(data)
    f.close()

#url=raw_input('URl:')
#path=raw_input('PATH:')
domain=re.findall('http://([^/]*)',url)
if not domain:raise
path=path+'/%s'%domain[0]
try:
    os.mkdir(path)
except:
    print 'exit'
getfile(url)
map(download,listurl)
