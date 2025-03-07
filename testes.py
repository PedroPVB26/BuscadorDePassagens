import pandas as pd
from itertools import chain

dicionario1 = {
    'Empresa' : ['Gol'],
    'Preço': [1500]
}

t1 = pd.DataFrame(dicionario1)

dicionario2 = {
    'Empresa' : ['Latam'],
    'Preço': [500]
}
t2 = pd.DataFrame(dicionario2)

tbs = [t1, t2]

tf = pd.concat(tbs)


print(tf)