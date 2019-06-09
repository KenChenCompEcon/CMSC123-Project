import os
import urllib.request
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
import multiprocessing

def readfile(filename):
  dest_dir = "./10k/"
  #read the index file
  file = open(filename, 'r')
  lines = file.readlines()
  for line in lines:
    cols = line.split()
    if len(cols) > 4 and cols[-3].isdigit():
      #check document type, only 10-k will be downloaded
      docu_type = cols[-4]
      if docu_type in ['10-K', '10-K405', '10-KSB', '10KSB', '10KSB40'] and cols[-5]!='NT':
        cik = cols[-3]
        #download from sec
        addr = "https://www.sec.gov/Archives/" + cols[-1]
        prefix = addr[addr.rfind('/') + 1 :]
        try:
          urllib.request.urlretrieve(addr, dest_dir + prefix)
        except URLError:
          print(filename + " " + cols[-1] + " fail to download")
          continue
        else:
            #save downloaded full 10k to a temp file
            tmpfile = open(dest_dir + prefix, "r+",encoding='utf-8', errors='ignore')
            text = tmpfile.read()
            #clean full 10k: html to raw text, delete non-ascii characters
            if '<html>' in text or '<HTML>' in text:
                try:
                    soup = BeautifulSoup(text, "html.parser")
                    raw = BeautifulSoup.get_text(soup)
                except:
                    print(filename + " " + cols[-1] + " fail to parse")
                    continue
                else:
                    raw = re.sub(r'[^\x00-\x7F]+',' ', raw)
                    tmplines = raw.split('\n')
            else:
                tmplines = text.split('\n')
            #find the ITEM 1 section, write back to temp file
            tmpfile.seek(0)
            write = False
            tmplines = [s.strip() for s in tmplines]
            tmplines = list(filter(lambda a: a != '', tmplines))
            for i,tmpline in enumerate(tmplines):
                #find the date of report
                if not write and tmpline[:27]=='CONFORMED PERIOD OF REPORT:':
                    report_date = tmpline[-8:]
                #find the beginning of the ITEM 1 section
                if not write and (tmpline[:7]=='ITEM 1 'or tmpline[:7]=='Item 1 ' or tmpline[:7]=='ITEM 1.'or tmpline[:7]=='Item 1.'or (tmpline[:4]=='ITEM' and tmplines[i+1][:1]=='1.')) and not tmpline[-1].isdigit() and 'ITEM' not in ''.join(tmplines[i+1:i+4]) and 'Item' not in ''.join(tmplines[i+1:i+4]):
                    write = True
                #find the end of the ITEM 1 section
                if write and (tmpline[:6]=='ITEM 2'or tmpline[:6]=='Item 2' or tmpline[:7]=='ITEM 1B'or tmpline[:7]=='Item 1B'):
                    break
                if write:
                    tmpfile.write(tmpline+'\n')
            tmpfile.truncate()
            tmpfile.close()
            #if the extracted text is larger than 1000 bytes, rename the temp file to the format "CIK_date.txt", else, delete it
            if os.path.getsize(dest_dir + prefix)>1000:
                os.rename(dest_dir + prefix, dest_dir + cik + '_' + report_date + '.txt')
            else:
                os.remove(dest_dir + prefix)
                print(filename + " " + cols[-1] + " fail to extract")
  file.close()
  print(filename + ' finished!')

if __name__ == "__main__":
  #collect the index files to a list
  file_lst = []
  for filename in os.listdir('./idx'):
    if filename.endswith(".idx"):
      file_lst.append('./idx/'+filename)
  pool = multiprocessing.Pool()
  #map over the list of index files
  pool.map(readfile, file_lst)
