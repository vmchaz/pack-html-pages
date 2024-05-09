import os
import sys

def parsestring(s, delimiter):
    r = []
    q = False
    buf = ""
    df = False
    nl = False
    for c in s.strip(" "):
        if not nl:
            if q:
                if c == '"':
                    q = False
                elif c == "\n":
                    nl = True
                else:
                    if len(r) == 0:
                        r.append("")
                    if df:
                        df = False
                        r.append("")
                    r[len(r)-1] += c
            else:
                if c == delimiter:
                    df = True
                elif c == "\n":
                    nl = True
                elif c == '"':
                    q = True
                else:
                    if len(r) == 0:
                        r.append("")
                    if df:
                        df = False
                        r.append("")
                    r[len(r)-1] += c
    for i in range(len(r)):
        r[i] = r[i].strip(" ")

    return r
                
            

def main():
    src_dir = sys.argv[1]
    target_file = sys.argv[2]
    d = []
    for e in os.listdir(src_dir):
        f_n, f_ext = os.path.splitext(e)
        if f_ext == ".txt":
            with open(os.path.join(src_dir, e), "r") as f:
                fd = f.read()
                
            r = parsestring(fd, ",")
            if len(r) >= 2:
                html_n, html_ext = os.path.splitext(r[1])
                if not r[0].endswith(html_ext):
                    r[0] = r[0] + html_ext
                    
                    with open(os.path.join(src_dir, e), "w") as f:
                        r2 = []
                        l = '"' + r[0] + '", "' + r[1] + '"\n'
                        f.write(l)

                    
if __name__ == "__main__":
    main()
