#################################################################################
import requests
from bs4 import BeautifulSoup

def get_esearch_example():

    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'

    params = {'db':'pubmed',
              'term':'pmc open access[filter] ' + 'breast cancer',
              'retmax': '5000'}

    response = requests.get(url, params=params)

    soup = BeautifulSoup(response.content)
    
    return soup

# This is a BeautifulSoup object - see above
esearch_example = get_esearch_example()

###################################################################################
# This returns a Response object.
def e_search(query=None, max_results=1000):
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    params = {'db':'pubmed',
              'term':'pmc open access[filter] ' + query,
              'retmax': max_results}
    response = requests.get(url, params=params)
    return response
    
    
# Note that this returns two values: the total count for that query and the list of retrieved IDs.
# Feel free to change it, but I thought it might be helpful
def e_search_id_list(query=None, max_results=1000):
    
    response = e_search(query, max_results)
    soup = BeautifulSoup(response.content)
    count = soup.find('count').text
    ids = [tag.text for tag in soup.find_all('id')]
    
    print('Total results: ', count)
    print('Results returned: ', len(ids))
    
    return ids
######################################################################################

## This stuff is for checkpointing the results

from ediblepickle import checkpoint
import os

if not os.path.exists('papers-json'):
    os.mkdir('papers-json')

def id_key(args, kwargs):
    return args[0] + '.pkl'    

# This formats the URL for the BioC API.
# You would basically just use the IDs from the previous step
def format_bioC_url(paper_id, format_='xml', encoding='unicode'):
    '''Generate a bioC_url for a particular PubMed Central article based on its ID.'''
    url = ('https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/'
           f'BioC_{format_}/{paper_id}/{encoding}')
    return url




# This takes in an ID, makes an HTTP request,
# and returns the parsed BeautifulSoup object.
@checkpoint(key=id_key, work_dir='papers-json')   
def get_paper_bioC(paper_id, format_='json'):
    '''Fetch a machine-readable paper from PubMed Central given its ID.'''
    url = format_bioC_url(paper_id, format_)
    
    response = requests.get(url)
    return response
##############################################################################################


























