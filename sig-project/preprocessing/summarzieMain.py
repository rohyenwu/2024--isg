from summarize import load_FestText,load_Pegasus
from summarize import extract_similar_keywords_by_category

model = load_FestText()

keywords_by_category = extract_similar_keywords_by_category(model, top_n=15)

print(keywords_by_category)