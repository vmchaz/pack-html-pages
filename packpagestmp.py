import os
import hashlib
import sys
import time

cExtensions = [".htm", ".html", ".mht", ".mhtml", ".maff"]
cExtensionsConvert = {".htm":".html", ".html":".html", ".mht":".mht", ".mhtml":".mht", ".maff":".maff"}

def main():
    if len(sys.argv) < 3:
        return
        
    htmldir = sys.argv[1]
    targetdir = sys.argv[2]
    processeddir = ""
    #duplicatesdir = ""
    

    
    if not os.path.isdir(htmldir):
        print("Invalid directory:", htmldir)
        return
        
    if not os.path.isdir(targetdir):
        print("Invalid directory", targetdir)
        return
        
    if len(sys.argv) >= 4:
        processeddir = sys.argv[3]
        if not os.path.isdir(processeddir):
            print("Invalid directory", processeddir)
            return
        
    #if len(sys.argv >= 5):
    #    if not os.path.isdir(duplicatesdir):
    #        print("Invalid directory", duplicatesdir)
    #        return
       
    
    
    print("Source dir:", htmldir) 
    print("Target dir:", targetdir)
    print("Processed dir:", processeddir)
    #print("Duplicates dir:", duplicatesdir)
    
    listdir_iter = os.listdir(htmldir)
    for e in listdir_iter:
        
        fullfn = os.path.join(htmldir, e)
        if os.path.isfile(fullfn):
            htmlnwe, htmlext = os.path.splitext(e)
            htmlext_lower = htmlext.lower()
            #print(htmlnwe, htmlext)
            
            if htmlext_lower in cExtensions:
                
                print("html file:", fullfn)
                f = open(fullfn, "rb")
                fdata = f.read()
                f.close()
                
                h = hashlib.md5(fdata)
                md5 = h.hexdigest()
                print("md5:", md5)
                
                
                #if not os.path.isfile()
                md5fn = os.path.join(targetdir, md5)                
                
                md5htmlfn = os.path.join(targetdir, md5+cExtensionsConvert[htmlext_lower])
                md5txtfn = os.path.join(targetdir, md5+".txt")
                
                duplicate = False
                
                if not os.path.isfile(md5htmlfn):
                    f2 = open(md5htmlfn, "wb")
                    f2.write(fdata)
                    f2.close()
                    
                else:
                    print(md5htmlfn, "already exists!")
                    duplicate = True
                
                if not os.path.isfile(md5txtfn):
                    f2 = open(md5txtfn, "w")
                    s = md5 +" "+e
                    f2.write(s)
                    f2.close()
                
                print("Done processing", e)
                
                #for future use
                #parameters
                if processeddir and os.path.isdir(processeddir):
                    if not duplicate:
                        if not os.path.isfile(os.path.join(processeddir, e)):
                            os.rename(os.path.join(htmldir, e), os.path.join(processeddir, e))
                        else:
                            os.rename(os.path.join(htmldir, e), os.path.join(processeddir, e+str(int(time.time()))+".duplicate"))
                    else:        
                        os.rename(os.path.join(htmldir, e), os.path.join(htmldir, e+".duplicate"))
    
if __name__ == "__main__":
    main()
