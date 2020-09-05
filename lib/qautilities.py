##example template
import requests

def cool_function(x):
    print("hey this is a cool function")
    print(f"here's that argument you specified: {x}")
    
    
def call_cool_function(x):
    cool_function(x)
    
def requests_something(x):
    response = requests.get('http://python.org')
    return response
#################################################################33
from transformers import AutoTokenizer, AutoModelForQuestionAnswering , QuestionAnsweringPipeline
import torch

import torch.nn.functional as F

# Working with the {ID, passage} dictionaries
def get_answer(question, passage_dict, title_dict,tokenizer,model):
    '''question is a string for one question, passage_dict is a dictionary with 'paper_id and 'passage_text'. '''

    text = passage_dict['passage_text'][:1000]
    paper_id = passage_dict['paper_id']

    inputs = tokenizer.encode_plus(question, text, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]

    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer_start_scores, answer_end_scores = model(**inputs) 

    answer_start = torch.argmax(
        answer_start_scores
    )  # Get the most likely beginning of answer with the argmax of the score
    answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    start_confidence=F.softmax(torch.tensor(answer_start_scores),dim=1).cpu().detach().numpy()[0].max()
    end_confidence =F.softmax(torch.tensor(answer_end_scores),dim=1).cpu().detach().numpy()[0].max()
    score = (start_confidence+end_confidence)/2
    
    # If answer is '[CLS]' set to zero
    if (answer.startswith('[CLS]')) or (answer == ''):
        score = 0

    output = {
        'paper_id': passage_dict['paper_id'],
        'paper_title': title_dict[paper_id],
        'question': question,
        'answer': answer,
        'score': score,
        'passage': text
    }
    
    return output
    

# def answer_question_from_papers(question, text_data, title_dict):
#     answer_outputs = []
#     for passage_dict in text_data:

#         result = get_answer(question, passage_dict, title_dict)
#         answer_outputs.append(result)
#     return answer_outputs


import pandas as pd
    
def answer_df(question_answers):
    df = pd.DataFrame(question_answers).sort_values(by='score', ascending=False)
    
    return df

##############################################################################

def answer_from_text(question,text_data,title_dict,tokenizer,model):
    answer_outputs=[]
    for passage_dict in (text_data):
        result=get_answer(question,passage_dict,title_dict,tokenizer,model)
        answer_outputs.append(result)
    return answer_outputs


###############################################################################










