import numpy as np
import pandas as pd
import pyspark as ps
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql import functions
import operator
from scipy.spatial.distance import pdist, jaccard


class Pyspk(object):
    """Used to filter dataset in spark(parallelization)
       Write filtered CSV to S3
       Then finish preprocessing in Pandas
       Split Train/Test at UTC time
       
        Args:
            s3_read_link: (str) link to s3 dataset
            utc_split: (int) where to split the data into train/test 
                everything before the utc_split is train and everything after 
                is test data 
    """

    def __init__(self, s3_read_link,utc_split):
        self.utc_split = utc_split
        self.df = self.read_data(s3_read_link)
        self.df_filtered = self._spark_filter()
        self.train, self.test = self.split(self.utc_split)



    def read_data(self,s3_read_link):
        """
        Loads data into spark using read json method from s3 link
        
        Args:
            s3_read_link: (str) link to s3 dataset
        """
        return spark.read.json(s3_read_link)

    def _spark_filter(self):
        """
        Filter criteria used:
            - Keep users with more than 60 posts
            - Keep users who did not delete their accounts
        
        """
        result_filtered_users = self.df.groupBy(
            'author').count().where('count>60').where('author != "[deleted]"')
        df_filtered = self.df[self.df.author.isin(set(result_filtered_users.toPandas().author.tolist()))]

        return df_filtered.select('author', 'subreddit', 'created_utc')

    def split(self,utc_split):
        '''Split the data like a time series data at a certain utc threshold (utc_split)
        Everything below utc is training data and everything equal to or after utc_split
        is considered test data

        '''
        train = self.df_filtered.select('author', 'subreddit', 'created_utc').where('created_utc < {} '.format(utc_split))   
        test = self.df_filtered.select('author', 'subreddit', 'created_utc').where('created_utc >= {} '.format(utc_split))

        return train, test

    def to_pandas(self, df):
        return df.toPandas()

    def write_s3(self, data_frame, s3_write_link):
        """
        Will write to S3 bucket in several csv's. Use CLI to merge them into one
        
        """
        data_frame.write.csv(s3_write_link)


class Pndas(object):
    """Process Filtered/Cleaned data from Spark using Pandas methods
       These are the steps this class does:
        1. Create Utility matrix (rows = Users, columns = subreddits)
        2. Compute user-user similarity between each user (Jaccard Similarity)
        3. Find the most similar users
        4. Get Recommendations based on where most similar users have comment activity
    
        Args:
            df: (DataFrame) Cleaned/Filtered DataFrame
    """

    def __init__(self, df):
        self.author = None
        self.df = df
        self.df_utility_matrix = self._utility_matrix()
        self.jaccard_user_similarity = jaccard_similarity_matrix()
        self.user_similarity_dict = {}
        self.top_users_ranked = rec_builder()

    def _utility_matrix(self):
        '''Creates a Utility Matrix with users as rows and subreddits as columns

        Args:

        Returns:
            Pandas dataframe: df_utility_matrix

        '''

        df_utility_matrix = pd.crosstab(self.df['author'], self.df[
                                        'subreddit']).reset_index()

        # Convert nonzero terms to 1
        self.author = df_utility_matrix.pop('author')
        df_utility_matrix = (df_utility_matrix /
                             df_utility_matrix == 1).astype(int)
        df_utility_matrix.insert(0, 'author', self.author)
        # df_utility_matrix.info()
        # df_utility_matrix.head()
        return df_utility_matrix

    def jaccard_similarity_matrix(self):
        '''Computes the Jaccard Similarity for each user to all other users in the
        Original set of users

        Args: 

        Returns:
            jaccard_user_similarity: (np array) array comparing similarity for each user with 
            every other user 

        '''

        author = self.df.pop('author')
        util_matrix_vals_np = self.df.values
        self.df.insert(0, 'author', author)
        m, n = util_matrix_vals_np.shape
        jaccard_user_similarity = np.zeros((m, m))
        np.diag(jaccard_user_similarity, 1.)
        # Creating Jaccard Similarity Matrix


        for i in xrange(m):
            for j in xrange(m):
                if i != j:
                    jaccard_user_similarity[i][j] = (
                        pdist(util_matrix_vals_np[[i, j], :], 'jaccard'))

        return 1 - jaccard_user_similarity

    def rec_builder(self):
        '''Change 20 to top number of similar users to compare to

        Args:
            user_name: (str) user to name recommendation on

        Returns:
            top_users_ranked: (DataFrame) Most similar users for all users
        
        '''
        # FOR ALL USERS
        most_similar_user_indices = np.argsort(
            -self.jaccard_user_similarity, axis=1)[:, :20]
        u, v = most_similar_user_indices.shape

        for i in xrange(u):
            self.user_similarity_dict[self.author[i]] = self.author[
                most_similar_user_indices[i]].values.tolist()

        top_users_ranked = pd.DataFrame.from_dict(self.user_similarity_dict).T
        return top_users_ranked

    def get_recommendations(self, user_list):
        ''' Retreive recommendations for each user in user_list
            
            Args:
                user_list: (list) a list of users to make recomendations on
                
            Returns:
                total_recss: (dictionary) Dict of the user with its subreddit recomendations

        '''
        total_recss = {}

        for user in user_list:

            top_users_ranked_for_client = self.top_users_ranked.loc[
                user].tolist()
            top_users_ranked_for_client.insert(0, user)

            recomendations = self.df_utility_matrix.set_index('author', inplace=False).loc[
                top_users_ranked_for_client, :]
            recomendations = recomendations - recomendations.iloc[0, ]
            sub_recommendations = {
                k: v for k, v in recomendations.sum(axis=0).iteritems() if v > 4}
            ranked_recommendations = map(lambda x: x[0], sorted(
                sub_recommendations.iteritems(), key=operator.itemgetter(1), reverse=True))
            total_recss[user] = ranked_recommendations

        return total_recss
