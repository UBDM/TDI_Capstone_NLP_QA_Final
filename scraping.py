#!/usr/bin/env python
# coding: utf-8

# ## get_esearch example

# In[ ]:


from lib.utilities import get_esearch_example


# In[5]:


import requests
from bs4 import BeautifulSoup


# In[6]:


esearch_example = get_esearch_example()


# In[7]:


# Get count
print('Total Results:', esearch_example.find('count'))

#Get IDs
ids = [x.text for x in esearch_example.find_all('id')]

# Note that 5000 IDS are returned because that was what we specified 
# for retmax in the example function above.
print('Number of IDs returned: {}'.format(len(ids)))

print('First 5 IDS', ids[:5])


# ## e-search , e-search-id-list

# In[8]:


from lib.utilities import e_search, e_search_id_list


# In[9]:


hello = ('Hello' 
         'World!')
         
print(hello)

query = ( '((((("survivorship care"[Title/Abstract]) OR '
          '("follow up plans"[Title/Abstract])) OR '
          '("patient care planning"[MeSH Terms])) OR '
          '("survivorship"[MeSH Terms])) OR '
          '("cancer survivors"[MeSH Terms])) AND '
          '(("breast cancer"[Title/Abstract]) OR '
          '(breast neoplasms[MeSH Terms]))' )


# In[10]:


# Get IDs
id_list = e_search_id_list(query)

#First 5 IDs
id_list[:5]


# In[13]:


short_list = id_list[:10]


# ## id_key, format_bioC_url, get_paper_bioC

# In[14]:


from lib.utilities import id_key, format_bioC_url, get_paper_bioC


# In[15]:


import json
parsed_papers = [json.loads(get_paper_bioC(x).text) for x in id_list]


# ## Continued, dump the json file

# In[16]:


all_papers = [paper['documents'][0] for paper in parsed_papers]


# In[17]:


import json


# In[18]:


with open('all-papers.json', 'w') as f:
    json.dump(all_papers, f)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




