from summarize import load_FestText,load_Pegasus,find_sentence, extract_sentences_by_keywords,filter_top_n_games, summarize_by_Pegasus,calculate_score
from preDataBase import convert_keywordstype, store_keywords,get_all_reviews,store_summaries_for_all_games_positive, store_summaries_for_all_games_negative,get_review_by_game,store_scores
from summarize import extract_similar_keywords_by_category

model = load_FestText()

keywords_by_category = extract_similar_keywords_by_category(model, top_n=15)

keyword = convert_keywordstype(keywords_by_category)
#store_keywords(keyword)
#키워드 추출하고 DB에 넣는거까지
game_id=[16,29,1,594,13,463,163,248,634,521]
for i in game_id:
    # 게임당 모든 리뷰 가져오기+한 뭉치로 만들기 (리뷰를 모두 하나의 문단으로 만들기)
    reviews=get_review_by_game(i)    
    # 가져온 리뷰 문장단위로 나누기
    
    # 문장 단위로 나눠져있는거 극성판단하기
    
    # 키워드별로 극성판단된 문장 나누기(아마 8개로 나눠질듯 카테고리 4개 극성2개), 키워드별로 문장을 뽑으면 카테고리,극성, 리뷰내용 이렇게 되는데 이ㄸㅐ 문장을 합쳐서 요약해야함 이때 개수세기
    
    # 나눠진 문장들 요약해서 gameid와 함께 요약 리뷰 db에 저장
    
    # 나눠진 문장들 개수 파악해서 점수 매기기
    graphicScore=calculate_score(graphicPositiveNum, graphicNegativeNum)
    soundScore=calculate_score(soundPositiveNum, soundNegativeNum)
    stroyScore=calculate_score(stroyPositiveNum, stroyNegativeNum)
    creativityScore=calculate_score(creativityPositiveNum, creativityNegativeNUm)
    
    # 점수 매길때 이미 극성판단된 문장 카테고리별로 뽑아서 문장을 하나로 뭉쳐서 요약하는데 뭉칠때 문장 하나씩 뭉치는데 이때 각 카테고리와 극성에 맞게 ++시켜줘서 갯수파악 가능
    store_scores(i,graphicScore, soundScore,stroyScore,creativityScore)
    
    
    
    
    
    
    
# positive_reviews_by_game, negative_reviews_by_game = get_all_reviews()


# positive_reviews_top_10 = filter_top_n_games(positive_reviews_by_game, n=10)
# negative_reviews_top_10 = filter_top_n_games(negative_reviews_by_game, n=10)


# positive_sentences_by_category = extract_sentences_by_keywords(positive_reviews_top_10, keyword)
# negative_sentences_by_category = extract_sentences_by_keywords(negative_reviews_top_10, keyword)

# positive_summaries = summarize_by_Pegasus(positive_sentences_by_category)
# negative_summaries = summarize_by_Pegasus(negative_sentences_by_category)

# store_summaries_for_all_games_positive(positive_summaries)
# store_summaries_for_all_games_negative(negative_summaries)