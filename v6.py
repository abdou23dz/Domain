from encodings import search_function
import xml.etree.ElementTree as ET
import re
from xml.dom import minidom
import os 
def validate(domain):
    return re.match('''
        (?=^.{,253}$)          # max. length 253 chars
        (?!^.+\.\d+$)          # TLD is not fully numerical
        (?=^[^-.].+[^-.]$)     # doesn't start/end with '-' or '.'
        (?!^.+(\.-|-\.).+$)    # levels don't start/end with '-'
        (?:[a-z\d-]            # uses only allowed chars
        {1,63}(\.|$))          # max. level length 63 chars
        {2,127}                # max. 127 levels
        ''', domain, re.X | re.I)

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def search_domain(namedomain,ip):
    tree = ET.parse('Domain.xml')
    root = tree.getroot()
   # configurationProperty list 
    list_from_xml=[]
    list_without_space=[]
    list_with_out_pipe=[]
    list_of_ip_position=[]
    # creat lis from xml file it is name list_from_xml
    for d in root.findall(".//configurationProperty"):
        if None!= d.get('value'):
        #  print(d.get('value'))
         list_from_xml.append(str(d.get('value')))
    existe = False
    # print(list_from_xml)
    # creat list with  out | name:list_with_out_pipe
    for i in range(len(list_from_xml)):
         x=list_from_xml[i]  
         list_with_out_pipe.append(x.replace('|', ' '))
    # print(list_with_out_pipe) 
    # creat list with  out space name:list_with_out_space
    for g in list_with_out_pipe:
         list_without_space+= g.split()
        #  print(list_without_space) 
        # search position of all ip address  
    for i in range(len(list_without_space)):
         if(validate_ip(list_without_space[i])):   
              list_of_ip_position.append(i)
    # print(list_without_space) 
    # print(list_of_ip_position)
    # search ip in list of ip addres infime xml 
    postion_ip=-1
    for x in list_of_ip_position:
        if str(ip) in list_without_space[x]:
           postion_ip=x  
    #    search in list in xml file in ip addres exicet in file
    # print(postion_ip)
    if(postion_ip>=0):
        if(postion_ip==list_of_ip_position[len(list_of_ip_position)-1]):
            for a in range(int(postion_ip),int(len(list_without_space))):
                if namedomain in list_without_space[a] :
                    existe = True      
                 
        else:  
             for a in range(int(postion_ip),int(list_of_ip_position[list_of_ip_position.index(postion_ip)+1])):
                 if namedomain in list_without_space[a] :
                     existe = True        
    else : existe=False
    return existe
def update_xml_file(ip_address,domain):
    tree = ET.parse('Domain.xml')
    root = tree.getroot()
    postion_ip_line=0
    postion_line=0
    is_here=False
    # search position of ip_adress in xml file
    for d in root.findall(".//configurationProperty"):
        if( None != d.get('value')):
              if(is_here!=True):
                  if ip_address == str(d.get('value')):
                       postion_ip_line=postion_ip_line+1
                       is_here=True 
                  postion_ip_line=postion_ip_line+1   
    # search next line for add domain name in xml file
    if(is_here):
           for d in root.findall(".//configurationProperty"):
                if( None != d.get('value')):
                    postion_line=postion_line+1
                if (postion_ip_line==postion_line):
                        tr=str(d.get('value'))+str(domain+'|')
                        d.set('value',tr)
                        print(d.text)
                        tree.write('Domain.xml',encoding='UTF-8',xml_declaration=True)   
    return is_here       

def check_domain(file_path,name_domain):
    search=False
    lines = []
    with open(str(file_path)) as f:
         lines = f.readlines()


    for line in lines:
         p2=line.index('"',2)
         print(line[1:p2])
         if( line[1:p2] in name_domain): 
           search=True  
         
    return search
def check_domain_2(file_path,name_domain):
    lines = []
    search =False
    with open(file_path) as f:
         lines = f.readlines()

    for line in lines:
         if( line[:(len(line)-2)] in name_domain): 
           print(line)  
           search=True 

    return  search        
def check_ip(ip_address):
    search_Ip=False
    for x in list_of_ip_position:
        if str(ip) in list_without_space[x]:
           postion_ip=x  
        
domain='zi.goole.com'
ip_address='2.4.2.2' 
search=False
if(validate(domain)):

    if search_domain(domain,ip_address):
         print( ' existe in XML file')
         print(True)
    elif(check_domain('globaldomain.txt',domain)):
          search=True
          print(search)
          print('in file 2')      
          update_xml_file(ip_address, domain)
    elif (check_domain_2('file3.txt',domain)):
           search=True
           print(search)
           print('in file 3')
    elif update_xml_file(ip_address,domain): 
         print("domain name add in file xml ")
    else:
        print("ip adress not found")     
else :
        print("ip adress or domain  name not found")            
