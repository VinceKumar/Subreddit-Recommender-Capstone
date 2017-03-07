

# Project 1: reddit

1. Reddit is 7th most visited site in the US. It is an aggregation of online discussion communities. Each community is known as a subreddit, users can post links to other websites or create texts posts, which can be upvoted/downvoted based on the quality of the content. Then a discussion takes place, based on this post. Each individual comment. 
2. Trying to figure out what I could do with this exactly. Ideas?
	* What makes a top comment?
	* Determining if someone is a shill (hard to do)
	* Comparisons of subreddit's
	* __Subreddit recommender__
	* Fake News
	* How sarcasm affects NLP
	
3. Web app/slides/Blog post
4. Scrape data and do EDA 
5. Data & Resources  
  * I was able to obtain all the public reddit comments for about 7 years (~1.7 billion comments, with all the details) {It's about 1 TB of data}.   
	Sample: 
		```
		{"parent_id":"t1_cnarldl","subreddit":"hockey","edited":false,"subreddit_id":"t5_2qiel","controversiality":0,"author_flair_text":"CGYNHL","gilded":0,"author_flair_css_class":"CGYNHL","retrieved_on":1425122408,"ups":1,"name":"t1_cnaw9mz","link_id":"t3_2qy9rp","score_hidden":false,"author":"LetsPlayPoopshoots","score":1,"archived":false,"id":"cnaw9mz","distinguished":null,"body":"Seriously?! what address did you use to connect to Russia?","created_utc":"1420080111","downs":0}		```
  
 
_____________________


# Project 2: Bitcoin Sentiment Analysis Prediction
 

1. Bitcoin is the most popular cryptocurrency. The system is decentralized, meaning no single entity has power over it. It's price is extremely volatile due to the low market cap, and limited supply of new bitcoins.  Therefore, the price can fluctuate by extreme amounts in a short period of time. The general trend I see, is a long plateau period and then sudden news causes a mass trigger of buy or sell. The idea of this project is to save me time reading for hours trying to figure out the general census on what is happening
2. Live scrape r/btc, r/bitcoin, r/bitcoinmarkets, CoinDesk, NewsBTC, for sentiment analysis on bitcoin price prediction (BONUS: if can scrape data from chinese sites)
-- I have applied for access to the Reddit API 
3. Web app/slides/Blog post
4. Scrape data and do EDA 
5. Data & Resources  
  * API for BTC pricing: 
     * https://www.blocktrail.com/api/
  * API for 70 news sources:    
     *  https://newsapi.org
    
_________________________
#Project 3: 

Develop/implement a genetic algorithm that detects cancer based on genome sequence data