from summarize import load_FestText,load_Pegasus,find_sentence, extract_sentences_by_keywords,filter_top_n_games, summarize_by_Pegasus
from preDataBase import convert_keywordstype, store_keywords,get_all_reviews,store_summaries_for_all_games_positive, store_summaries_for_all_games_negative
from summarize import extract_similar_keywords_by_category

model = load_FestText()

keywords_by_category = extract_similar_keywords_by_category(model, top_n=15)

keyword = convert_keywordstype(keywords_by_category)
#store_keywords(keyword)
#키워드 추출하고 DB에 넣는거까지

positive_reviews_by_game, negative_reviews_by_game = get_all_reviews()


positive_reviews_top_10 = filter_top_n_games(positive_reviews_by_game, n=10)
negative_reviews_top_10 = filter_top_n_games(negative_reviews_by_game, n=10)


positive_sentences_by_category = extract_sentences_by_keywords(positive_reviews_top_10, keyword)
negative_sentences_by_category = extract_sentences_by_keywords(negative_reviews_top_10, keyword)

positive_summaries = summarize_by_Pegasus(positive_sentences_by_category)
negative_summaries = summarize_by_Pegasus(negative_sentences_by_category)

store_summaries_for_all_games_positive(positive_summaries)
store_summaries_for_all_games_negative(negative_summaries)
