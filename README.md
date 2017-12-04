# citycompare
city compare compares cities

# to run local
- pip install -r requirements.txt
- python run.py
- browse to localhost:5000

# to deploy
push to master

#Development progress:
20171203 
Attempted to train 100 topic LDA on 20,000+ wikiepdia articles and then apply it to the city database descriptions. After classification the accuracy was not the greatest even with  98% accuracy requirement. This was most likley because the topics are too broad. Next step is to attempt to classify on the city descriptions only.
