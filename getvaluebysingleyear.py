import pandas as pd

def vrednost_iz_excela(putanja_do_fajla, aop_vrednost, godina_vrednost):
    df = pd.read_excel(putanja_do_fajla)

    df['AOP'] = df['AOP'].astype(str).str.zfill(3)  

    
    filtrirani_df = df[(df['AOP'] == aop_vrednost) & (df['Godina'] == godina_vrednost)]
    
    if not filtrirani_df.empty:
        return filtrirani_df['Bruto tekuća'].values[0]
    else:
        return None  
    
# ------------------Primjer dodjele vrednosti varijabli--------------------

Kratkorocna_potrazivanja = vrednost_iz_excela('bilans_stanja.xlsx', '031', 2021) 
print(Kratkorocna_potrazivanja)  
