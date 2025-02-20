# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:35:22 2024

@author: eveli
"""

# 1. INLADEN VAN DE PACKAGES EN GEGENEREERDE CSV-BESTANDEN

# 1.1 packages inladen
import pandas as pd
import matplotlib.pyplot as plt

# 1.2 datasets (csv) inladen
df = pd.read_csv('simulatie_resultaten35.csv')
df57 = pd.read_csv('simulatie_resultaten57.csv')
df79 = pd.read_csv('simulatie_resultaten79.csv')
 

# 2. AANROEPEN VAN DE BENODIGDE GEGEVENS

# 2.1 twee snelheden selecteren
df_hoge_snelheid = df[df['Snelheid'] == 'hoge snelheid (1.5 m/s)']
df_lage_snelheid = df[df['Snelheid'] == 'lage snelheid (1.0 m/s)']

# 2.2 berekenen van de gemiddelde waarden per dag per strategie
gemiddelden_lage_snelheid = df_lage_snelheid.groupby('Strategie')[['Totaal Observaties', 'Totale Reistijd']].mean()
gemiddelden_hoge_snelheid = df_hoge_snelheid.groupby('Strategie')[['Totaal Observaties', 'Totale Reistijd']].mean()


# 3. BEREKENEN EN VISUALISEREN VAN DE RESULTATEN

# 3.1 berekenen reistijden per strategie per snelheid
print(f"De gemiddelde reistijden per strategie per dag bij 1 m/s \n{gemiddelden_lage_snelheid['Totale Reistijd']}")
print(f"De gemiddelde reistijden per strategie per dag bij 1.5 m/s \n{gemiddelden_hoge_snelheid['Totale Reistijd']}")

# 3.2 plot voor aantal observaties per rijstrategie
plt.figure(figsize=(8, 5))
gemiddelden_hoge_snelheid['Totaal Observaties'].plot(kind='bar', color='skyblue', legend=False)
plt.title('Het gemiddelde aantal observaties per strategie per dag')
plt.ylabel('Gemiddelde aantal observaties')
plt.xlabel('Strategie')
plt.xticks(rotation=0)
for i, value in enumerate(gemiddelden_hoge_snelheid['Totaal Observaties']):
    plt.text(i, value - 0.02 * value, f'{value:.2f}', ha='center', va='top', fontsize=10)
plt.tight_layout()
plt.show()
 
 
# 3.3 plot voor de reistijd per strategie per dag
plt.figure(figsize=(8, 5))
gemiddelden_hoge_snelheid['Totale Reistijd'].plot(kind='bar', color='skyblue', legend=False)
plt.title('De reistijd per strategie per dag')
plt.ylabel('Gemiddelde reistijd in minuten')
plt.xlabel('Strategie')
plt.xticks(rotation=0)
for i, value in enumerate(gemiddelden_hoge_snelheid['Totale Reistijd']):
    plt.text(i, value - 0.02 * value, f'{value:.2f}', ha='center', va='top', fontsize=10)
plt.tight_layout()
plt.show()

# 3.4 aantal observaties per dag voor 3 verschillende observatietijden

# 3.4.1 definieren van snelheid 1,5 ms en strategie nearest
df = df[df['Snelheid'] == 'hoge snelheid (1.5 m/s)']
df57 = df57[df57['Snelheid'] == 'hoge snelheid (1.5 m/s)']
df79 = df79[df79['Snelheid'] == 'hoge snelheid (1.5 m/s)']

df = df[df['Strategie'] == 'nearest1']
df57 = df57[df57['Strategie'] == 'nearest1']
df79 = df79[df79['Strategie'] == 'nearest1']

# 3.4.2 organiseren en aanroepen van de benodigde gegevens
# hernoemen van kolommen Totaal Observaties
df57 = df57.rename(columns={'Totaal Observaties': 'Totaal Observaties57'})
df79 = df79.rename(columns={'Totaal Observaties': 'Totaal Observaties79'})

# kolommen toevoegen aan dataset df
df['Totaal Observaties57'] = df57['Totaal Observaties57']
df['Totaal Observaties79'] = df79['Totaal Observaties79']

# gemiddelde en percentages berekenen
gemiddelden = df.groupby('Strategie')[['Totaal Observaties', 'Totaal Observaties57', 'Totaal Observaties79']].mean()
percentages = gemiddelden/161*100

# weergeven en printen van de gemiddelden
print(gemiddelden)
print(percentages)