import glob
import os
import shutil
import sys
import re
from PIL import Image

MAX_IMG_SIZE = 1280

def convert_img(file):
    img = Image.open(file)
    longer_side = max(img.width, img.height)
    ratio = min(1, MAX_IMG_SIZE / longer_side)
    width = int(img.width * ratio)
    height = int(img.height * ratio)
    img_resized = img.resize((width, height))
    return img_resized

elements_dir = sys.argv[1]

if os.path.exists('generated/' + elements_dir):
    shutil.rmtree('generated/' + elements_dir)
os.mkdir('generated/' + elements_dir)

css_file = elements_dir + '/style.css'

langs = []
with open('lang.txt', 'r', encoding='utf-8') as f:
    for line in f.read().splitlines():
        dr = line.split()[-1]
        text = line.replace(' ' + dr, '')
        langs.append([dr, text])

with open('main_page_url.txt', 'r', encoding='utf-8') as f:
    main_page_url = f.readline()

with open(elements_dir + '/head.html', 'r', encoding='utf-8') as f:
    head = f.read()

with open(elements_dir + '/head2.html', 'r', encoding='utf-8') as f:
    head2 = f.read()

menu = '<div class="menu_bar">\n'
#menu += '<a class="menu_a" href="' + main_page_url + elements_dir + '"><img class="bar_icon" src="https://raw.githubusercontent.com/Nyanyan/Nyanyan.github.io/master/img/favicon.jpg"></a>\n'
with open(elements_dir + '/menu_elements.txt', encoding='utf-8') as f:
    menu_elems = f.read().splitlines()
    n_menu_elems = []
    for elem in menu_elems:
        link = elem.split()[-1]
        text = elem.replace(' ' + link, '')
        n_menu_elems.append([text, link])
    menu_elems = [elem for elem in n_menu_elems]
for text, link in menu_elems:
    if link[0] == '/':
        link = main_page_url + elements_dir + link
        menu += '<div class="menu_button"><a class="menu_a" href="' + link + '">' + text + '</a></div>'
    else:
        menu += '<div class="menu_button"><a class="menu_a" href="' + link + '" target="_blank" el=”noopener noreferrer”>' + text + '</div></a>\n'
menu += '</div>\n'

with open(elements_dir + '/tweet.html', 'r', encoding='utf-8') as f:
    tweet = f.read()

with open(elements_dir + '/foot.html', 'r', encoding='utf-8') as f:
    foot = f.read()

section_head1 = '<div>\n<h2>'
section_head2 = '</h2>\n'
section_foot = '</div>\n'

centering_head = '<div style="text-align: center">\n'
centering_foot = '</div>'

link1 = '<a href="'
link2 = '" target="_blank" el=”noopener noreferrer”>'
link3 = '</a>'

link21 = '<a href="'
link22 = '">'
link23 = '</a>'

def judge_raw_html(html_elem):
    html_tags = ['table', 'tr', 'td', 'th', 'a', 'div', 'ul', 'li', 'p', 'span', 'canvas', 'details', 'summary', 'code', 'label', 'script']
    count = 0
    for tag in html_tags:
        if '<' + tag in html_elem:
            count += 1
        elif '</' + tag in html_elem:
            count -= 1
    #print(html_elem)
    # ignore img, input, br
    return count

def create_html(dr):
    alternate = ''
    for lang in langs:
        if dr[3:]:
            alternate += '<link rel="alternate" href="' + main_page_url + lang[0] + '/' + dr[3:] + '/" hreflang="' + lang[0] + '" />\n'
        else:
            alternate += '<link rel="alternate" href="' + main_page_url + lang[0] + '/" hreflang="' + lang[0] + '" />\n'
    if dr[3:]:
        alternate += '<link rel="alternate" href="' + main_page_url + 'en/' + dr[3:] + '/" hreflang="x-default">\n'
    else:
        alternate += '<link rel="alternate" href="' + main_page_url + 'en/" hreflang="x-default">\n'
    with open(dr + '/index.md', 'r', encoding='utf-8') as f:
        md = f.read()
    md_split = md.splitlines()
    '''
    for i, elem in enumerate(md_split):
        # special replacements
        # section tags
        if elem[:2] == '# ':
            elem = '<h1>' + elem[2:] + '</h1>'
        if elem[:3] == '## ':
            elem = '<h2>' + elem[3:] + '</h2>'
        if elem[:4] == '### ':
            elem = '<h3>' + elem[3:] + '</h3>'
        # links
        links = re.findall('\[.+?\]\(.+?\)', elem)
        for link in links:
            text, url = link[1:-1].split('](')
            if url[0] != '.':
                html_link = link1 + url + link2 + text + link3
            else:
                html_link = link21 + url + link22 + text + link23
            elem = elem.replace(link, html_link)
        # bold
        bolds = re.findall('\*\*.+?\*\*', elem)
        for bold in bolds:
            html_bold = '<b>' + bold[2:-2] + '</b>'
            elem = elem.replace(bold, html_bold)
        # modify data
        md_split[i] = elem
    '''
    raw_html = 0
    for i, elem in enumerate(md_split):
        while elem and (elem[0] == ' ' or elem[0] == '\t'):
            elem = elem[1:]
        html_elems = re.findall('\<.+?\>', elem)
        for html_elem in html_elems:
            raw_html += judge_raw_html(html_elem)
        # section tags
        if elem[:2] == '# ':
            elem = '<h1>' + elem[2:] + '</h1>'
        elif elem[:3] == '## ':
            last_h3_title = elem[3:]
            elem = '<h2 id="' + elem[3:] + '">' + elem[3:] + '</h2>'
        elif elem[:4] == '### ':
            elem = '<h3 id="' + last_h3_title + '_' + elem[4:] + '">' + elem[4:] + '</h3>'
        elif elem[:5] == '#### ':
            elem = '<h4>' + elem[5:] + '</h4>'
        # links
        links = re.findall('\[.+?\]\(.+?\)', elem)
        for link in links:
            text, url = link[1:-1].split('](')
            if url[0] != '.':
                html_link = link1 + url + link2 + text + link3
            else:
                html_link = link21 + url + link22 + text + link23
            elem = elem.replace(link, html_link)
        # bold
        bolds = re.findall('\*\*.+?\*\*', elem)
        for bold in bolds:
            html_bold = '<b>' + bold[2:-2] + '</b>'
            elem = elem.replace(bold, html_bold)
        # code
        codes = re.findall('```.+?```', elem)
        for code in codes:
            html_code = '<code>' + code[3:-3] + '</code>'
            elem = elem.replace(code, html_code)
        # paragraph
        if raw_html == 0:
            elem = '<p>' + elem + '</p>'
        # img
        '''
        if elem[:4] == '<img':
            img_file_name = ''
            for elem_elem in elem.split():
                if elem_elem[:4] == 'src=':
                    last_idx = elem_elem.rfind('"')
                    img_file_name = elem_elem[5:last_idx]
                    img_file_name = img_file_name.replace('"', '').replace('>', '')
            if img_file_name:
                print(dr + '/' + img_file_name)
                img = Image.open(dr + '/' + img_file_name)
                shorter_side = min(img.width, img.height)
                ratio = min(1, MAX_IMG_SIZE / shorter_side)
                img_width = int(img.width * ratio)
                img_height = int(img.height * ratio)
                elem = '<img width="' + str(img_width) + '" height="' + str(img_height) + '"' + elem[4:]
        '''
        # modify data
        md_split[i] = elem
    this_page_url = main_page_url + dr
    with open(dr + '/title.txt', 'r', encoding='utf-8') as f:
        page_title = f.readline()
    html = ''
    html += '<div class="box">\n'
    html += '<p>\n'
    html += tweet.replace('DATA_URL', this_page_url).replace('DATA_TEXT', page_title) + ' \n'
    for lang_dr, lang_name in langs:
        original_lang = dr.split('/')[0]
        if lang_dr == original_lang:
            continue
        modified_dr = dr[len(original_lang) + 1:]
        lang_link = main_page_url + lang_dr + '/' + modified_dr
        html += link21 + lang_link + link22 + lang_name + link23 + ' \n'
    html += '</p>\n'
    try:
        with open(dr + '/head_additional.html', 'r', encoding='utf-8') as f:
            html += f.read()
            html += '\n'
    except:
        pass
    last_empty = False
    for line in md_split:
        if last_empty == False and line == '':
            last_empty = True
        else:
            if line:
                html += line
            else:
                html += line + '<br>\n'
            last_empty = False
    try:
        with open(dr + '/foot_additional.html', 'r', encoding='utf-8') as f:
            html += f.read()
            html += '\n'
    except:
        pass
    html += '</div>\n'
    head_title = '<title>' + page_title + '</title>\n'
    og_image = '<meta property="og:image" content="' + this_page_url + '/img/eyecatch.png" />\n'
    additional_head = '<meta property="og:url" content="' + this_page_url + '/" />\n'
    additional_head += '<meta property="og:title" content="' + page_title + '" />\n'
    #additional_head += '<meta property="og:description" content="' + meta_description + '" />\n'
    additional_head += '<link rel="canonical" href="' + this_page_url + '/">\n'
    #additional_head += '<meta name="description" content="' + meta_description + '"/>\n'
    out_dr = 'generated/' + dr
    if not os.path.exists(out_dr):
        os.mkdir(out_dr)
    with open(out_dr + '/index.html', 'w', encoding='utf-8') as f:
        f.write(head + alternate + og_image + head2 + head_title + menu + html + foot)
    shutil.copy(css_file, out_dr + '/style.css')
    if os.path.exists(dr + '/img'):
        img_files = glob.glob(dr + '/img/**')
        os.mkdir(out_dr + '/img')
        for file in img_files:
            resized_img = convert_img(file)
            file_name = file.split('\\')[-1]
            resized_img.save(out_dr + '/img/' + file_name)
    tasks = []
    try:
        with open(dr + '/tasks.txt', 'r', encoding='utf-8') as f:
            tasks = f.read().splitlines()
    except:
        pass
    if tasks:
        print(dr, 'new tasks', tasks)
        for task in tasks:
            create_html(dr + '/' + task)

create_html(elements_dir)
