import pandas as pd

def vrednosti_iz_excela(putanja_do_fajla, opis_vrednost, godine_vrednosti):
    df = pd.read_excel(putanja_do_fajla)
    
    filtrirani_df = df[(df['Opis'] == opis_vrednost) & (df['Godina'].isin(godine_vrednosti))]
    
    if not filtrirani_df.empty:
        return filtrirani_df['Bruto tekuća'].values  
    else:
        return None  

# --------------Primjer dodjele vrednosti promjenjivoj---------------------------


Kratkorocna_potrazivanja = vrednosti_iz_excela('bilans_stanja.xlsx', 'II - KRATKOROČNA POTRAŽIVANJA, KRATKOROČNI PLASMANI I GOTOVINA (040 + 047 + 056 + 059 + 060)', [2021, 2022, 2023]) 
print(Kratkorocna_potrazivanja)
