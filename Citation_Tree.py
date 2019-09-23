# to be done:-

# 1. also get "next page"
# 2. avoid empty data error

# download Chrome Driver at https://chromedriver.chromium.org/downloads
# make sure the driver you used w.r.t your Chrome version

import bibtexparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

# for drawing graphs
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

def search_by_head_tail(longText,head,tail):
    # this function will search for the first head matching the result
    # and then the first tail after the first head
    
    posi_start=longText.find(head)
    posi_end=longText.find(tail,posi_start)
    length_head=len(head)
    phase_extracted=longText[(posi_start+length_head):posi_end]
    
    return phase_extracted

def cut_string(str,max_length):
    str_slices=str.split()
    
    l_total=0
    str_total=''
    for word in str_slices:
        l=len(word)
        if l_total+1+l<=max_length:
            if str_total=='': #initial position
                str_total=word
            else:
                str_total=str_total+' '+word
            l_total=l_total+1+l
        else:
            str_total=str_total+'\n'+word
            l_total=l
    
    return str_total

def sort_dict(data_papers,column_i):
    # this function will sort the papers by years
    
    #x[1] refers to value of x, while x[0] is the key.
    data_papers_sorted_list=sorted(data_papers.items(), key=lambda x: x[1][column_i]) 

    # convert the list back into the dictionary
    data_papers_sorted={}
    for paper in data_papers_sorted_list:
        data_papers_sorted[paper[0]]=paper[1]      
    
    return data_papers_sorted

def vertices_less_dense(posi):
    # this function makes the vertices less dense in graph
    
    coord=np.array(list(posi.values()))
    # distance matrix times 100 so that they won't be selected as the min value
    distance_vrt=np.ones((num_vertices,num_vertices))*100 

    # calculate distance
    for i in range(num_vertices-1):
        for j in range(i+1,num_vertices):
            distance_vrt[i,j]=np.linalg.norm(coord[i]-coord[j])
            # distance_vrt[j,i]=distance_vrt[i,j]

    idx_min = np.argmin(distance_vrt, axis=1)

    # range from num-1,...,0 (ignore num-1 since that don't contain useful info)
    for i in range(num_vertices-1):
    
        # in a sorted DAG, for every pair of vertices, 
        # one vert is at the "up-side", while one is at the "down side"
        i_up=i
        i_down=idx_min[i]
    
        # drive vertice of i_down away from the cloest point
        dist_desired=0.7
        dist_now=np.linalg.norm(coord[i_up]-coord[i_down])
        shift_factor=(dist_desired-dist_now)*1
        coord[i_up]=coord[i_up]+(coord[i_up]-coord[i_down])*shift_factor
    
    posi_new={}
    i=0
    for x in posi:
        posi_new[x]=coord[i]
        i+=1
    
    return posi_new

# sometimes we used /abs/, sometimes we used /#abs/. Depending on situation
linkPrefix = "https://ui.adsabs.harvard.edu/#abs/"
absLinkSuffix = "/abstract"
refLinkSuffix = "/references"

# note that the .bib need to form a DAG. If not, please remove some papers
bibtex_path="C:\\Users\\Lanston\\Documents\\GitHub\\Citation_Tree_Python\\Many_Papers_DAG.bib"

chrome_driver_path="C:\\Users\\Lanston\\Documents\\GitHub\\Citation_Tree_Python\\chromedriver.exe"
    
bibtex_file = open(bibtex_path, encoding='utf8')
bib_database = bibtexparser.load(bibtex_file)

papers=bib_database.entries
num_papers=len(papers)

# open chrome
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# surf Google as an initialization to keep time for later parts consistent
driver.get("https://www.google.com/")
time.sleep(3)

##### Section: Get paper's data #####

print("###    Section 1: Web scrapping    ###")

data_all_papers={}
j=0
for paper in papers:
    
    j+=1
    print("Paper: "+str(j)+" of "+str(num_papers))
    
    if 'arxivid' in list(paper.keys()):
        arXivID_before=paper['arxivid']
            
        if 'author' in list(paper.keys()):
            author=paper['author']
        else:
            author=''
            
        if 'year' in list(paper.keys()):
            year=paper['year']
        else:
            year=''
    
        # remove version number, which would not be used in the url
        vPosi=arXivID_before.find('v')
        if vPosi==-1:
            arXivID=arXivID_before
        else:
            arXivID=arXivID_before[0:vPosi]

        # get Bibcode and title of the paper
        absLink = linkPrefix + arXivID + absLinkSuffix    
        driver.get(absLink)
        time.sleep(3)
    
        pageSourceAbs=driver.page_source
    
        bibCode=search_by_head_tail(pageSourceAbs,"bibcode=","\"")

        title=search_by_head_tail(pageSourceAbs,"<title>","</title>")
        
        # use Chrome to check Reference page
        refLink = linkPrefix + arXivID + refLinkSuffix    

        # get reference info
        driver.get(refLink)
        time.sleep(3)
    
        # get source code
        pageSourceRef=driver.page_source
        
        num_Ref=search_by_head_tail(pageSourceRef,"References\n","</span>\n")
        num_Ref=search_by_head_tail(num_Ref,"(",")")
        print("Refrences: ("+str(num_Ref)+")")
    
        # find the position of papers' titles
        positions=[m.start() for m in re.finditer("h3 class", pageSourceRef)]
        num_papers_one_page = len(positions)
        positions.insert(0,0)

        list_children=[]
        for i in range(num_papers_one_page):
            posi_start=positions[i]
            posi_end=positions[i+1]
            posi_a_start=pageSourceRef.rfind("<a href=\"#", posi_start, posi_end)
            posi_a_end=pageSourceRef.rfind("\" class=\"", posi_start, posi_end)
            link_partial=pageSourceRef[(posi_a_start+10):posi_a_end]
            bibCode_child_i=link_partial[(link_partial.find('abs/')+4):link_partial.find('/abstract')]
            list_children.append(bibCode_child_i)
        
        vrt_name_one_line = title + ' - ' + author + ' - ' + year
        vrt_name_multi_lines=cut_string(vrt_name_one_line,25)
        
        # keep vrt_name_multi_lines,list_children to be the last two entries!!!
        one_paper_data=[author,year,title,arXivID,num_Ref, \
                        vrt_name_multi_lines,list_children]
        data_all_papers[bibCode]=one_paper_data

driver.close()

print("###    Section 2: Draw Graph    ###")

##### Section: remove non selected children; create data frame #####

# sort papers by years; 1 means the "2nd column" of one_paper_data
data_all_papers=sort_dict(data_all_papers,1)   
      
bibCode_all_papers=list(data_all_papers.keys())
    
from_all_papers=[]
to_all_papers=[]
for bibCode_one_paper, data_one_paper in data_all_papers.items():
    list_children=data_one_paper[-1]
    list_children_remained=[x for x in list_children if x in bibCode_all_papers]
    data_one_paper[-1]=list_children_remained
    data_all_papers[bibCode_one_paper]=data_one_paper
    
    # create data frame
    num_child=len(list_children_remained)
    
    vrt_name_children_remained=[]
    for bibCode_child_i in list_children_remained:
        vrt_name_multi_lines=data_all_papers[bibCode_child_i][-2]
        vrt_name_children_remained.append(vrt_name_multi_lines)

    vrt_name_one_paper=data_all_papers[bibCode_one_paper][-2]
        
    from_one_paper=vrt_name_children_remained # the older paper
    to_one_paper=[vrt_name_one_paper]*num_child # the newer paper
    
    # concatenate the lists
    from_all_papers=from_all_papers+from_one_paper
    to_all_papers=to_all_papers+to_one_paper

##### Section: Draw Graph #####

# Build a dataframe with 4 connections
df = pd.DataFrame({ 'from':from_all_papers, 'to':to_all_papers})
 
# Build your graph
G=nx.from_pandas_dataframe(df, 'from', 'to', create_using=nx.DiGraph())

# determine vertices' coordinate
if not nx.is_directed_acyclic_graph(G):
    raise TypeError('Cannot to a graph that is not a DAG')

vertices_sorted=list(nx.topological_sort(G))

num_vertices=len(vertices_sorted)

posi={}
for i in range(num_vertices):
    vrt_name=vertices_sorted[i]
    posi_vert=-i/num_vertices
    posi_hori=random.random()
    posi[vrt_name]=np.array([posi_hori,posi_vert])

# make the vertices less dense
posi_new = vertices_less_dense(posi)

# logic similar to the EM algorithm to get a "good graph"
for i in range(round(num_vertices*1.4)):
    posi_new = vertices_less_dense(posi_new)

# if the graph doesn't look good, change figsize and rerun the last 3 lines
plt.figure(1,figsize=(18,18)) 
nx.draw(G,pos=posi_new,with_labels=True, node_size=150, arrows=True)
plt.show()