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

# This function checks the existance of the IP and subdomain in the XML file
def search_domain(namedomain,ip):
    tree = ET.parse('Domain.xml')
    root = tree.getroot()
   # configurationProperty lists
    list_from_xml=[]
    list_without_space=[]
    list_without_pipe=[]
    list_of_ip_position=[]
    # Creates a list from xml file named list_from_xml. output ['1.1.1.1', 'Line1Domain1|Line1Domain2|Line1Domain3|', '2.2.2.2', 'Line2Domain1|']
    for d in root.findall(".//configurationProperty"):
        if None!= d.get('value'):
        #  print(d.get('value'))
         list_from_xml.append(str(d.get('value')))
    existe = False
    # print(list_from_xml)
    # Creates list that replaces "" with "|" because splitting based on | didn't work for some reason. list is named :list_without_pipe
    # output ['1.1.1.1', 'Line1Domain1 Line1Domain2 Line1Domain3 ', '2.2.2.2', 'Line2Domain1 ']
    for i in range(len(list_from_xml)):
         x=list_from_xml[i]  
         list_without_pipe.append(x.replace('|', ' '))
    # Print(list_without_pipe) 
    # Creates list without spaces named :list_with_out_space. output ['1.1.1.1', 'Line1Domain1', 'Line1Domain2', 'Line1Domain3', '2.2.2.2', 'Line2Domain1']
    for g in list_without_pipe:
         list_without_space+= g.split()
        # print(list_without_space) 
        # search position of all ip address  
    for i in range(len(list_without_space)):
         if(validate_ip(list_without_space[i])):   
              list_of_ip_position.append(i)
    # print(list_of_ip_position)
    # This looks for valid IPs in the final list and keeps their positions in a separate list called position_ip
    for x in list_of_ip_position:
        if str(ip) in list_without_space[x]:
           postion_ip=x  
        #    print(ip) 
        
#   After we check if an the given IP of the server is present in the XML file, this checks if the subdomain exists between that IP position and the next one
    for a in range(int(postion_ip),int(list_of_ip_position[list_of_ip_position.index(postion_ip)+1])):
        if namedomain in list_without_space[a] :
            existe = True        
    return existe


def check_domain(file_path,name_domain):
    search=False
    lines = []
    with open(str(file_path)) as f:
         lines = f.readlines()

    for line in lines:
         if( line[:(len(line)-2)] in name_domain): 
           search=True  
         
    return search


domain='2.2.2.2:80'
ip_address='1.1.1.1' 
search=False

if search_domain(domain,ip_address):
    print( ' Exists in XML file')
    print(True)
elif(check_domain('globaldomain.txt',domain)):
    search=True
    print(search)
    print('Exists global approved domains')           
elif (check_domain('file3.txt',domain)):
    search=True
    print(search)
    print('Exists in custom approved domains')
else:
    print ('Non existant domain')
    #print(search) 

          
