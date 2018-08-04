import matplotlib.pyplot as plt

models = ('Baseline', 'Borda', 'Markov')
y = [0.732575869237, 0.824848875661 , 0.882938879441]
n = [0,1,2]

plt.bar(n, y, align='center', alpha=0.5)
plt.xticks(n, models)
plt.ylabel('MAP Score')
plt.xlabel('Ranking models ')
plt.title('Analyzing Ranking Models using MAP Score ')
plt.show()
