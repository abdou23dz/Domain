from encodings import search_function
import xml.etree.ElementTree as ET
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
         print(d.get('value'))
         list_from_xml.append(str(d.get('value')))
    existe = False
    print(list_from_xml)
    # creat list with  out | name:list_with_out_pipe
    for i in range(len(list_from_xml)):
         x=list_from_xml[i]  
         list_with_out_pipe.append(x.replace('|', ' '))
    print(list_with_out_pipe) 
    # creat list with  out space name:list_with_out_space
    for g in list_with_out_pipe:
         list_without_space+= g.split()
    print(list_without_space) 
        # search position of all ip address  
    for i in range(len(list_without_space)):
         if(validate_ip(list_without_space[i])):   
              list_of_ip_position.append(i)
    print(list_without_space) 
    print(list_of_ip_position)
    # search ip in list of ip addres infime xml 
    for x in list_of_ip_position:
        if str(ip) in list_without_space[x]:
           postion_ip=x  
           print(ip) 
        
#    search in list in xml file in ip addres exicet in file
    for a in range(int(postion_ip),int(list_of_ip_position[list_of_ip_position.index(postion_ip)+1])):
        if namedomain in list_without_space[a] :
            existe = True        

    return existe

domain='site.com'
ip_address='1.1.1.1' 
search=False
if search_domain(domain,ip_address):
    print( ' existe in XML file')
    search=True
else :   
     lines = []
     with open('globaldomain.txt') as f:
         lines = f.readlines()

     for line in lines:
         if( line[:(len(line)-2)] in domain): 
           print(line)  
           print( ' existe in globaldomain file')
           search=True 

print(search)            
