import pandas as pd

def vrednosti_iz_excela(putanja_do_fajla, aop_vrednosti_po_godinama):
    df = pd.read_excel(putanja_do_fajla)
    
    df['AOP'] = df['AOP'].astype(str).str.zfill(3)
    
    rezultati = []
    
    for godina, aop_vrednost in aop_vrednosti_po_godinama.items():
        filtrirani_df = df[(df['AOP'] == aop_vrednost) & (df['Godina'] == godina)]
        
        if not filtrirani_df.empty:
            rezultati.append(filtrirani_df['Bruto tekuća'].values[0].item())
        else:
            rezultati.append(None)  
    
    # return pd.Series(rezultati)
    # izbriši donju liniju a odkomentariši gornju ako hoces čiste podatke bez godina
    return pd.Series(rezultati, index=list(aop_vrednosti_po_godinama.keys())) 



# ------------------Primjer dodjele vrednosti varijabli--------------------
# Promeni vrednosti AOP za razlicite god (039,044,044)

Kratkorocna_potrazivanja = vrednosti_iz_excela('bilans_stanja.xlsx', {2021: '039', 2022: '044', 2023: '044'}) 
print(Kratkorocna_potrazivanja)
