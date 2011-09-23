# By Jimmy Ruska
# Sorts Desktop and Downloads folder by extension.
# Made for easy modification. Tested: Windows/Ubuntu Python 2.7, 3.2.
# Beware, it will also move folders and program shortcuts.

import os,re,platform
_organize={'txt':       'txt,rtf,doc,xls,org,htm,html,odp,odt,pps,ppt,nfo,tex'
          ,'txt/ebook': 'pdf,epub,chm,ps,djvu'
          ,'images':    'png,gif,jpg,bmp,jpeg,tiff,ico,psd,xcf,svg,tga,ai'
          ,'exe':       'exe,msi,lnk,swf,jar,jnlp,dll,com,bat,app,gadget'
          ,'iso':       'iso,nrg,bin,cue,mds,ccd,udf,daa,uif,vcd'
          ,'zip':       'zip,gz,tar,bz2,rar,ace,tgz,z,7z,deb,pls,m3u,sfv,pkg,dmg,rpm'
          ,'audio':     'wav,mp3,midi,mid,wma,aac,ac3,faac,ape,m4a'
          ,'video':     'mp4,mkv,ogg,mpg,mpeg,wmv,avi,m4v,flv,divx,ogv,mov,vob,rm,3gp'
           ,'src':       'php,c,py,js,css,fla,lsp,erl,sh,hs,scm,d,go,pl,avs,ahk,as,fla,cpp,bash,hrl,h,java,m,ml'
          ,'src/dat':   'log,sql,cnf,conf,patch,diff,ini,xml,cvs,cfg'
          ,'other':     '*'
          ,'other/bt':   "torrent"
          ,'dir':       '/'
          }
_ignore=[("re","^\."),("match","crdownload"),("exact","desktop.ini"),("exact","Downloads"),("re","\.part$")]

def main():
    # Set which folder things get sorted into
    if (platform.uname())[0]=="Windows":
        final=os.environ['USERPROFILE']+"\\My Documents\\Downloads\\"
    else: final="/home/"+os.environ.get("USERNAME")+"/Downloads/"
    if not os.path.isdir(final): os.mkdir(final)
    # Put which folders you want sorted
    sort([final,final+"..\\..\\Desktop\\","/home/"+os.environ.get("USERNAME")+"/Desktop/"], final)

# sort list of dirs into folder final
def sort(dirs,final): 
    # make base directories if they don't exist
    for key in _organize.keys():
        if os.path.isdir(final+key)==False: os.makedirs(final+key)
    #loop through and sort all directories
    for (path,file) in sum([[(d,z) for z in os.listdir(d)] for d in dirs if os.path.exists(d)],[]): 
        if file in _organize or exclude(file): pass
        elif os.path.isdir(path+file) and os.path.exists(final+"dir/"+file)==False:
            os.rename(path+file, final+"dir/"+file)
        else: 
            to=final+grouping(file.rpartition(".")[2].lower())+file
            if os.path.exists(to)==False: os.rename(path+file,to)

# Don't sort certain files like Desktop.ini
def exclude(name):
    for (op,check) in _ignore:
        if   op=="re" and re.match(check,name)!=None: return True
        elif op=="match" and re.search(check,name)!=None: return True
        elif op=="exact" and check==name: return True
    return False

# Match file extensions to find group
def grouping(ext):
    for folder,exts in _organize.items():
        if exts.replace(' ','').split(",").count(ext)>0: return folder+"/"
    return "other/"

if __name__ == '__main__':
    main()
