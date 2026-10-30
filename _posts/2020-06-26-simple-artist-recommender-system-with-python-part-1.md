---
layout: post
title: "Simple Artist Recommender System with Python — Part 1"
date: 2020-06-26T16:17:35+00:00
original_url: "https://medium.com/@yamaceay/simple-artist-recommender-system-with-python-part-1-a9b163e50c61"
tags: []
excerpt: "Source: Microsoft Store “And mostly all I have to say about these songs is that I love them, and want to sing along to them, and force other people to listen to them, and get cross when these other pe"
---

<figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*tI3D9IM3YbGB2c59UqDw2w.jpeg" /><figcaption>Source: Microsoft Store</figcaption></figure><blockquote>“And mostly all I have to say about these songs is that I love them, and want to sing along to them, and force other people to listen to them, and get cross when these other people don&#x27;t like them as much as I do. ”<br/>-Nick Hornby</blockquote><p>We all have experienced this situation necessarily: A friend who listens to the same kind of music suggests a song and we don’t like it at all, or someday you cool down from your favorite genre and start listening to music that has nothing to do with your taste. If you are through the same situation as I am, this is completely normal, because you have a unique musical taste that no one else could have.</p><p>Spotify is -in my opinion- the most successful music library app in the world, not only because of its brilliant-design and rich content but also the personalization: You can find a wide variety of songs that are similar to your musical taste in seconds thanks to its powerful recommendation engine. Not a few of us spends time using Spotify for many hours: not surprising at all!</p><p>The more accurate recommender systems are, the more users will be satisfied. Spotify uses a hybrid recommendation engine consisting of three different approaches (A good explanation can be found in this article below)</p><p><a href="https://towardsdatascience.com/how-spotify-recommends-your-new-favorite-artist-8c1850512af0">How Spotify Recommends Your New Favorite Artist</a></p><p>However, I will show you how to make an artist recommendation based on only the genres of the artists, which only requires a little bit of linear algebra. The <a href="https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks">dataset</a> we will use is my Kaggle dataset that contains audio features of nearly 170k tracks from Spotify, and we will be using <a href="https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks?select=data_w_genres.csv">data_w_genres.csv</a> file from this dataset, which contains nearly 28k artists and their genres.</p><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*QzWFpc_cShwbhq64I1alnQ.jpeg" /><figcaption>Screenshot of my Spotify Dataset</figcaption></figure><h4>Table of Content</h4><ol><li>Algorithm</li><li>Code</li><li>Review</li></ol><h4>1. Algorithm</h4><p>Our main goal is to examine the artists that Steve likes in terms of genre and to introduce brand new artists who make music of a similar genre. The overview of the algorithm:</p><p><em>0. Take ratings of artists and genres of all artists as input</em></p><ol><li><em>Find out the genre profile of user:<br/>1.1. Create artist-genre-matrix of given artists<br/>1.2. Calculate the dot product of artists’ ratings and artist-genre-matrix</em></li><li><em>Find out new artists:<br/>2.1. Discover artists with any common genre as the genre profile of user<br/>2.2. Create artist-genre-matrix of those artists<br/>2.3. Select only the genres that are included in the genre profile</em></li><li><em>Calculate similarity scores of each artist:<br/>3.1. Calculate the maximum score that an artist could ever have (the sum of all values in the genre profile)<br/>3.2. Calculate the score of each artist (calculate the dot product of genre profile and the artist-genre-matrix of new artists)</em><br/>3<em>.3. Calculate the similarity score of each artist by dividing the artist score by the maximum score</em></li><li><em>Sort similarity scores of given artists in descending order and select k-many results</em></li></ol><p>The dataframe is displayed below:</p><pre><code>import pandas as pd</code></pre><pre><code>df_by_artists = pd.read_csv(&quot;/kaggle/working/data_w_genres.csv&quot;)</code></pre><pre><code>#only &quot;artists&quot; and &quot;genres&quot; columns of the top 5 rows are shown
df_by_artists.head(5)[[&quot;artists&quot;, &quot;genres&quot;]]</code></pre><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*xjkK6XPP7Pn9jB9n23ZdOg.jpeg" /></figure><p>Let’s assume Steve is a huge alternative metal &amp; post-grunge fan, and he is expected to rate his most favourite artists within range from 0 to 10 based on its “favouriteness”.</p><pre><code>name_rate_dict = {&quot;Linkin Park&quot;: 10, &quot;Red Hot Chili Peppers&quot;: 9, &quot;Three Days Grace&quot;: 7, &quot;Arctic Monkeys&quot;: 4, &quot;Papa Roach&quot;: 6, &quot;Green Day&quot;: 8, &quot;Foo Fighters&quot;: 1, &quot;Billy Talent&quot;: 2, &quot;Nirvana&quot;: 5, &quot;The Offspring&quot;: 3}</code></pre><p>Given that these artists are included in the dataset, we can find the genres of artists and store this information in a new dataframe:</p><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*fIjOqg0b51zJuAU8v3F4rg.jpeg" /></figure><p>Artist-genre matrix: The matrix, which one-hot-encodes all genres whether an artist has the genre (1) or not (0). <br/>The result of the dot product of artists’ ratings and artist-genre-matrix is the genre profile of given user.</p><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*CJaDEEo0Q6hlfzzSkntVcA.jpeg" /></figure><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*kYsIVoE2HJBpI2nHs1Euwg.png" /></figure><p>I leave this notation here for those who do not know the dot product:</p><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*u0Gem0TnYKlSyQaloDh_QA.jpeg" /><figcaption>Matrix — Vector Dot Product</figcaption></figure><p>At the end of the calculation, Steve’s genre profile looks like this:</p><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*CWM_PKWEpJs8mt85PRQXJg.png" /><figcaption>Steve’s most favourite genres in descending order</figcaption></figure><p>Well done Steve, you are indeed a post-grunge fan!</p><p>Finally we have Steve&#x27;s genre profile. Now it’s time to explore new artists that contain any of these genres, and we should create an artist-genre-matrix for those too:</p><pre><code>#Only the top 5 rows are shown
matrix_new_artists.head()</code></pre><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*8HFXjqsnWF9YL0L561kBig.jpeg" /><figcaption>Screenshot from the original DataFrame</figcaption></figure><p>We have both the genre profile of user and the matrix of new artists. In the next step, we will find out:</p><ul><li>the maximum score that an artist could ever have (“maxScore”)</li><li>the score of each artist (“scores”)</li><li>and finally the similarity scores of artists (“scores” divided by “maxScore”)</li></ul><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*oN4QcgzVUw6fWe6FGIQD_w.jpeg" /><figcaption>Similarity score calculation</figcaption></figure><p>For the sake of simplicity, I pick the top 5 similar artists.</p><p>The maximum score is equal to 257, which is the sum of all values in the genre profile.</p><pre><code>weighted_scores_sorted = weighted_scores.sort_values(ascending = False)
weighted_scores_sorted.head()</code></pre><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*3iTcBvig-MymaFsOynz6VA.jpeg" /><figcaption>Weighted scores of top similar artists</figcaption></figure><pre><code>similarity_scores = weighted_scores_sorted/257
similarity_scores.head()</code></pre><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*qgM0Vwe2OMeSHBFiInpRgg.jpeg" /><figcaption>Similarity scores of given artists</figcaption></figure><p>And voila! In the last step, you can format results in a more human-understandable way, so that Steve understands too. For example:</p><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*H46RDNPLF9qBRvO4kUnZfg.png" /></figure><h4>2. Code</h4><p>You can visit my Kaggle<a href="https://www.kaggle.com/yamaerenay/submission-artist-recommendation-task"> notebook</a> or GitHub <a href="https://github.com/yamaceay/spotify_2/blob/master/part_1/part_1.ipynb">code</a>.</p><pre><code>{
 &quot;cells&quot;: [
  {
   &quot;cell_type&quot;: &quot;markdown&quot;,
   &quot;metadata&quot;: {},
   &quot;source&quot;: [
    &quot;# STEP 1: SETUP&quot;
   ]
  },
  {
   &quot;cell_type&quot;: &quot;code&quot;,
   &quot;execution_count&quot;: 1,
   &quot;metadata&quot;: {
    &quot;_kg_hide-input&quot;: true,
    &quot;_kg_hide-output&quot;: true
   },
   &quot;outputs&quot;: [],
   &quot;source&quot;: [
    &quot;import numpy as np \n&quot;,
    &quot;import pandas as pd \n&quot;,
    &quot;import re\n&quot;,
    &quot;import ast\n&quot;,
    &quot;from matplotlib import pyplot as plt&quot;
   ]
  },
  {
   &quot;cell_type&quot;: &quot;markdown&quot;,
   &quot;metadata&quot;: {},
   &quot;source&quot;: [
    &quot;# STEP 2: CREATE FUNCTIONS&quot;
   ]
  },
  {
   &quot;cell_type&quot;: &quot;code&quot;,
   &quot;execution_count&quot;: 2,
   &quot;metadata&quot;: {
    &quot;_cell_guid&quot;: &quot;b1076dfc-b9ad-4769-8c92-a6c4dae69d19&quot;,
    &quot;_kg_hide-input&quot;: true,
    &quot;_uuid&quot;: &quot;8f2839f25d086af736a60e9eeb907d3b93b6e0e5&quot;
   },
   &quot;outputs&quot;: [],
   &quot;source&quot;: [
    &quot;def col(df, colname = \&quot;artists\&quot;):\n&quot;,
    &quot;    return np.array([int(x == colname) for x in df.columns]).argmax()\n&quot;,
    &quot;def query_artists(df, lists = [], full = False, strict = True):\n&quot;,
    &quot;    return pd.concat([query_artist(df, string = name, strict = strict) for name in lists], axis = 0)\n&quot;,
    &quot;def query_artist(df, string = \&quot;--\&quot;, full = False, strict = True):\n&quot;,
    &quot;    lists = []\n&quot;,
    &quot;    for i, artist in enumerate(df[\&quot;artists\&quot;]):\n&quot;,
    &quot;        if(len(re.findall(string, \&quot;\&quot;.join(artist))) != 0):\n&quot;,
    &quot;            if(strict):\n&quot;,
    &quot;                if(string == artist):\n&quot;,
    &quot;                    if(full):\n&quot;,
    &quot;                        lists.append(df.iloc[i])\n&quot;,
    &quot;                    else:\n&quot;,
    &quot;                        lists.append(df.iloc[i, [col(df, \&quot;artists\&quot;), col(df, \&quot;genres\&quot;)]])\n&quot;,
    &quot;            else:\n&quot;,
    &quot;                if(full):\n&quot;,
    &quot;                    lists.append(df.iloc[i])\n&quot;,
    &quot;                else:\n&quot;,
    &quot;                    lists.append(df.iloc[i, [col(df, \&quot;artists\&quot;), col(df, \&quot;genres\&quot;)]])\n&quot;,
    &quot;    if(full): \n&quot;,
    &quot;        return pd.DataFrame(lists, columns = df.columns)\n&quot;,
    &quot;    else:\n&quot;,
    &quot;        return pd.DataFrame(lists, columns = [\&quot;artists\&quot;, \&quot;genres\&quot;])\n&quot;,
    &quot;def perfect_eval(string):\n&quot;,
    &quot;    try:\n&quot;,
    &quot;        return ast.literal_eval(string)\n&quot;,
    &quot;    except:\n&quot;,
    &quot;        return []\n&quot;,
    &quot;def create_random_dict(df_by_artists, length, score):\n&quot;,
    &quot;    list_of_names = list(set(df_by_artists[\&quot;artists\&quot;]))\n&quot;,
    &quot;    random_indices = [round(x) for x in np.random.random(length)*len(list_of_names)]\n&quot;,
    &quot;    random_names = pd.Series(list_of_names).iloc[random_indices].values.tolist()\n&quot;,
    &quot;    random_rates = [int(round(x)) for x in (score[0] + np.random.random(length)*(score[1]-score[0]))]\n&quot;,
    &quot;    name_rate_dict = {}\n&quot;,
    &quot;    for index in range(length):\n&quot;,
    &quot;        name_rate_dict.update({random_names[index]: random_rates[index]})\n&quot;,
    &quot;    return name_rate_dict\n&quot;,
    &quot;def rate_artist(df_by_artists, name_rate_dict):\n&quot;,
    &quot;    #convert the name_rate_series to a pandas dataframe\n&quot;,
    &quot;    name_rate_series = pd.DataFrame({\&quot;rate\&quot;: name_rate_dict.values, \&quot;artists\&quot;: name_rate_dict.index})\n&quot;,
    &quot;    #create a new dataframe, only selecting the artists and genres columns of artists selected by user\n&quot;,
    &quot;    artists_genres = df_by_artists[df_by_artists[\&quot;artists\&quot;].isin(list(name_rate_dict.keys()))][[\&quot;artists\&quot;, \&quot;genres\&quot;]]\n&quot;,
    &quot;    #merge both of these\n&quot;,
    &quot;    df_name_rate = pd.merge(name_rate_series, artists_genres, on = \&quot;artists\&quot;, how = \&quot;inner\&quot;)\n&quot;,
    &quot;    df_x = df_name_rate.copy()\n&quot;,
    &quot;    #create the artist-genre-matrix for artists selected by users\n&quot;,
    &quot;    for index, genres in enumerate(df_name_rate[\&quot;genres\&quot;]):\n&quot;,
    &quot;        for genre in genres:\n&quot;,
    &quot;            #artist includes the genre: 1\n&quot;,
    &quot;            df_x.at[index, genre] = 1\n&quot;,
    &quot;    #artist does not include the genre: 0\n&quot;,
    &quot;    df_x = df_x.fillna(0)\n&quot;,
    &quot;    #ratings of artists\n&quot;,
    &quot;    df_user = df_x[\&quot;rate\&quot;]\n&quot;,
    &quot;    #drop all columns except the genre columns\n&quot;,
    &quot;    df_genre_matrix = df_x.drop([\&quot;artists\&quot;, \&quot;genres\&quot;, \&quot;rate\&quot;], axis = 1).reset_index(drop = True)\n&quot;,
    &quot;    #find out the genres&#x27; ratings\n&quot;,
    &quot;    df_profile = df_genre_matrix.transpose().dot(df_user)\n&quot;,
    &quot;    return df_profile\n&quot;,
    &quot;def select_artist(df_by_artists, df_rate):\n&quot;,
    &quot;    # save the indices of artists, which include any of the genres in the genre profile\n&quot;,
    &quot;    list_of_id = []\n&quot;,
    &quot;    for index, row in df_by_artists.iterrows():\n&quot;,
    &quot;        for genre in row[\&quot;genres\&quot;]:\n&quot;,
    &quot;            if(genre in df_rate.index):\n&quot;,
    &quot;                list_of_id.append(index)\n&quot;,
    &quot;    #find the unique indices\n&quot;,
    &quot;    list_of_id = list(set(list_of_id))\n&quot;,
    &quot;    #select the artists and genres columns of the artists including any of the genres in the genre profile\n&quot;,
    &quot;    df_select_columns = df_by_artists.iloc[list_of_id, [col(df_by_artists, \&quot;artists\&quot;), col(df_by_artists, \&quot;genres\&quot;)]]\n&quot;,
    &quot;    df_select = df_select_columns.copy()\n&quot;,
    &quot;    #create the artist-genre-matrix of new artists\n&quot;,
    &quot;    for index, row in df_select_columns.iterrows():\n&quot;,
    &quot;        for genre in row[&#x27;genres&#x27;]:\n&quot;,
    &quot;            #artist includes genre: 1\n&quot;,
    &quot;            df_select.at[index, genre] = 1\n&quot;,
    &quot;    #artist does not include genre: 0\n&quot;,
    &quot;    df_select = df_select.fillna(0)[df_rate.index]\n&quot;,
    &quot;    return df_select\n&quot;,
    &quot;def recommend_artist_by_genre(df_by_artists, name_rate_dict, how_many):\n&quot;,
    &quot;    df_by_artists = df_by_artists.copy()\n&quot;,
    &quot;    #make sure that genres are list, not string\n&quot;,
    &quot;    df_by_artists[\&quot;genres\&quot;] = [perfect_eval(genre) for genre in df_by_artists[\&quot;genres\&quot;]]\n&quot;,
    &quot;    #create a name_rate pandas series\n&quot;,
    &quot;    name_rate_series = pd.Series(name_rate_dict)\n&quot;,
    &quot;    #find out the genre profile of user\n&quot;,
    &quot;    df_rate = rate_artist(df_by_artists, name_rate_series)\n&quot;,
    &quot;    #create new artists&#x27; matrix\n&quot;,
    &quot;    df_select = select_artist(df_by_artists, df_rate)\n&quot;,
    &quot;    #calculate similarity scores of those artists\n&quot;,
    &quot;    affinity_scores = df_select.dot(df_rate)/df_rate.sum()\n&quot;,
    &quot;    #sort it in descending order\n&quot;,
    &quot;    affinity_scores_sorted = pd.Series(affinity_scores, name = \&quot;genre_affinity\&quot;).sort_values(ascending = False)\n&quot;,
    &quot;    #retrieve the names of artists by their indices\n&quot;,
    &quot;    artists_in_df = df_by_artists.iloc[affinity_scores_sorted.index, [col(df_by_artists, \&quot;artists\&quot;)]]\n&quot;,
    &quot;    #store the artists&#x27; names and their similarity scores in a dataframe\n&quot;,
    &quot;    resulted_df = pd.concat([affinity_scores_sorted, artists_in_df], axis = 1)\n&quot;,
    &quot;    #drop the artists already selected by user and limit the count of artists to a specified amount\n&quot;,
    &quot;    output = resulted_df[~resulted_df[\&quot;artists\&quot;].isin(name_rate_series.index)].iloc[:how_many, :]\n&quot;,
    &quot;    #create new indices\n&quot;,
    &quot;    return output.reset_index()\n&quot;,
    &quot;def pretty_recommend_artist(df_by_artists, name_rate_dict, how_many):\n&quot;,
    &quot;    df_scores = recommend_artist_by_genre(df_by_artists, name_rate_dict, how_many)\n&quot;,
    &quot;    print(\&quot;\\n\\n--- GENRE AFFINITY ---\\n\\n\&quot;)\n&quot;,
    &quot;    for index, row in df_scores.iterrows():\n&quot;,
    &quot;        print(\&quot;Number \&quot;,str(index),\&quot;: \&quot;,row[\&quot;artists\&quot;],\&quot; matching \&quot;,str(round(row[\&quot;genre_affinity\&quot;] * 100, 2)),\&quot;%\&quot;)\n&quot;,
    &quot;    print(\&quot;\\n\\n\&quot;)\n&quot;,
    &quot;    plt.figure(figsize = (10, 10))\n&quot;,
    &quot;    plt.bar(list(df_scores[\&quot;artists\&quot;]), list(df_scores[\&quot;genre_affinity\&quot;]), color = [\&quot;green\&quot; for x in range(how_many)])\n&quot;,
    &quot;    plt.xticks(rotation = 90)\n&quot;,
    &quot;    plt.xlabel(\&quot;Artists\&quot;)\n&quot;,
    &quot;    plt.ylabel(\&quot;Score\&quot;)\n&quot;,
    &quot;    plt.title(\&quot;Top \&quot;+str(how_many)+\&quot; Favourite Artists\&quot;)&quot;
   ]
  },
  {
   &quot;cell_type&quot;: &quot;markdown&quot;,
   &quot;metadata&quot;: {},
   &quot;source&quot;: [
    &quot;# STEP 3: GENERATE INPUT&quot;
   ]
  },
  {
   &quot;cell_type&quot;: &quot;code&quot;,
   &quot;execution_count&quot;: 3,
   &quot;metadata&quot;: {
    &quot;_cell_guid&quot;: &quot;79c7e3d0-c299-4dcb-8224-4455121ee9b0&quot;,
    &quot;_uuid&quot;: &quot;d629ff2d2480ee46fbb7e2d37f6b5fab8052498a&quot;
   },
   &quot;outputs&quot;: [],
   &quot;source&quot;: [
    &quot;df_by_artists = pd.read_csv(\&quot;data_w_genres.csv\&quot;)\n&quot;,
    &quot;#name_rate_dict = create_random_dict(df_by_artists, 10, [0, 10])\n&quot;,
    &quot;name_rate_dict_1 = {\&quot;Linkin Park\&quot;: 10, \&quot;Red Hot Chili Peppers\&quot;: 9, \&quot;Three Days Grace\&quot;: 7, \&quot;Arctic Monkeys\&quot;: 4, \&quot;Papa Roach\&quot;: 6, \&quot;Green Day\&quot;: 8,\n&quot;,
    &quot;                  \&quot;Foo Fighters\&quot;: 1, \&quot;Billy Talent\&quot;: 2, \&quot;Nirvana\&quot;: 5, \&quot;The Offspring\&quot;: 3}\n&quot;,
    &quot;#name_rate_dict_2 = {\&quot;Wiz Khalifa\&quot;: 10, \&quot;Eminem\&quot;: 9, \&quot;Logic\&quot;: 7, \&quot;Kendrick Lamar\&quot;: 4, \&quot;JAY-Z\&quot;: 6, \&quot;Kanye West\&quot;: 8,\n&quot;,
    &quot;#                  \&quot;XXXTentacion\&quot;: 8, \&quot;Travis Scott\&quot;: 8, \&quot;Joyner Lucas\&quot;: 5, \&quot;Snoop Dogg\&quot;: 3}\n&quot;,
    &quot;#name_rate_dict_3 = {\&quot;Rihanna\&quot;: 10, \&quot;Beyonce\&quot;: 9, \&quot;Britney Spears\&quot;: 7, \&quot;Adele\&quot;: 4, \&quot;Camila Cabello\&quot;: 6, \&quot;Ciara\&quot;: 8,\n&quot;,
    &quot;#                  \&quot;Nicki Minaj\&quot;: 8, \&quot;Iggy Azalea\&quot;: 8, \&quot;Ariana Grande\&quot;: 5, \&quot;Clean Bandit\&quot;: 3}\n&quot;,
    &quot;how_many = 15&quot;
   ]
  },
  {
   &quot;cell_type&quot;: &quot;markdown&quot;,
   &quot;metadata&quot;: {},
   &quot;source&quot;: [
    &quot;# STEP 4: CHECK ARTISTS&quot;
   ]
  },
  {
   &quot;cell_type&quot;: &quot;code&quot;,
   &quot;execution_count&quot;: 4,
   &quot;metadata&quot;: {},
   &quot;outputs&quot;: [
    {
     &quot;data&quot;: {
      &quot;text/html&quot;: [
       &quot;&lt;div&gt;\n&quot;,
       &quot;&lt;style scoped&gt;\n&quot;,
       &quot;    .dataframe tbody tr th:only-of-type {\n&quot;,
       &quot;        vertical-align: middle;\n&quot;,
       &quot;    }\n&quot;,
       &quot;\n&quot;,
       &quot;    .dataframe tbody tr th {\n&quot;,
       &quot;        vertical-align: top;\n&quot;,
       &quot;    }\n&quot;,
       &quot;\n&quot;,
       &quot;    .dataframe thead th {\n&quot;,
       &quot;        text-align: right;\n&quot;,
       &quot;    }\n&quot;,
       &quot;&lt;/style&gt;\n&quot;,
       &quot;&lt;table border=\&quot;1\&quot; class=\&quot;dataframe\&quot;&gt;\n&quot;,
       &quot;  &lt;thead&gt;\n&quot;,
       &quot;    &lt;tr style=\&quot;text-align: right;\&quot;&gt;\n&quot;,
       &quot;      &lt;th&gt;&lt;/th&gt;\n&quot;,
       &quot;      &lt;th&gt;artists&lt;/th&gt;\n&quot;,
       &quot;      &lt;th&gt;genres&lt;/th&gt;\n&quot;,
       &quot;    &lt;/tr&gt;\n&quot;,
       &quot;  &lt;/thead&gt;\n&quot;,
       &quot;  &lt;tbody&gt;\n&quot;,
       &quot;    &lt;tr&gt;\n&quot;,
       &quot;      &lt;th&gt;14202&lt;/th&gt;\n&quot;,
       &quot;      &lt;td&gt;Linkin Park&lt;/td&gt;\n&quot;,
       &quot;      &lt;td&gt;[&#x27;alternative metal&#x27;, &#x27;nu metal&#x27;, &#x27;post-grunge...&lt;/td&gt;\n&quot;,
       &quot;    &lt;/tr&gt;\n&quot;,
       &quot;    &lt;tr&gt;\n&quot;,
       &quot;      &lt;th&gt;19854&lt;/th&gt;\n&quot;,
       &quot;      &lt;td&gt;Red Hot Chili Peppers&lt;/td&gt;\n&quot;,
       &quot;      &lt;td&gt;[&#x27;alternative rock&#x27;, &#x27;funk metal&#x27;, &#x27;funk rock&#x27;...&lt;/td&gt;\n&quot;,
       &quot;    &lt;/tr&gt;\n&quot;,
       &quot;    &lt;tr&gt;\n&quot;,
       &quot;      &lt;th&gt;24971&lt;/th&gt;\n&quot;,
       &quot;      &lt;td&gt;Three Days Grace&lt;/td&gt;\n&quot;,
       &quot;      &lt;td&gt;[&#x27;alternative metal&#x27;, &#x27;canadian metal&#x27;, &#x27;canad...&lt;/td&gt;\n&quot;,
       &quot;    &lt;/tr&gt;\n&quot;,
       &quot;    &lt;tr&gt;\n&quot;,
       &quot;      &lt;th&gt;1492&lt;/th&gt;\n&quot;,
       &quot;      &lt;td&gt;Arctic Monkeys&lt;/td&gt;\n&quot;,
       &quot;      &lt;td&gt;[&#x27;garage rock&#x27;, &#x27;modern rock&#x27;, &#x27;permanent wave...&lt;/td&gt;\n&quot;,
       &quot;    &lt;/tr&gt;\n&quot;,
       &quot;    &lt;tr&gt;\n&quot;,
       &quot;      &lt;th&gt;18398&lt;/th&gt;\n&quot;,
       &quot;      &lt;td&gt;Papa Roach&lt;/td&gt;\n&quot;,
       &quot;      &lt;td&gt;[&#x27;alternative metal&#x27;, &#x27;nu metal&#x27;, &#x27;post-grunge...&lt;/td&gt;\n&quot;,
       &quot;    &lt;/tr&gt;\n&quot;,
       &quot;    &lt;tr&gt;\n&quot;,
       &quot;      &lt;th&gt;9210&lt;/th&gt;\n&quot;,
       &quot;      &lt;td&gt;Green Day&lt;/td&gt;\n&quot;,
       &quot;      &lt;td&gt;[&#x27;permanent wave&#x27;, &#x27;punk&#x27;]&lt;/td&gt;\n&quot;,
       &quot;    &lt;/tr&gt;\n&quot;,
       &quot;    &lt;tr&gt;\n&quot;,
       &quot;      &lt;th&gt;7955&lt;/th&gt;\n&quot;,
       &quot;      &lt;td&gt;Foo Fighters&lt;/td&gt;\n&quot;,
       &quot;      &lt;td&gt;[&#x27;alternative metal&#x27;, &#x27;alternative rock&#x27;, &#x27;mod...&lt;/td&gt;\n&quot;,
       &quot;    &lt;/tr&gt;\n&quot;,
       &quot;    &lt;tr&gt;\n&quot;,
       &quot;      &lt;th&gt;2686&lt;/th&gt;\n&quot;,
       &quot;      &lt;td&gt;Billy Talent&lt;/td&gt;\n&quot;,
       &quot;      &lt;td&gt;[&#x27;alternative metal&#x27;, &#x27;canadian punk&#x27;, &#x27;nu met...&lt;/td&gt;\n&quot;,
       &quot;    &lt;/tr&gt;\n&quot;,
       &quot;    &lt;tr&gt;\n&quot;,
       &quot;      &lt;th&gt;17616&lt;/th&gt;\n&quot;,
       &quot;      &lt;td&gt;Nirvana&lt;/td&gt;\n&quot;,
       &quot;      &lt;td&gt;[&#x27;alternative rock&#x27;, &#x27;grunge&#x27;, &#x27;permanent wave...&lt;/td&gt;\n&quot;,
       &quot;    &lt;/tr&gt;\n&quot;,
       &quot;    &lt;tr&gt;\n&quot;,
       &quot;      &lt;th&gt;24366&lt;/th&gt;\n&quot;,
       &quot;      &lt;td&gt;The Offspring&lt;/td&gt;\n&quot;,
       &quot;      &lt;td&gt;[&#x27;alternative metal&#x27;, &#x27;permanent wave&#x27;, &#x27;post-...&lt;/td&gt;\n&quot;,
       &quot;    &lt;/tr&gt;\n&quot;,
       &quot;  &lt;/tbody&gt;\n&quot;,
       &quot;&lt;/table&gt;\n&quot;,
       &quot;&lt;/div&gt;&quot;
      ],
      &quot;text/plain&quot;: [
       &quot;                     artists  \\\n&quot;,
       &quot;14202            Linkin Park   \n&quot;,
       &quot;19854  Red Hot Chili Peppers   \n&quot;,
       &quot;24971       Three Days Grace   \n&quot;,
       &quot;1492          Arctic Monkeys   \n&quot;,
       &quot;18398             Papa Roach   \n&quot;,
       &quot;9210               Green Day   \n&quot;,
       &quot;7955            Foo Fighters   \n&quot;,
       &quot;2686            Billy Talent   \n&quot;,
       &quot;17616                Nirvana   \n&quot;,
       &quot;24366          The Offspring   \n&quot;,
       &quot;\n&quot;,
       &quot;                                                  genres  \n&quot;,
       &quot;14202  [&#x27;alternative metal&#x27;, &#x27;nu metal&#x27;, &#x27;post-grunge...  \n&quot;,
       &quot;19854  [&#x27;alternative rock&#x27;, &#x27;funk metal&#x27;, &#x27;funk rock&#x27;...  \n&quot;,
       &quot;24971  [&#x27;alternative metal&#x27;, &#x27;canadian metal&#x27;, &#x27;canad...  \n&quot;,
       &quot;1492   [&#x27;garage rock&#x27;, &#x27;modern rock&#x27;, &#x27;permanent wave...  \n&quot;,
       &quot;18398  [&#x27;alternative metal&#x27;, &#x27;nu metal&#x27;, &#x27;post-grunge...  \n&quot;,
       &quot;9210                          [&#x27;permanent wave&#x27;, &#x27;punk&#x27;]  \n&quot;,
       &quot;7955   [&#x27;alternative metal&#x27;, &#x27;alternative rock&#x27;, &#x27;mod...  \n&quot;,
       &quot;2686   [&#x27;alternative metal&#x27;, &#x27;canadian punk&#x27;, &#x27;nu met...  \n&quot;,
       &quot;17616  [&#x27;alternative rock&#x27;, &#x27;grunge&#x27;, &#x27;permanent wave...  \n&quot;,
       &quot;24366  [&#x27;alternative metal&#x27;, &#x27;permanent wave&#x27;, &#x27;post-...  &quot;
      ]
     },
     &quot;execution_count&quot;: 4,
     &quot;metadata&quot;: {},
     &quot;output_type&quot;: &quot;execute_result&quot;
    }
   ],
   &quot;source&quot;: [
    &quot;query_artists(df_by_artists, list(name_rate_dict_1.keys()))&quot;
   ]
  },
  {
   &quot;cell_type&quot;: &quot;markdown&quot;,
   &quot;metadata&quot;: {},
   &quot;source&quot;: [
    &quot;# STEP 5: RUN RECOMMENDATION ENGINE&quot;
   ]
  },
  {
   &quot;cell_type&quot;: &quot;code&quot;,
   &quot;execution_count&quot;: 5,
   &quot;metadata&quot;: {
    &quot;tags&quot;: []
   },
   &quot;outputs&quot;: [
    {
     &quot;name&quot;: &quot;stdout&quot;,
     &quot;output_type&quot;: &quot;stream&quot;,
     &quot;text&quot;: [
      &quot;\n&quot;,
      &quot;\n&quot;,
      &quot;--- GENRE AFFINITY ---\n&quot;,
      &quot;\n&quot;,
      &quot;\n&quot;,
      &quot;Number  0 :  Jane&#x27;s Addiction  matching  74.71 %\n&quot;,
      &quot;Number  1 :  Audioslave  matching  65.76 %\n&quot;,
      &quot;Number  2 :  Faith No More  matching  65.37 %\n&quot;,
      &quot;Number  3 :  Rage Against The Machine  matching  64.2 %\n&quot;,
      &quot;Number  4 :  Rage  matching  64.2 %\n&quot;,
      &quot;Number  5 :  Deftones  matching  62.65 %\n&quot;,
      &quot;Number  6 :  311  matching  61.48 %\n&quot;,
      &quot;Number  7 :  Incubus  matching  61.09 %\n&quot;,
      &quot;Number  8 :  White Zombie  matching  60.7 %\n&quot;,
      &quot;Number  9 :  Primus  matching  59.14 %\n&quot;,
      &quot;Number  10 :  The Smashing Pumpkins  matching  57.98 %\n&quot;,
      &quot;Number  11 :  Filter  matching  56.42 %\n&quot;,
      &quot;Number  12 :  Chevelle  matching  56.42 %\n&quot;,
      &quot;Number  13 :  Perfect  matching  56.42 %\n&quot;,
      &quot;Number  14 :  Helmet  matching  56.42 %\n&quot;,
      &quot;\n&quot;,
      &quot;\n&quot;,
      &quot;\n&quot;
     ]
    },
    {
     &quot;data&quot;: {
      &quot;image/png&quot;: &quot;iVBORw0KGgoAAAANSUhEUgAAAmEAAALXCAYAAADFZpcjAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4yLjAsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy8GearUAAAgAElEQVR4nOzdeZhkZXn+8e/NIAIuoGHcWAQVRTSCCqjRuCTBgBsaFxbXqCFERfOLGsENNRpjXOKGIUSJxg1QEwVFcQcRNAwEWcUQUBmROCiCIgoDz++Pc4qpKXoWpqfOWzPz/VxXX9N16nSdZ7qrq+9611QVkiRJGtZGrQuQJEnaEBnCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCStoSSvTvLB1nWMS7Jdkl8nWdC6FkkrZwiTNiD9H+fRx41Jrh27/cy1dI1nJDk1yW+SfHOO+yvJNWPXXWGISfLhJNdN1L3v2qhzbaiqv6+qFwIk2b7/v208n8dMcpv+/3nCap7/wyR/MlbTj6vqtlV1wyq+7nlJTplPrZLmZ14vFpLWLVV129HnSX4IvLCqvrqWL/ML4N3ATsAfreCcXarqotV8vH+sqteulcrWoiQbV9XSKTz004DfAY9Ncteq+unA15c0EFvCJJHk1kneneSy/uPdSW7d3/foJIv7rrcr+paXFbaaVdVXq+pY4LIp1vueJJcmuTrJGUn+sD9+t751745j5z6wr/tWSTZK8tokP0rysyT/nmSL8f/nxHVuamVK8oYkn07ysSRXA8/rj32sP/3k/t9f9i1ZD+u/7vlJLkhyZZITk9x9Ff+95wJHAGcDy32f+3peleRs4JoknwS2A47vr/m3ky1yfYvXxUl+leSSJM9Mct/+Gg/rv+6X/bmPS3J+f+5PkrzilvxcJN0yhjBJAK8BHgrsCuwC7AGMtz7dBdgK2JouJByZ5D7zuN7JSS5P8h9Jtl+Drz+9r/WOwCeATyXZtKouA04Dnjp27gHAp6vqeuB5/cdjgHsAtwXefwuuuw/waWBL4OMT9z2y/3fLvjvwtCRPBl4N/BmwEPgW8MkVPXiS7YBH94/9ceA5c5y2P/D4/jr7Az8Gnthf8x8nHu82wHuBvavqdsAfAGdV1QXAQcBp/ddt2X/Jh4C/7M+9P/D1VX1DJK05Q5gk6Fpc3lRVP6uqJcAbgWdPnPO6qvpdVZ0EfAF4xhpe61HA9nTdlZcBn1/FOKpXJPll/3EFQFV9rKp+XlVLq+qdwK2BUSj8BF1QIUmA/fpjo//nu6rq4qr6NXAosN8tGMd1WlV9tqpurKprV+P8vwTeWlUX9F2Hfw/supLWsOcAZ1fV+XRh7X5JHjhxznur6tLVvD7AjcD9k2xWVT+tqvNWcu71wM5Jbl9VV1bVmat5DUlrwBAmCeBuwI/Gbv+oPzZyZVVds5L7V1tVnVxV11XVL4GXATsA913Jl7yjqrbsP7YCSPLyvovvqr4rbQu6ljroWqoeluRudK1TRdcCtaL/58bAnVez/EtX87yRuwPvGYVIuvFyoWtRnMtz6FvY+la9k+haHteohv5nti9dq9dPk3whyU4r+ZKnAo8DfpTkpFGXqqTpMIRJgq5Farx1ZjuWH9N1h75ra0X3z0fRBZPV0o//ehVdS9wd+q60q0aP0Ye7L/f3HwB8sqqq//K5/p9Lgf8DrgE2H7vOArouxMlaV/b/mHQpXffelmMfm1XVqXP8v/4A2BE4tO+qvRx4CLD/REvd5HVWVhNVdWJV7QncFfg+8K8r+rqqOr2q9gHuBHwWOHZljy1pfgxhkqDr+nptkoVJtgJeD3xs4pw3JtmkD0FPAD411wMlWZBkU7oWpo2SbJrkVv1990uya3/ObYF3Aj8BLrgFtd6OLjgtATZO8nrg9hPnfIKuVempLOuKHP0//1+SHfrr/z1wTN9V+ANg0ySP7+t9LV035+paQtf1d4+xY0fQhar7ASTZIsnTV/D1zwW+AuxMN95tV7pxWZsDe6/kuv83cc2bJLlzkif1Afp3wK+BG8a+bpskm/TnbtIP2t+iHz939di5kqbAECYJ4M3AIroZeecAZ/bHRi4HrqRrSfo4cFBVfX8Fj/Vs4Frgn4E/7D8ftb7cGTiG7g/8xXRjw57Q/9FfXScCX6QLTT8CfsvNu+iOo2tV+r+q+t7Y8aOAj9LNZLyk/9qDAarqKuBFwAfpguE1wHKzJVemqn4DvAX4dt/9+NCq+k/gbcDR/YzKc5kjUPWh9RnA+6rq8rGPS/p6J7skx72VLkD/co7ZjBsBL6f7uf2Cbjzei/r7vg6cB1w+GmtH97P7YV/rQcCzVvf/L+mWy7JWekm6uSSPBj5WVdu0rkWS1ie2hEmSJDVgCJMkSWrA7khJkqQGbAmTJElqYJ3bwHurrbaq7bffvnUZkiRJq3TGGWdcUVWTaw4C62AI23777Vm0aFHrMiRJklYpyY9WdJ/dkZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAY2bl3ArMobM9i16rAa7FqSJGk22BImSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDUw1hCXZK8mFSS5Kcsgc978yyVn9x7lJbkhyx2nWJEmSNAumFsKSLAAOB/YGdgb2T7Lz+DlV9faq2rWqdgUOBU6qql9MqyZJkqRZMc2WsD2Ai6rq4qq6Djga2Gcl5+8PfHKK9UiSJM2MaYawrYFLx24v7o/dTJLNgb2Az6zg/gOTLEqyaMmSJWu9UEmSpKFNM4RljmO1gnOfCHx7RV2RVXVkVe1WVbstXLhwrRUoSZLUyjRD2GJg27Hb2wCXreDc/bArUpIkbUCmGcJOB3ZMskOSTeiC1nGTJyXZAngU8Lkp1iJJkjRTNp7WA1fV0iQvAU4EFgBHVdV5SQ7q7z+iP/UpwJer6ppp1SJJkjRrphbCAKrqBOCEiWNHTNz+MPDhadYhSZI0a1wxX5IkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJamDj1gVo5fLGDHatOqwGu5YkSRs6W8IkSZIaMIRJkiQ1YHekVsuQ3aJg16gkaf1nS5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgOuEaZ0yS+uVuaWUJGk+bAmTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IDbFknrOLdPkqR1ky1hkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOuEyZprRhyvTJwzTJJ6z5bwiRJkhowhEmSJDVgd6Sk9YrdopLWFbaESZIkNWBLmCRNiZurS1oZW8IkSZIamGoIS7JXkguTXJTkkBWc8+gkZyU5L8lJ06xHkiRpVkytOzLJAuBwYE9gMXB6kuOq6vyxc7YEPgDsVVU/TnKnadUjSZI0S6bZErYHcFFVXVxV1wFHA/tMnHMA8B9V9WOAqvrZFOuRJEmaGdMMYVsDl47dXtwfG3dv4A5JvpnkjCTPmeuBkhyYZFGSRUuWLJlSuZIkScOZZgiba1rQ5PSdjYEHA48H/hR4XZJ73+yLqo6sqt2qareFCxeu/UolSZIGNs0lKhYD247d3ga4bI5zrqiqa4BrkpwM7AL8YIp1SZIkNTfNlrDTgR2T7JBkE2A/4LiJcz4H/GGSjZNsDjwEuGCKNUmSJM2EqbWEVdXSJC8BTgQWAEdV1XlJDurvP6KqLkjyJeBs4Ebgg1V17rRqkiRJmhVTXTG/qk4ATpg4dsTE7bcDb59mHZIkSbPGbYskaT3n9knSbHLbIkmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkB1wmTJA1iyPXKwDXLNPtsCZMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgNsWSZI2OENuobSy7ZM2xDpgxbXMSh1DsSVMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktTAVENYkr2SXJjkoiSHzHH/o5NcleSs/uP106xHkiRpVmw8rQdOsgA4HNgTWAycnuS4qjp/4tRvVdUTplWHJEnSLJpmS9gewEVVdXFVXQccDewzxetJkiStM6YZwrYGLh27vbg/NulhSb6X5ItJ7jfXAyU5MMmiJIuWLFkyjVolSZIGNc0QljmO1cTtM4G7V9UuwPuAz871QFV1ZFXtVlW7LVy4cC2XKUmSNLxphrDFwLZjt7cBLhs/oaqurqpf95+fANwqyVZTrEmSJGkmTDOEnQ7smGSHJJsA+wHHjZ+Q5C5J0n++R1/Pz6dYkyRJ0kyY2uzIqlqa5CXAicAC4KiqOi/JQf39RwBPA/4qyVLgWmC/qprsspQkSVrvTC2EwU1djCdMHDti7PP3A++fZg2SJEmzyBXzJUmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDWw2iEsyWZJ7jPNYiRJkjYUqxXCkjwROAv4Un971yTHTbMwSZKk9dnqtoS9AdgD+CVAVZ0FbD+dkiRJktZ/qxvCllbVVbf0wZPsleTCJBclOWQl5+2e5IYkT7ul15AkSVoXrW4IOzfJAcCCJDsmeR9w6sq+IMkC4HBgb2BnYP8kO6/gvLcBJ96iyiVJktZhqxvCDgbuB/wO+ARwFfDXq/iaPYCLquriqroOOBrYZwWP/RngZ6tZiyRJ0jpv41Wd0LdUHVdVfwK85hY89tbApWO3FwMPmXjsrYGnAH8E7L6SGg4EDgTYbrvtbkEJkiRJs2mVLWFVdQPwmyRb3MLHzlwPN3H73cCr+musrIYjq2q3qtpt4cKFt7AMSZKk2bPKlrDeb4FzknwFuGZ0sKpeupKvWQxsO3Z7G+CyiXN2A45OArAV8LgkS6vqs6tZlyRJ0jppdUPYF/qPW+J0YMckOwA/AfYDDhg/oap2GH2e5MPA5w1gkiRpQ7BaIayqPpJkE+De/aELq+r6VXzN0iQvoZv1uAA4qqrOS3JQf/8R86hbkiRpnbZaISzJo4GPAD+kG+u1bZLnVtXJK/u6qjoBOGHi2Jzhq6qetzq1SJIkrQ9WtzvyncBjq+pCgCT3Bj4JPHhahUmSJK3PVnedsFuNAhhAVf0AuNV0SpIkSVr/rW5L2KIkHwI+2t9+JnDGdEqSJEla/61uCPsr4MXAS+nGhJ0MfGBaRUmSJK3vVjeEbQy8p6reBTeton/rqVUlSZK0nlvdMWFfAzYbu70Z8NW1X44kSdKGYXVD2KZV9evRjf7zzadTkiRJ0vpvdUPYNUkeNLqRZDfg2umUJEmStP5b3TFhfw18KslldJtw3w3Yd2pVSZIkredW2hKWZPckd6mq04GdgGOApcCXgEsGqE+SJGm9tKruyH8Brus/fxjwauBw4ErgyCnWJUmStF5bVXfkgqr6Rf/5vsCRVfUZ4DNJzppuaZIkSeuvVbWELUgyCmp/DHx97L7VHU8mSZKkCasKUp8ETkpyBd1syG8BJLkXcNWUa5MkSVpvrTSEVdVbknwNuCvw5aqq/q6NgIOnXZwkSdL6apVdilX1nTmO/WA65UiSJG0YVnexVkmSJK1FhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhqYaghLsleSC5NclOSQOe7fJ8nZSc5KsijJI6ZZjyRJ0qzYeFoPnGQBcDiwJ7AYOD3JcVV1/thpXwOOq6pK8gDgWGCnadUkSZI0K6bZErYHcFFVXVxV1wFHA/uMn1BVv66q6m/eBigkSZI2ANMMYVsDl47dXtwfW06SpyT5PvAF4PlzPVCSA/vuykVLliyZSrGSJElDmmYIyxzHbtbSVVX/WVU7AU8G/m6uB6qqI6tqt6rabeHChWu5TEmSpOFNM4QtBrYdu70NcNmKTq6qk4F7JtlqijVJkiTNhGmGsNOBHZPskGQTYD/guPETktwrSfrPHwRsAvx8ijVJkiTNhKnNjqyqpUleApwILACOqqrzkhzU338E8FTgOUmuB64F9h0bqC9JkrTemloIA6iqE4ATJo4dMfb524C3TbMGSZKkWeSK+ZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqYKohLMleSS5MclGSQ+a4/5lJzu4/Tk2yyzTrkSRJmhVTC2FJFgCHA3sDOwP7J9l54rRLgEdV1QOAvwOOnFY9kiRJs2SaLWF7ABdV1cVVdR1wNLDP+AlVdWpVXdnf/A6wzRTrkSRJmhnTDGFbA5eO3V7cH1uRFwBfnOuOJAcmWZRk0ZIlS9ZiiZIkSW1MM4RljmM154nJY+hC2Kvmur+qjqyq3apqt4ULF67FEiVJktrYeIqPvRjYduz2NsBlkycleQDwQWDvqvr5FOuRJEmaGdNsCTsd2DHJDkk2AfYDjhs/Icl2wH8Az66qH0yxFkmSpJkytZawqlqa5CXAicAC4KiqOi/JQf39RwCvB34P+EASgKVVtdu0apIkSZoV0+yOpKpOAE6YOHbE2OcvBF44zRokSZJmkSvmS5IkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDUw1hSfZKcmGSi5IcMsf9OyU5LcnvkrximrVIkiTNko2n9cBJFgCHA3sCi4HTkxxXVeePnfYL4KXAk6dVhyRJ0iyaZkvYHsBFVXVxVV0HHA3sM35CVf2sqk4Hrp9iHZIkSTNnmiFsa+DSsduL+2O3WJIDkyxKsmjJkiVrpThJkqSWphnCMsexWpMHqqojq2q3qtpt4cKF8yxLkiSpvWmGsMXAtmO3twEum+L1JEmS1hnTDGGnAzsm2SHJJsB+wHFTvJ4kSdI6Y2qzI6tqaZKXACcCC4Cjquq8JAf19x+R5C7AIuD2wI1J/hrYuaqunlZdkiRJs2BqIQygqk4ATpg4dsTY55fTdVNKkiRtUFwxX5IkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNGMIkSZIaMIRJkiQ1YAiTJElqwBAmSZLUgCFMkiSpAUOYJElSA4YwSZKkBgxhkiRJDRjCJEmSGjCESZIkNWAIkyRJasAQJkmS1IAhTJIkqQFDmCRJUgOGMEmSpAYMYZIkSQ0YwiRJkhowhEmSJDVgCJMkSWrAECZJktSAIUySJKkBQ5gkSVIDhjBJkqQGDGGSJEkNTDWEJdkryYVJLkpyyBz3J8l7+/vPTvKgadYjSZI0K6YWwpIsAA4H9gZ2BvZPsvPEaXsDO/YfBwL/PK16JEmSZsk0W8L2AC6qqour6jrgaGCfiXP2Af69Ot8Btkxy1ynWJEmSNBNSVdN54ORpwF5V9cL+9rOBh1TVS8bO+TzwD1V1Sn/7a8CrqmrRxGMdSNdSBnAf4MKpFD1/WwFXtC6iNyu1WMfyZqUOmJ1arGN5s1IHzE4t1nFzs1KLdaza3atq4Vx3bDzFi2aOY5OJb3XOoaqOBI5cG0VNU5JFVbVb6zpgdmqxjtmsA2anFuuYzTpgdmqxjpublVqsY36m2R25GNh27PY2wGVrcI4kSdJ6Z5oh7HRgxyQ7JNkE2A84buKc44Dn9LMkHwpcVVU/nWJNkiRJM2Fq3ZFVtTTJS4ATgQXAUVV1XpKD+vuPAE4AHgdcBPwG+PNp1TOQWeoynZVarGN5s1IHzE4t1rG8WakDZqcW67i5WanFOuZhagPzJUmStGKumC9JktSAIUySJKkBQ5gkSVIDhjCtVUnuneRrSc7tbz8gyWsb1XL3JH/Sf75Zktu1qENalSSPSPLn/ecLk+zQuqaWkrwsye37mfMfSnJmkse2rkta2wxh85Dk4Um+kuQHSS5OckmSixvWs1mS+7S6fu9fgUOB6wGq6my65UkGleQvgE8D/9If2gb47NB19LVsnuR1Sf61v71jkic0quWeSW7df/7oJC9NsmWLWiYl2anBNZt/P5IcBryK7vcG4FbAx4asYaKehye5Tf/5s5K8K8ndBy7j+VV1NfBYYCHdzPl/GLgGkixI8tWhrzuXGXsd+ejqHBugjq+tzrFZZgibnw8B7wIeAewO7Nb/O7gkTwTOAr7U3941yeS6bEPYvKr+a+LY0gZ1vBh4OHA1QFX9D3CnBnUA/BvwO+Bh/e3FwJsb1fIZ4IYk96J7/u4AfKJRLZO+3OCas/D9eArwJOAagKq6DGjZavvPwG+S7AL8LfAj4N8HrmG0m8rjgH+rqu+NHRtMVd1A973YYuhrz2GWXkfuN34jyQLgwUNdPMmmSe4IbJXkDknu2H9sD9xtqDrWhmluW7QhuKqqvti6iN4b6DZN/yZAVZ3VPyGHdkWSe9JvP9XvIdpiAd7fVdV1Sfe6nWRj5tgSayD3rKp9k+wPUFXXZlTY8G7s1/B7CvDuqnpfkrNeIrEAACAASURBVP8e6uJJ3ruiu4AWLXJNvx+966qqkox+Z24z8PUnLe3r2Qd4T1V9KMlzB67hjCRfpgvFh/ZDCW4cuIaR3wLnJPkKfVAGqKqXDlxH89eRJIcCrwY2S3L16DBwHcOu0/WXwF/TBa4zx45fDRw+YB3zZgibn28keTvwH3TvUACoqjNX/CVTs7Sqrmr3t/0mL6b7ZdwpyU+AS4BnNqjjpCSjF4s9gRcBxzeoA+C6JJuxLJjek7Hny8Cu71/Enws8sT92qwGv/+fAy5n7/7//gHWMtP5+AByb5F+ALftu9OfTdeu38qv+j+2zgEf2rRxDf09eAOwKXFxVv0nye7RbzPsL/UdrzV9HquqtwFuTvLWqDl3lF0yvjvcA70lycFW9r1Uda4MhbH4e0v87vmloAX/UoJZzkxwALEiyI/BS4NQhC+hfrP+qqv6kfze/UVX9asgaxhxC90J+Dt27phOADzaq5TC6buJtk3ycrpv0eY1q+XPgIOAtVXVJPwB8yPFHpwPnVtXNnptJ3jBgHSOtvx9U1Tv6NwpXA/cBXl9VXxmyhgn7AgcAL6iqy5NsB7x9yAKq6sYk/wfs3LdiN1NVH+nDz3ZVdWHDUmbpdeS/kmxRVVcB9OMoH11VQ4+7PSrdxK/tqurA/m/ffarq8wPXscZcMX89kWRz4DV0A1mh2y7qzVX124Hr+HpVtQihM61/J/9Quqb771TVFQ1rafYHpR/H8duq+s3Q19a6I8nb6MLg+cAN/eGqqic1qOWJwDuATapqhyS7Am9qVMtMvI4kOauqdp049t9V9cCB6zgGOAN4TlXdv39tO22ytllmCJuHfrDmYcAj+0Mn0f1yXtWglgdW1dBjWeaq453AjsCnWH78xH8MXMfD6cbJ3Z2uxTddGXWPIevoa3nQHIevAn5UVYNOWpilPyizIMklzDFWcIjnSZJTquoRSX41UcPouXr7adewgrrG69mErivy11U12OD0JBcCD6iqVt3247WcQde78c1RyEhyTlX9/kDXn+v14yYthr8kObuqHjBxbLDvydg1F1XVbuMBMMn3qmqXIeuYD7sj5+co4FzgGf3tZ9PNYPmzBrW8K8ld6cLP0VV1XoMaAO4I/Jzlu2SLbtzckD4E/D+6d0k3rOLcafsA8CDgbLo/sPfvP/+9JAdV1ZCzAt/AzSdwzMSaVEm+WFV7D3zZ8aEEmwJPp3sOT11VPaL/d6bWr5usJ8mT6Z4zQ7qYLvw1D2HMPd52yNaLd67kvlbDXxYleRfdIPgCDqZ7rR1a83Fy82UIm597VtVTx26/MclZLQqpqsckuQtdIDwyye2BY6pq0CnMVdVq8OykWZq5+kO68TXnASTZGXgl8Hd04XTIENb0D8pK3tWHbiD2oKrq5xOH3p3kFOD1Q9bRf18eQfezOGUWWrVHquqzSQ4Z+LK/Ac5Kt+bT+KSnoWckQuPxtlX1mKGudQscDLwOOKa//WWgxaLcszRObo0Ywubn2iSPqKpT4KYusGtbFVNVlwPvTfINuvV9Xs/A68gk2QZ4H90vQwGnAC+rqsVD1sFszVzdabxlsqrO77uPL24wm7X1BI7T6brt5/qPD75ExUQo3IiuZWzQlqkkr6drgRu1Fn84yaeGfgM1Vs94S/7oezL0uJXj+o9ZcDDdeNvf0a0hdyLdG6hBTPw8bmbooR79Na8BDkly26r69dDXH6vjK0nOZNk4uZe1HG+7JhwTNg/9eJqPAFvQPQF+ATyvX1hw6FruSzeQ9Wl03YFHA5+pqp8NXMdX6F6oRqsnPwt4ZlXtOXAd35jjcLWYNNAPHv0F3c8Eup/TVnTd16dU1WAL/E5M4Aj9H5ShJnCk287qKf3iuZP3XVpV2w5Rx9g1x58nS+laLd8x5KSFJBcADxz9DPrulTOr6r5D1TBRz7+N3Rx9T/516NeSWZHk6VX1qVUdm+L1/20ld1dVPX+IOsYl+QO62ea3rart0i3s+5dV9aIGtTwA2J6xRqUWwXRNGcLWgr7rj+q22WhVw3eATwKfqm7F7VZ1zDVr5mbHNiT9H9UX0XU3ha518AN0i0Bu3vKd5NDSLd57zlwhJ8mTG0xxby7JF4H9q+qX/e0tgY9VVZMtaVpKcmxVPSPJOcw9YeIBc3zZtGs6s6oetKpjG5Ik36V7w3/c2ID4c6vq/gPXcRTwAOA8li3m2ySYrim7I9dAkmdV1ceS/M3EcQCq6l1D11RVDx36mitwRZJn0QVC6BbgnBx3MzUr+tmMNPrZXEs3uHauAbaDBrAk9wZewc3fOQ7SQlhVn06yR5Ldq+r0fnzcXsD3WwSwfsr/YYyNx6KbLTr152yS9/XX/B1wXt+KXMCefR1N9BM1Dubmz5EhZtC+rP+3eQBNsjfdtklbZ/mdHm5Pg63YktwZ+HvgblW1d/+787Cq+tDQtQBU1aUTwylaTIB6aFXt3OC6a40hbM2MthWZa+xIk6bFfnzPW4Gd6WZ5dcUMvyTD84H3A/9E9704tT82lJX9bJqYoZ8NdLNnj6DrShj8RTPdZtV7Axv3oeMhdDM1D+nHyb1l4JKOBk4GRhNsnkk32PhPBrj2ov7fM4D/HDv+zQGuvTKfpZtdfDwDbxVUVaMtznaenFiT5CC65+5QLqP72TyJ5Wf+/Ypu5vXQPkw3+/41/e0f0D1XW4SwS/suyUqyCd3Y0gsa1HFakp2r6vwG114r7I6chyQPr6pvr+rYQLWcQveO/p/otl/5c7qf72FD16LlzdLPJskZVTXYRrtzXP8culmQtwYuB7apqqv7LtvvDt3dNNf3Y7T20JB1zJIk362qh6z6zKnWcCrw2qr6en/7VXQrsg+9hAlJNh56Pb8V1HF6Ve0+sSZWk6EeSbYC3kP3ZiV0syNfNkQL8kQdj6R7s3A5XYvyaI29wbut15QtYfPzPrr1n1Z1bAibVdXXkqSqfgS8Icm36P74T11WvDEzMPzU8iQLgb/g5l0qLcYKNP3ZTDg+yYvoWl7GZ43+YqDrL62qG4DfJPnf0TjK6jYjbrFB8zeS7Acc299+GgPvE5jkCXSz7SYXFm6yWCvdnnyH0f1hbTWz+EnA55O8kq67eqf+2GDGx6XNNYu5wR/6a/ru81FND6Vb9HkwSd5WVa8CHlNVLfYEnnQU3QSnc2i3wfu8GMLWQJKHAX8ALJwYe3R7YEGbqvhtko2A/0nyEuAnwJ0GvP5BdAvXHkvXjN96J/HPAd8Cvkr7xVpb/2zGPbf/95VjxwoYqmv0uiSbV7dt0U0tUOl2nxjsRTTLVoUP8Dcs2y9yI7pxekMG5HfTLfB8Ts1G18Tv0/1h+yPGBjsz4KKgVXVFkifR/f6eATytwfem+bi0CS+nW7bjnkm+DSyke9MwpMel26vxULqhDa39uKpmZSmTNWJ35BpI8ijg0XTBY3yMwq+A4+eafj9ATbvT9clvSfeuegvgH6vqOwNd//fo1jral27Q6jF0S2RcOcT156hnZmZkruBn87aq+m7TwhpIcuuaYyuavnvjrlV1ToOymuqXyfjjqpqJd/JJvk+3ZdB1Da49uYXTJnSvJ0Xb1sGZkG4z8/vQvXm4sKquH/j6bwcOpBt7+5u+jtGbmcF/Pkk+QPe6ejzLt9q6RMWGIMnd++4ljUmyNd2syL8BXlVVH13Fl0yjhjcDp1bVCUNfe1X6F9J9q+rjDa59K+CvWLbf6TeBfxn6xXxW9GNKbqaqTh6wht3pwvlJLP+HZPCZvH09xwAHb6jrgo1kxvb2TPI9uje3x1TV/w557Tlq+VxV7dOyhr6OudZQW6eWqDCEzUM/u+vpY+v73IFu38Y/HbCG41nJjMyBppXfJN0K5PvTTbM/A3jnkDNXJrqZbkP3R+16Grxw9uvHvRjYmq4b4Sv97VcA32vxIpbkg3R78n2kP/Rs4IaqeuHQtcyC/vdnZFO6PRLPGGrJjr6GL9N1gS43rqWq3jhUDRP1fJNu7aXTWT4UDv1a8mcsWzrkW0MvYTJrb7KT3J2up2FfuufJMcCxVfXjgetYAJxYVUPMIF7vGcLmYXyWysqOTbmGR63s/qo6aaA63kg3huICumn/X5qFGUUtJfkccCVwGvDHwB3ouldeVlVN9hhN8r2q2mVVxzZUSbal68bff8BrztRszBW9pgz1WtLX8AHgXixbb3Bf4H+r6sUD1nDTgqxJPlPL7xPcVL/szevodiMZfBxykuOAZ1fVoBMDxq4/WmNvTkNPBJsPB+bPz41Jthu9E+nfqQyaaud6Yexb5LatqrMHLOV1wMXALv3H3/czippMGU7yFODroxeJdKuQP3rgd9P3qKrf76//QeAKYLuq+tWANUy6Ick9R90ZSe5B+4kLs2QxMOiq38BXkzy2qobcyH2FhgxbK/Eo4P6jwfhJPkLXUjik8clFLdb0u5kk2wPPoAulN9DtEdzCb4Fz+t6ga0YHBww/i1Z9yrrBEDY/rwFOSTJ60Xok3aDFwfVdCE+i+5meBSxJclJVzbly/BTsMNB1VtdhVXXTAphV9ct+2v2QIeymcVZVdUOSSxoHMOhmRX4jycV0f2TuzrCL6c6UiXfUG9GtYTb03q8vBv42yXUse860GHM0S2OgLgS2A0bdgdsCQ76phOW/B827jNJtFXQrulmJT6+qixuW8wUGXsplXFV9ZPx2kttUt6n4OsfuyHnqZ3WNdnA/rRrt4D7qBk3yQrpWsMOSnL0uLVq3Ns31f09yzqhlaqAabmDZu8QAmzE2o6jFTK8kt+4/Hc2w+j5dMTebsbghSPLcsZtLgR9Wg8WWtbz+je3uwH/1h3an69b/DQwzPm3s93f8dxfaDczfqaq+P+Q1VybdAsvb1YCb3c9Rw8PodgxovpH4mrIlbA2Mfhn6QejQrYsFsF3fPTnkooYjGye5K11T9WtWdfIGYFGSdwGH072LPZjltx6ZuhZjNVbDaf04l5taFZKcSZsFhmfBp4HfVreALEkWjK1jNph+TaybZqxW1eeHvP5YHRsBZ9fAGzHP4fWNrz+Lv79XJvkQM7B3ZJInAu+gG+O6Q5Jd6fZcHXTyBt0ae39KN/GJqvreimY8zypD2Jp5Od1q7HNtyDzoooZj3gScCHy7uo2R7wEMvl7ZDDmYbpzaMSzbVmOwQb2zJsld6GZpbpbkgSwb73J7YPNmhbX3NbqtV0YbqW9G91z5g6EKSPIPdC09oyVLXpbkEVV1yFA1jFTVjUm+Nz7WtYXRuLR+hvH4jhdD7ewwiz7M7Owd+Qa6mcTfBKiqs9Jt/D64mo2NxNeYIWwNVNVf9P8+pnUtI1X1KcZWMO7HCzSZzZNuQ9d79zcHX1AQoB8fMPgfsRn2p8DzgG3o3jyMXrWuBl7dqKZZsGlVjQIYVfXrJEOH0scBu1a/WGs/CP2/aff8vStwXpL/YvlB14O1ciQ5kG7ttGvplmMYLQo6EwPkG9mqqo5NcihAVS3tu0xbWFpVV02EnxZjm2ZlI/E1ZghbA/36NStUDVbrTbIN3b6VD6f7ZTiFbimExQPX8Wi6Nah+SPfCuW2S59aAi1/2dSykmzl0P7r1nwAYcv2nGbNzVT0myTOq6thVn77BuCbJg0ZDCJI8mO4P/9C2BEatPFs0uP64JuuTTXglcL9WY2xnVPO9I8ecm+QAYEG/XMZLgVMb1HEQ3UbiW9PNbF7nejwcmL8GxlbpvRNdt8XX+9uPoRvPsdKQNqWavgJ8AhitTv8sujVk9hy4jjOAA0aDNZPcG/hkVT145V+51uv4Ml1T/SvoflGfCyypbvPZDU66zYgfBHx3tPaRblqt/miWjeu8K91uBoONH0yyP/APwDfo3rg8Eji0qo4eqoa+jk3pflfuRbccxIdarfWX5EvAnw09Nm+W9WOQ30e3hMq59HtHDrwU0aiWzem6RR/bHzoReHNV/XboWtZ1hrB5SPJ54C+q6qf97bsChzcKYTfbK3GuYwPUMdesxMFnaSY5o6oePH7tfsmOlS5uu77KjO35NkvSbeV002zRFt3n/WvH7n0N362qyxvUcAzdEhnfAvYGflRVLxu6jr6WB9KNf/ouy6/av84swjkNab935EwEdRdr1cj2owDW+z+WjYUa2hVJnsWyFab3B37eoI5F/QyeUYvcMxl4VmJv9OL00ySPp2vp2KZBHTOhql4JvDIzsufbjNkd2J7u9fCBSaiqf5/2RZO8FfinqvpZ/zpy3Nh9b2vQarvz2OLCH2LZ8hAt/AtdD8NyWzmJPVj2XH3QUM/VMR9h+aB+X+CvB7z+yPhirW8EDmtQw1phS9g8JHk/sCNd8ClgP+Ciqjq4QS3bAe8HHtbXcirdmLBB9z7r16F6Md2ebwFOBj4w9DpUSZ5A90KxLV0T/u2BN1bVcSv9wg1Aup0ddqyqr/Zr/Ww8A4vINpHko8A96RY4Hg1yriHeSSe5Cvgl8KKq+sLEfTdtmTOUyWu2qGHs2qdW1WAzVNcFLZ+rYzWcMxbUNwb+q/Xwhgy8VeDaZgibp36Q/h/2N0+usVXapVmT5C/ouiXvWFX37AfVHlFVf9y4tCaSXEDXAjT4C2GS/6bbQP3jdG8YXjEaU9PiD8ssLS6c5C10q+Ufz/LdkRvsEhUtn6tjNcxMUJ+lGubD7sh56mdCDj4bciTJ31bVP66oj3yod0lJvjHX9ZeVMcwf+STvXdn969JYgSl5MV2XxncBqup/ktypbUlNnQvcBfjpqk6cgqqqc5M8BPhHuq78A1oMtO6LmaXFSQ/o/z107NiGvkRFy+fqyC5Jru4/D926g1fj2NI1ZghbA7n53mrLGfiJOFoTpfWGpq+Y49hD6ZaJ+NmAdRxE92J1LN04sKz89A3O76rqutH6Pn2XwobcHL4VcH6/JtZ4i8tga2L1rV8vTbI3cPyq3khsCKpq1vaibSbJ8XS/o7ej/XN1JoL6xN/gzSeC4ToVBg1ha6CqbgeQ5E3A5XSD0EM3CP12A9dyfP/vR1Z17pTruGnwfZJH0a1Wf2vgoKr64oCl3BV4OrAv3V6AxwCfqaorB6xhlp2U5NV072D3BF5E1+WzoXpDw2svv9Jl1ReT7AYcBWyQe76OJHnOXMcHHoQ+K44D7kzXZT3uUcBPhi+nvdHf4PWBY8LmIcl3q+ohqzo25RpG75LmNPAq139KF75+C7ylqr4x1LVXUM/WdLNE/wZ4VVV9dBVfst5LtzfgC+jW9wnd+j4fbDnOZEOVZJsVLaac5KFV9Z2ha5oV/fCKkU2BPwbOrKqnNSqpmX4ppFdPdlP3gf2wqnpim8q0NtgSNj83JHkm3WKPRfcHf+htJN7R//tndOMFPtbf3p9u1fpBJDmdbvHAtwOn9cduGixZA29q3l97f2BP4Iu0WSZj5lS3N+Bngc9W1ZLW9bSykiEFg3VnrCiA9fdtsAEMYHKGeZItWLbszYZm+7nGCVbVoiTbD1+O1iZbwuah/wV4D8u2Cvo2DZaF6Gs5uaoeuapjU7z+N1n2R220COhI1UDbBSV5I/AEurFyRwNfarXq9yxJNwjsMOAldD+b0L1heF9VvallbdKq9Avqnl1V921dy9CSXFRV97ql92ndYAhbi/o1l55Q3WbaQ1/7AuDx1W3cTbod7U/Y0F60ktwIXMyy/f9GT/BRC8cGOdYmyf+j2yj6wKq6pD92D+Cf6YLqP7WsTxo3McxiI2Bn4NiqarWpeTNJPgl8var+deL4C4DHVtW+bSrT2mAIm6ckC+jG1+zf/3tKi3ELSfYCjqQLINCtqvyXVXXi0LW01C9EukItWilnQb8m1Z41sSFyuo3Ov7wuL3a4rutbKZ8J3KOq3tQvvHyXqmq5Yn1T/eSekaV0WyitsPt2fZbkzsB/AtexbFjFbsAmwFOqwRZXWnsMYWsoySPp1rJ5PN32Hg+nexFttuFsv1r9Tv3N7w+9Sr1mV5Jzq+r+t/Q+TV+Sf6bbmuePquq+Se5AF4x3b1za4GZlb8JZlOQxdJt3A5xXVV9vWY/WDgfmr4Eki4Ef03XlvLKqfpXkksYBbHJK9y4N9hXT7LpuDe/T9D2kqh7Ut1ZSVVcm2aR1UY1M7k24M9BkE/FZ0882bzrjXGufIWzNfAZ4Mt1aVDck+RztF7wcf9d805RuYPAQ1i8NcXfGnl9VdfLQdWg54ytdjwvd80XtXN8Payi4qYt4Q920epY2EZemzu7INdSP43gM3Viwx9FtEP0CusHwv25ZGyyb0j3kOmH9dd9GF07PZ/lNZgeto69lM2C7qrpw6GtLq6tf5mZf4EF0LUFPA15XVcc2LayBWdybUJomQ9ha0E+f3ot+cH5VbdW4pFFN51TVTqs8ee1e90LgAa3HoyV5It0aaptU1Q5JdgXe1CIMSquSZCe61usAX6uqC1bxJeulWdpEXBqC3ZFrQVVdT7f1y/F968vgJqZ0LwDuS7d/4tAuBm7F2N5mjbyBbqPqbwJU1VkubKhZlOSjVfVs4PtzHNugzMrehNJQDGFrWVVdu+qzpuIdY58vpXvnuP9QF++3GSm6d61nJfkay28y+9KhauktraqrRhtVSzPsfuM3+vFhD25Ui6QBGcLWE1V1Ut/ldgDwDOASugkEQ1nU/3sG3Yazy5U3YB0j5yY5AFiQZEfgpcCpDeqQ5pTkUGC0mfrVLNtl4jq6Nf8kreccE7aW9Bsj37aq5pqBNs3r3hvYj67V6+fAMcArqmqli5ZOsZ6XVdV7VnVsgDo2B17D8htV/11V/XbIOqRVSfLWqjq0dR2ShmcIm4ckn6BbWPAGuhagLYB3VdXbB6zhRro1dV5QVRf1xy6uqnsMVcNEPTebzZTkv12RXVpekp2q6vvjG92PG3rTe0nDsztyfnauqqv7KeYnAK+iC2ODhTDgqXQtYd9I8iW6TasHHwiVZH+6rtAdkox3R96OroVu6HruDbyCbvum8fXKBtlIXFoNfwMcCLxzjvsK2GCfq0l+xc2HMVxFN+zh5aM9cqV1nSFsfm7VLwXxZOD9VXV9kkGbFqvqP+H/t3f3QXbV9R3H358EgQABJAJKMU8MLUNCCgHlKVAeZjq22kwplAgqFRgtozzK0FbrFCswtLWDIrYUFK3SUBiwEYsU0AzlMSESCSHIowTQgEUKoSkQDPDpH+ds2F12N9vsvfd3c+7nNZPJveee3f0sw95893d+5/tlgaSt6xxnATvXo1AW2L6lQ1HuBp4F3sXAf1TWAMs7lKG/a4F/Ar7BW/3KIrqG7U/Wfx9eOksXugh4BriK6pfKDwPvBh4BvgkcVixZRAvlcuQYSDqdavXrfqoZkpOBf7F9SOFcOwB/DMzr1ZUfSUtt5w6z2CRIOoi3r9r27MgxSffY3n/QscW2D5B0v+3fLpUtopVShLVQ3UV/fC8OnJV0p+05Q1xG6GiTxboAhepuyOeABQxslfFCJ3JEjJakK4HdgGUMnDLR6bYuXUPSIuDLwHX1oWOAz9RF2DLbe5dLF9E6KcI2Qr9h2a/avrZomBhA0kqqInCofXEudcNCxHAkPUS1vzRvxjVJ04GLgQOpfp4XU221WAXsa/vOgvEiWiZ7wjbOtPrvNUVTdDFJO9FvMLTtpzv0pY+3vahDXyuiFVZQ7Xd6tnSQblFvvP+DYV5OARaNkZWwaClJc6k25u9CdTlwCvCQ7RkjfmDrvn4G/sYmod+osYnA3sASBl4679k5p5J2BD7B2/fJnVQqU0Q7ZCVsDOo2CJcCO9ueKWkWMNf2+YWjlXQecADwI9v7SDqcDo5PokB7joiN9PcbPqVnXU/V//BH5O7maLCshI2BpNuAc4DL+pqRSlphe2bZZOVIutf2fpLuB/ax/aakJbbf36Gvvxq4fbjXe3l1IbqLpDOBu4D7evFmnpFk8330iqyEjc1WtpcMGhLd62+mqyVtQ1UIzZf0HJ39b/Irhm5+GdFtdqXafL6HpOVUvfbuAhblLl5ukPT7tm8sHSSinbISNgaS/gM4FbjW9mxJx1CND/q9wtE6TtJk20/XTWNfBcYBH6Ea5TTfdke65mdPWGxqJG0O7AccRHU34IHAatt7Fg1WUN3qZmuqPXLr6HCrm4hOyUrY2HwauJzqN9lVwErgo2UjFfM9YLbtlyV91/bRwLcL5HiywNeMGIsJwLZUv7BsR9Up/oGiiQqzPbF0hohOyEpYC9SrP+Ns92zLiv5DujOwO2LDJF0OzKBqdXMPVS+sxbZfLBqsoAw1j16TlbAxkLQF1QDtqcBmfXvDbH+xYKxSPMzjiBjaZGAL4DGqJqS/AFYXTVRehppHT8lK2BhIugl4CVhKv9uobffcxnBJbwAvU+3dmAC80vcS2csRMaR61NkMqv1gBwEzgReoNuefWzJbRLRfirAx6PV2FN1M0kLbR27oWEQ3kLQrcDBVIfYhYJLt7cumKitDzaMX5HLk2NwtaS/bPb2JtptI2hLYCniXpHfyVvPWbam6+Ed0BUmnUxVdB1PdAXgXsAj4Jj2+MX+4oeZAirBolBRhYzMH+Hg9NPo13rr0NqtsrJ72p8CZVAXXUt4qwv4H+IdSoSKGMBW4DjjLduZGDrQfGWoePSCXI8dA0pShjtt+qtNZYiBJp9m+pHSOiPj/k3QtcHqK02i6rISNQV+xJWknYMvCcWKgX0qaaHuNpM8Ds4Hzc4t7RPcaNNT8p5Iy1DwaLSthYyBpLtWt1LsAzwFTgIdszygaLJC03PYsSXOAC6mGJX/O9v6Fo0XEMCT9zkiv276tU1kiOmFc6QCbuPOAA4BHbU8DjqTaXBvl9W3m/SBwqe3rgc0L5omIDbB9W11o3QvcUT9+lmqSwN1Fw0W0QYqwsVlXz0QcJ2mc7VuBvUuHCgBWSboMOBa4sW6sm//fIzYNtwNbSvoNYCFwIvDPRRNFtEH+URqb1ZK2Ae4A5ku6GHi9cKaoHAvcDHzA9mpgB+CcspEiYpRk+xXgj4BLbB9F1dQ2olFShI3NXKrO8GcANwGPUzVagTj53wAACNJJREFUjMLqN/DrgZclTQbeATxcNlVEjJIkHQh8BPhBfWx8wTwRbZG7IzeCpDW8fT5iXz+qv5L0M+AvbS/sbLLoI+k04Fzgv4A368MG0sMtovudAXwWWGD7QUnTgVsLZ4poudwd2WKSxlPNf5ufkUblSHoc2L/esxcREdF1shLWYrbfAO6XlEahZf2carh6RGxiJO0I/BnVPrD1PRhtH1EsVEQbpAhrE9uXlc7Q454A/lPSDxjY7PGicpEiYpTmA9dQ7bE9BfgT4FdFE0W0QTbmR1M9DfyQqjfYxH5/IqL7TbJ9BVUboNtsn0TVkzGiUbISFo1k+69LZ4iIjbau/vtZSR8EngF2LZgnoi1ShEWjSPqK7TP7zaAbILPnIjYJ50vaDjgbuATYFjirbKSI1svdkdEokva1vXS4GXSZPRcREd0iRVhERHQVSdOA04Cp9Ltik5XsaJpcjoxGkrQ7cCGwJwNvcZ9eLFREjNb3gCuAf+etZssRjZMiLJrqW1Qd878MHE41AFgjfkREdIu1tr9aOkREu+VyZDSSpKW295X0gO296mN32D6kdLaIGJmk44HdgVsY2OfvJ8VCRbRBVsKiqdZKGgc8JulUYBWwU+FMETE6ewEfA45g4OzXdMyPRslKWDSSpPcBDwHbA+cB2wF/Z3tx0WARsUGSHgZm2f516SwR7ZQiLCIiuoqka4DTbD9XOktEO+VyZDTSMM1aXwLuBS6zvbbzqSJilHYGHpb0YwbuCUuLimiUrIRFI0m6GNgR+Nf60Dzgl8AEYFvbHyuVLSJGlmbL0StShEUjSbrd9qFDHZP0oO0ZpbJFxOhImgQcCjxte2npPBGtNq50gIg22VHS5L4n9eMd66fZ7BvRhSTdIGlm/fg9wArgJOBKSWcWDRfRBtkTFk11NnCnpJ9RNWmdBnxa0tbAt4smi4jhTLO9on58IvBD2ydImgjcBXylXLSI1ksRFo1k+8Z6dNEeVEXYw8AbtteRN/KIbrWu3+Mjga8D2F4jKeOLonFyOTIay/ZrwHJgB+BrwC/KJoqIDfi5pNMkHQXMBm4CkDQBeEfRZBFtkCIsGknS/vUdkk8B3wfuoFoVi4judTIwA/g4MM/26vr4AVTzYCMaJXdHRqNIugA4Fniaqj3FAuBe29OKBouIiBgke8KiaT4JPAJcCtxge62k/KYRERFdJ5cjo2neDVwAzAUel3QlMEFSfuGIiIiuksuR0ViStgQ+BBwHzAEW2j6+bKqIiIhKVsKisWyvtX2d7aOB3YGbS2eKiA2T9JuSFkpaUT+fJenzpXNFtFpWwiIioqtIug04B7jM9j71sRW2Z5ZNFtFaWQmLiIhus5XtJYOOvV4kSUQbpQiLiIhu87yk3QADSDoGeLZspIjWy+XIaCRJW1HNj5xs+xP1CKPfsn1D4WgRsQGSpgOXAwcBLwIrgY/afrJkrohWSxEWjSTpGmApcILtmfXYk0W29y4cLSJGSdLWwDjba0pniWiH9E6KptrN9jxJxwHYflWSSoeKiA2TtAVwNDAV2KzvR9f2FwvGimi5FGHRVL+uV7/69pTsBrxWNlJEjNL1wEtUq9n5uY3GShEWTXUucBPwXknzgYOphgJHRPfb1fYHSoeIaLfsCYvGkjQJOAAQsNj284UjRcQoSLocuMT2A6WzRLRTirBoJEmzhzj8EvCU7fQbiuhCdYf8N6mu0uwOPEF1OVKAbc8qGC+i5VKERSNJWgzMBpZTvYHPrB9PAk6xfUvBeBExBEkvAsPewWz7qQ7GiWi77AmLpnoSONn2gwCS9qQag3Ie8G9AirCI7rMyhVb0khRh0VR79BVgALZ/Kmkf20+kU0VE19pJ0meGe9H2RZ0ME9FuKcKiqR6RdClwdf18HvBo3X9oXblYETGC8cA2VFsIIhove8KikeoeYZ8C5lC9od8J/COwlmo48P8WjBcRQ5D0E9tD3VQT0UgpwiIioitIus/2PqVzRHRKirBopHpg94XAnsCWfcdtTy8WKiJGJGkH2y+UzhHRKeNKB4hok28BlwKvA4cD3wGuLJooIkaUAix6TYqwaKoJthdSrfY+ZfsLwBGFM0VERKyXuyOjqdZKGgc8JulUYBWwU+FMERER62VPWDSSpPcBDwHbUzVo3Q74W9v3FA0WERFRSxEWPUHSZsA82/NLZ4mIiIDsCYuGkbStpM9K+pqk31XlVOBx4NjS+SIiIvpkJSwaRdL1wIvAIuBI4J3A5sAZtpeVzBYREdFfirBoFEkP2N6rfjweeB6YbHtN2WQRERED5XJkNM36uZC23wBWpgCLiIhulJWwaBRJbwAv9z0FJgCv1I9te9tS2SIiIvpLERYRERFRQC5HRkRERBSQIiwiIiKigBRhEREREQWkCIuIRpF0lCRL2mOY17eX9Kl+z3eRdN0In2/A+RERrZIiLCKa5jjgTuDDg1+oe8dtD6wvqmw/Y/uYET7fgPMjIlolRVhENIakbYCDgZOpizBJh0m6VdJVwAPA3wC7SVom6UuSpkpaUZ87Q9KS+rXlknYf4vz3SLq9fr5C0iFlvtuI2NRtVjpAREQL/SFwk+1HJb0gaXZ9/P3ATNsrJU2tH+8NUD/vcwpwse35kjYHxgN/Mej8s4GbbV9Qr6xt1YHvKyIaKCthEdEkxwFX14+vrp8DLLG9chQfvwj4nKQ/B6bYfnWIc34MnCjpC8BemcgQERsrRVhENIKkScARwDckPQmcA8yjmpbw8ggfup7tq4C5wKvAzZKOGOKc24FDgVXAlZJOaMk3EBE9J0VYRDTFMcB3bE+xPdX2e4GVwJxB560BJg71CSRNB56w/VXg+8CswedLmgI8Z/vrwBXA7KE+V0TEhqQIi4imOA5YMOjYd4Hj+x+w/d/AXfWm+i8NOn8esELSMmAPqqJu8PmHAcsk3QccDVzc+m8lInpBZkdGREREFJCVsIiIiIgCUoRFREREFJAiLCIiIqKAFGERERERBaQIi4iIiCggRVhEREREASnCIiIiIgr4P289VahrKgRDAAAAAElFTkSuQmCC\n&quot;,
      &quot;text/plain&quot;: [
       &quot;&lt;Figure size 720x720 with 1 Axes&gt;&quot;
      ]
     },
     &quot;metadata&quot;: {
      &quot;needs_background&quot;: &quot;light&quot;
     },
     &quot;output_type&quot;: &quot;display_data&quot;
    }
   ],
   &quot;source&quot;: [
    &quot;pretty_recommend_artist(df_by_artists, name_rate_dict_1, how_many)&quot;
   ]
  }
 ],
 &quot;metadata&quot;: {
  &quot;kernelspec&quot;: {
   &quot;display_name&quot;: &quot;Python 3&quot;,
   &quot;language&quot;: &quot;python&quot;,
   &quot;name&quot;: &quot;python3&quot;
  },
  &quot;language_info&quot;: {
   &quot;codemirror_mode&quot;: {
    &quot;name&quot;: &quot;ipython&quot;,
    &quot;version&quot;: 3
   },
   &quot;file_extension&quot;: &quot;.py&quot;,
   &quot;mimetype&quot;: &quot;text/x-python&quot;,
   &quot;name&quot;: &quot;python&quot;,
   &quot;nbconvert_exporter&quot;: &quot;python&quot;,
   &quot;pygments_lexer&quot;: &quot;ipython3&quot;,
   &quot;version&quot;: &quot;3.8.2&quot;
  }
 },
 &quot;nbformat&quot;: 4,
 &quot;nbformat_minor&quot;: 4
}</code></pre><h4>3. Review</h4><p>Like every recommender system, this system has its own advantages and disadvantages. You can find my own pro-con-list for building a genre-based recommender system below:</p><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*uhww3vJxypCRbND8yLH2TA.jpeg" /><figcaption>Groupmap.com</figcaption></figure><h4>Conclusion</h4><p>In this article, we first examined the algorithm of genre-based recommender system, then we implemented the code of the algorithm, and finally discussed about the pros and cons of this recommender system. Happy coding :)</p>
