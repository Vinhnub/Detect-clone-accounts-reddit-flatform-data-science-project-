from sentence_transformers import SentenceTransformer, util
import torch
import re
import math
model = SentenceTransformer('all-MiniLM-L6-v2')

def splitAndEmb(text):
    document = []
    textSplit = re.split(r'(?<=[.?!])\s+', text)
    for l in range(len(textSplit)):
        emb = model.encode(textSplit[l], convert_to_tensor=True)
        detail = {"text": textSplit[l], "emb": emb}
        document.append(detail)
    return textSplit, document

def responses(query, document):
    countMatch = 0
    countMax = math.ceil((int(len(document))/100)*20)
    res = []
    queryEmb = model.encode(query, convert_to_tensor=True)
    for doc in document:
        sim = util.cos_sim(queryEmb, doc["emb"]).item()
        if sim >= 0.4:
            res.append(doc["text"])
            countMatch += 1

    if countMatch >= int(countMax):
        return True, res
    else:
        return False, res
    
text = """
    Huge discounts this weekend!
    Buy now and save up to 50% on selected items.
    Limited-time offer, don’t miss out.
    High-quality products at unbeatable prices.
    """
query = "special discount limited offer don’t miss"

textSplit, document = splitAndEmb(text)
result, res = responses(query, document)

print(result,res)