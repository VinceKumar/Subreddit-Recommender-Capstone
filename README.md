# Capstone
Capstone Project for Galvanize: Data Science Immersive


## Introduction
Reddit is the 4th most visited site in the US([Alexa](http://www.alexa.com/topsites/countries/US)). It is an aggregation of online discussion communities. Each content community is known as a subreddit; users can post links to other websites or create texts posts, which can be upvoted/downvoted based on the quality of the content. Then a discussion takes place, based on this post. There is a full spectrum of subreddits(topics) including science, politics, music, various image types, jokes, news, and gaming.

There are currently over 1 million subreddits. It can be overwhelming having to deal with a list of that many choices, so I thought it would be a great opportunity to make a recommender, since nobody has time to look through a list of a million subreddits to see what they might like. 

<img src="https://raw.githubusercontent.com/VinceKumar/Subreddit-Recommender-Capstone/master/img/timeparadox.png" width="450">    <img src="https://raw.githubusercontent.com/VinceKumar/Subreddit-Recommender-Capstone/master/img/meme1.png" width="250">

## The Dataset

This [dataset](https://www.reddit.com/r/datasets/comments/3bxlg7/i_have_every_publicly_available_reddit_comment/) was found on [r/datasets](https://www.reddit.com/r/datasets/) It has all public comment data from 2007 to 2015, which is about 1.8 billion comments, totaling about 1 TB. 


<img src="https://raw.githubusercontent.com/VinceKumar/Subreddit-Recommender-Capstone/master/img/pyramid.png" width="400">

## The Method

The approaches used in recommender systems are either: Collaborative filtering, Content-based filtering, or Hybrid recommender systems. Collaborative filtering makes recommendations on users by finding the most similar users are and what they like might also be what the user will like also. Content-based filtering recommends items that are similar to those that a user liked in the past, commonly uses TF-IDF(term frequency–inverse document frequency) to find items that are similar. Hybrid recommender systems are usually better because they take the best of both worlds. 

Collaborative filtering (CF) seemed like it would work the best under the time constraint and the mass amount of user data. It tends to fail when there are not many similar users compared to the desired user to make a recommendation on. If a user is into [r/opera](https://www.reddit.com/r/opera/), [r/machinelearning](https://www.reddit.com/r/MachineLearning/), [r/Nickelback](https://www.reddit.com/r/Nickelback/), and [r/metal](https://www.reddit.com/r/Metal/). There are very few users similar to this user therefore it will be difficult to make recommendations on this user. 

Content-Based Filtering (CBF) seemed like it would not be very consistent considering how much sarcasm is on reddit, and it would not generalize many cases, where [r/bird](https://www.reddit.com/r/bird/) would be similar to [r/eagles](https://www.reddit.com/r/eagles/), when in reality the former subreddit is about birds and latter is about an NFL(football) team. Another case would be where users who are in communities with opposing views would probably not like a recommendation to a subreddit with completely opposite views. An example of that is [r/The_Donald](https://www.reddit.com/r/The_Donald/) is a subreddit for users who like Trump, while [r/MarchAgainstTrump](https://www.reddit.com/r/MarchAgainstTrump/) is a subreddit for people who dislike Trump. Also since subreddits are always one word, it would also probably not always split at the correct words. Is r/Overwatch Over watch or Overwatch? Is r/AdviceAnimals Ad vice Animals or Advice Animals?

I would build a Hybrid recommender if I were deploying this in the industry, but given my time and financial constraints, I will stick to just the CF. 

### Collaborative filtering 

Given a user to make a recommendation on, I find the most similar users based on where people have comment activity. Then aggregate where the 20 most similar users have comment activity in minus where the original user already has comment activity in and take votes for each user per subreddit. Whichever subreddits have the most votes, will the top recommendations in a descending fashion by the number of votes. 

<img src="https://raw.githubusercontent.com/VinceKumar/Subreddit-Recommender-Capstone/master/img/tables.png" width="800">


In the figure above, to make a recommendation for Gavin. Gavin is the most similar to Richard, Nelson, and Gilfoyle. The three of these guys together all have comment activity in technews, therefore technews would be the first recommendation. The next recommendation would be programming, because 2/3 have comment activity there. Last would be compsci, since Richard is the most similar user and has comment activity there. The recommendations for Gavin in ranked order would be technews, programming, and compsci. 


## To Run


### Steps:

1. Torrent data onto an EC2 (I recommend this way, because it gets around the bottleneck of your ISP's upload speeds)
2. Upload the unzipped data onto your S3 bucket all in the same directory
3. Launch cluster(EMR) on AWS 

 ``` 
 bash launch_cluster.sh mybucket_name mypem 20
 ```
launch_cluster.sh  Takes three arguments:  
  - bucket name - one that has already been created
  - name of key file - without .pem extension
  - number of slave instances   
***Modify script as needed
 
4. Run PySpark with jupyter kernel in EMR and create SSH tunnel 
5. Run Jupyspark kernel and connect on your tunneled Jupyter notebook

##### Spark

1. Create an instance of Pyspk:
     ```
     spark_data = Pyspk(INSERT S3 READ LINK, UTC TIME SPLIT) 
     ```
 
  UTC time split will split everything after the specified time to be test data, and everything before to be training data. 
  
2. After it has finished running (few hours), you can write to s3 by calling the method of the instance __write_s3__, AWS credentials need to be initialized also to write. 
     ```
     spark_data.write_s3(s3_write_link)
     ```
3. There will be many csv's that will need to be concatenated, use an EC2 instance to do this. It should be much quicker than the previous steps

##### Pandas
1. Import csv of dataframe  
    ```
    df = pd.read_csv(concatenated_csv)
    ```
2. Create an instance of Pndas
    ```
    pandas_data = Pnds(df)
    ```

2. This will create a Utility matrix where the rows are Users and columns are subreddits
2. Then it will compute the user-user similarity between each user using Jaccard Similarity
3. Find the most similar users
4. Get Recommendations based on where most similar users have comment activity, for a list of users by:
    ```
    pandas_data.get_recommendations(user_list)
    ```
    which will return a dictionary of the user with its subreddit recomendations 


## Dependencies

* Spark 2.1
* Python 2.7.13 
* Numpy
* Pandas
* Scipy
