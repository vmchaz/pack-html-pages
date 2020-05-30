import os
import os.path
import sys
import time
import datetime
import zipfile
import hashlib

def main():
    assert sys.version_info >= (3, 6)
    if len(sys.argv) < 2:
        print("USAGE: packpages directory")
        return
    
    pagesdir = sys.argv[1]
    pairs = []
    pairs2 = []
    for diritem in os.listdir(pagesdir):        
        diritem_name, diritem_ext = os.path.splitext(diritem)
        diritem_full_name = os.path.join(pagesdir, diritem)
        if os.path.isfile(diritem_full_name):
            if diritem_ext.upper() == ".HTML":
                #print("HTML file", diritem_name, diritem_ext)
                possible_dir_name = diritem_name+"_files"
                possible_dir_full_name = os.path.join(pagesdir, possible_dir_name)
                if os.path.isdir(possible_dir_full_name):
                    pair_html = diritem_name
                    pair_dir = possible_dir_name                    
                    
                    print("Pair found:")
                    print(diritem)
                    print(possible_dir_name)
                    pairs.append( (diritem, possible_dir_name) )
                    pairs2.append(diritem)
                    
    for p in pairs:
        html_fn, dn = p
        print(html_fn, dn)
        #savedir = os.getcwd()
        #os.chdir(dn)
        mtime_int = int(os.path.getmtime(html_fn))
        mtime_dt = dt = datetime.datetime.fromtimestamp(mtime_int)
        t = str(mtime_int) #str(int(time.time()))
        
        h = hashlib.md5()
        h.update(html_fn.encode("utf8"))
        md5str = h.hexdigest()
        
        rdf_text = '<?xml version="1.0"?>\n'+\
            '<RDF:RDF xmlns:MAF="http://maf.mozdev.org/metadata/rdf#"\n'+\
            'xmlns:NC="http://home.netscape.com/NC-rdf#"\n'+\
            'xmlns:RDF="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'+\
            '<RDF:Description RDF:about="urn:root">\n'+\
            '<MAF:originalurl RDF:resource="https:/unknown"/>\n'+\
            '<MAF:title RDF:resource="unknown title"/>\n'+\
            '<MAF:archivetime RDF:resource="Fri, 21 Apr 2017 03:40:48 +0300"/>\n'+\
            '<MAF:indexfilename RDF:resource="'+ html_fn +'"/>\n'+\
            '<MAF:charset RDF:resource="UTF-8"/>\n'+\
            '</RDF:Description>\n'+\
            '</RDF:RDF>'
        
        
        rdf_data = rdf_text.encode("utf8")
        
        zipname = os.path.splitext(html_fn)[0] + ".maff"
        #zipname = md5str + ".maff"
        zf = zipfile.ZipFile(zipname, "w")
        
        dt = datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0)
        modTime = time.mktime(dt.timetuple())
        
        zipinfo_time = (mtime_dt.year, mtime_dt.month, mtime_dt.day, mtime_dt.hour, mtime_dt.minute, mtime_dt.second)
        
        for e in os.walk(dn):
            wcd, dirs, files = e        
            for content_fn in files:
                local_fn = os.path.join(wcd, content_fn)
                f = open(local_fn, "rb")
                fdata = f.read()
                f.close()
                                
                fn_in_zip = os.path.join(t, local_fn)
                zi = zipfile.ZipInfo(fn_in_zip, zipinfo_time)
                zf.writestr(zi, fdata)
                
                #print(e)
        
        f = open(html_fn, "rb")
        fdata = f.read()
        f.close()
        
        fn_in_zip = os.path.join(t, html_fn)
        zi = zipfile.ZipInfo(fn_in_zip, zipinfo_time)
        zf.writestr(zi, fdata)        
                
                
        zi = zipfile.ZipInfo(os.path.join(t, "index.rdf"), zipinfo_time)
        zf.writestr(zi, rdf_data)
        
        zf.close()
        
        os.utime(zipname, (modTime, modTime))
        #os.chdir(savedir)

            
if __name__ == "__main__":
    main()
