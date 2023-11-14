from dataset import Dataset
from sentence_similarity import SentenceSimilarity
import csv
from students.models import Final



with open('data.csv','w',newline='') as csvfile:
    csvw=csv.writer(csvfile,delimiter=',')
    for f in Final:
        csvw.writerow([f.title,f.teamname])

data = Dataset('data.csv')
sentence_sim = SentenceSimilarity(data)

most_similar = sentence_sim.get_most_similar("How is it possible for machines to learn?")
print("\n".join(most_similar))