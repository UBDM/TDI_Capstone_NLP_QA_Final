#!/usr/bin/env python
# coding: utf-8

# In[1]:



##example template


# In[ ]:


from lib.good_stuff import call_cool_function


# In[2]:


call_cool_function("this is a dumb function ....")


# In[ ]:


######################################################


# ## Pre-trained model 

# In[1]:


from transformers import AutoTokenizer, AutoModelForQuestionAnswering , QuestionAnsweringPipeline
import torch

tokenizer = AutoTokenizer.from_pretrained("ktrapeznikov/biobert_v1.1_pubmed_squad_v2")
model = AutoModelForQuestionAnswering.from_pretrained("ktrapeznikov/biobert_v1.1_pubmed_squad_v2")

nlp = QuestionAnsweringPipeline(model=model, tokenizer=tokenizer)


# ## Read Json 

# In[2]:


import json
# JSON file 
f = open ('all-papers.json', "r") 
  
# Reading from file 
all_papers = json.loads(f.read())


# # title_dict and text_data

# In[3]:


title_list_02=[]
for paper in all_papers:
    complete_title = ''
    paper_id = paper['id']
    for ps in paper['passages']:
        try:
            if ps['infons']['section_type']=='TITLE':
                complete_title += ' '
                complete_title += ps['text']
        except:
            pass
    passage_dict = {'paper_id':paper_id,
                           'title': complete_title}
    title_list_02.append(passage_dict)
        


# In[4]:


title_dict = {paper['paper_id']: paper['title'] for paper in title_list_02}


# In[5]:


title_dict


# In[6]:


text_data_02=[]
for paper in all_papers:
    complete_abstract = ''
    paper_id = paper['id']
    for ps in paper['passages']:
        try:
            if ps['infons']['type']=='abstract':
                complete_abstract += ' '
                complete_abstract += ps['text']
        except:
            pass
    passage_dict = {'paper_id':paper_id,
                           'passage_text': complete_abstract}
    text_data_02.append(passage_dict)
        


# ## Answer from text

# In[7]:


from lib.qautilities import answer_df


# In[8]:


from lib.qautilities import answer_from_text


# In[9]:


from IPython.display import display
import matplotlib.pyplot as plt


# In[10]:


#title_dict = {paper['paper_id']: paper['title'] for paper in title_list_02}


# In[11]:


import pandas as pd
for question in ['Which group developed a clinical practice guideline?',
                 'Which type of breast-cancer is most affected?',
                 'What recommendation to you give to stage 1 versus stage 2 cancer patients?',
                 'How does a surviorship plan look like for a stage 3  cancer patient?',
                 'How is the patient engagement rated in the cancer survivorship plans?']:
    result_answer = answer_from_text(question,text_data_02,title_dict,tokenizer,model)
    df = pd.DataFrame(result_answer).sort_values(by='score', ascending=False)
    df = answer_df(result_answer)
    display(df.head())
    plt.figure()
    df['score'].plot.hist()


# ## Follow up question

# In[14]:


import pandas as pd
result_answer = answer_from_text('Why is the elderly population most susceptible to breast cancer?',text_data_02,title_dict,tokenizer,model)
df = pd.DataFrame(result_answer).sort_values(by='score', ascending=False)
df = answer_df(result_answer)
display(df.head())
plt.figure()
df['score'].plot.hist()


# In[15]:


df.iloc[0].passage


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




