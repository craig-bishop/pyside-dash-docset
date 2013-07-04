from bs4 import BeautifulSoup
import sqlite3
import os.path
import re

APPLE_REF = '//apple_ref/cpp/{0}/{1}'

conn = sqlite3.connect('docSet.dsidx')
db = conn.cursor()
try:
  db.execute('DROP TABLE searchIndex;')
except:
  pass
db.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, '
    'type TEXT, path TEXT);')
db.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

with open('contents.html', 'r') as file:
  contents_html = file.read()

soup = BeautifulSoup(contents_html)
modules_tag = soup.find(class_='toctree-wrapper').ul
module_tags = modules_tag.find_all('a')
toplevel_link = modules_tag.find(href="modules.html")
module_tags.remove(toplevel_link)
modules = {}
for module_link in module_tags:
  name = module_link.string
  link = module_link['href']
  modules[name] = link
  db.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES "
      "('{0}', '{1}', '{2}');".format(name, "Module", link))
  print(name + ' - ' + link)

classes = {}

for module_name, filename in modules.items():
  module_base_path = os.path.dirname(filename)
  with open(filename, 'r') as file:
    soup = BeautifulSoup(file.read())
  toc_container = soup.find(class_='pysidetoc')
  toc_links = toc_container.find_all('a', class_='reference internal')
  for toc_link in toc_links:
    name = toc_link.string
    if not name.startswith('Q'):
      continue
    link = toc_link['href']
    link = module_base_path + '/' + link
    db.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES "
        "('{0}', '{1}', '{2}');".format(module_name + '.' + name,
        "cl", link))
    classes[module_name + '.' + name] = link
    print(module_name + '.' + name + ' - ' + link)

member_count = 0

for class_name, filename in classes.items():
  print("Parsing members for " + class_name)
  with open(filename, 'r') as file:
    soup = BeautifulSoup(file)
  function_tags = soup.select("#functions ul li a.reference")
  for func_link in function_tags:
    name = class_name + '.' + func_link.string
    link = filename + func_link['href']
    db.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES "
        "('{0}', '{1}', '{2}');".format(name, "clm", link))
    member_count += 1
    anchor_tag = soup.new_tag('a')
    header_link = soup.find(class_='headerlink',
        href=re.compile('.*' + name.replace('.', '\\.')))
    header_link.insert_before(anchor_tag)
    anchor_tag['name'] = APPLE_REF.format("clm", func_link.string)
    #print(name + ' - ' + link)

  function_tags = soup.select("#virtual-functions ul li a.reference")
  for func_link in function_tags:
    name = class_name + '.' + func_link.string
    link = filename + func_link['href']
    db.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES "
        "('{0}', '{1}', '{2}');".format(name, "clm", link))
    member_count += 1
    anchor_tag = soup.new_tag('a')
    header_link = soup.find(class_='headerlink',
        href=re.compile('.*' + name.replace('.', '\\.')))
    header_link.insert_before(anchor_tag)
    anchor_tag['name'] = APPLE_REF.format("clm", func_link.string)
    #print(name + ' - ' + link)

  function_tags = soup.select("#static-functions ul li a.reference")
  for func_link in function_tags:
    name = class_name + '.' + func_link.string
    link = filename + func_link['href']
    db.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES "
        "('{0}', '{1}', '{2}');".format(name, "clm", link))
    member_count += 1
    anchor_tag = soup.new_tag('a')
    header_link = soup.find(class_='headerlink',
        href=re.compile('.*' + name.replace('.', '\\.')))
    header_link.insert_before(anchor_tag)
    anchor_tag['name'] = APPLE_REF.format("clm", func_link.string)
    #print(name + ' - ' + link)

  function_tags = soup.select("#slots ul li a.reference")
  for func_link in function_tags:
    name = class_name + '.' + func_link.string
    link = filename + func_link['href']
    db.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES "
        "('{0}', '{1}', '{2}');".format(name, "clm", link))
    member_count += 1
    anchor_tag = soup.new_tag('a')
    header_link = soup.find(class_='headerlink',
        href=re.compile('.*' + name.replace('.', '\\.')))
    header_link.insert_before(anchor_tag)
    anchor_tag['name'] = APPLE_REF.format("clm", func_link.string)
    #print(name + ' - ' + link)

  function_tags = soup.select("#signals ul li a.reference")
  for func_link in function_tags:
    name = class_name + '.' + func_link.string
    link = filename + func_link['href']
    db.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES "
        "('{0}', '{1}', '{2}');".format(name, "clm", link))
    member_count += 1
    anchor_tag = soup.new_tag('a')
    header_link = soup.find(class_='headerlink',
        href=re.compile('.*' + name.replace('.', '\\.')))
    header_link.insert_before(anchor_tag)
    anchor_tag['name'] = APPLE_REF.format("Attribute", func_link.string)
    #print(name + ' - ' + link)

  file = open('PySide.docset/Contents/Resources/Documents/' + filename, 'wb')
  file.write(soup.prettify('utf-8'))
  file.close()

print('\n')
print('\n')
print("Added {0} modules.".format(len(modules)))
print("Added {0} classes.".format(len(classes)))
print("Added {0} members.".format(member_count))

conn.commit()
conn.close()
