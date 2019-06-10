## Part 4: word cloud and top-k results analyses

### Overview of Part 4
In this part, we first build a word cloud to see the 12 topic clusters and which words are most frequent inside each topic. Then we will analyze some typical pairs and the correlation between two these two firms through the results about nearest firms of top-k model. The conclusion is that our method can help find competitors, business partners and affiliates.

### Pre-processed Data
Top 50 nearest firms for each year got from top-k model.

### Results
* Word cloud is below:
* ![](https://github.com/KenChenCompEcon/CMSC123-Project/blob/master/Part4/wordcloud.png)
* 12 latent topics are uncovered by our K-means clustering. Additionally, we’ve computed the topic loadings on all these clusters and recovered the most loaded words, by mapping to the dictionary we got from the first steep. From the graphs above we know that some of clusters reflects the industry the firm belongs to.

*Top 50 analyses
*![](https://github.com/KenChenCompEcon/CMSC123-Project/blob/master/Part4/topk.png)

*In this part, we use examples from our top-k model to illustrate 3 typical relationships between near firms. 
*In SEC system, ANAREN is registered as a radio & tv broadcasting & COMMUNICATIONS EQUIPMENT company. The nearest one for this company in the topic model is API Technologies Corp, which is registered as a SEMICONDUCTORS manufacture company. And we google the two firms find that ANAREN is APIi's first competitor.
AVANEX is also a SEMICONDUCTORS manufacture company. Its pair is LRAD, which is HOUSEHOLD AUDIO & VIDEO EQUIPMENT. These two are in the same industry chain.
In the Top-k model, we also find a firm matches many different firms. It is bally total fitness in Illinois. The paired firms are BALLY TOTAL FITNESS OF THE MID-ATLANTIC, BALLY TOTAL FITNESS OF UPSTATE NEW YORK, BALLYS FITNESS & RACQUET CLUBS in Florida, BALLY TOTAL FITNESS OF GREATER NEW YORK. So we can also use our method to find out the affiliate firms run the same business.
