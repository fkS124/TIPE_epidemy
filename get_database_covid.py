import pandas as pd


# Définir les dates de début et de fin (format : YYYY-MM-DD)
start_date = input("Entrez la date de début : ")
end_date = input("Entrez la date de fin : ")

# URL de l'API de Our World in Data
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'

# Télécharger les données
df = pd.read_csv(url)

# Filtrer les données pour la France et la période spécifiée
df['date'] = pd.to_datetime(df['date'])
mask = (df['location'] == 'France') and (df['date'] >= start_date) and (df['date'] <= end_date)
france_data = df.loc[mask]

# Récupérer abscisse et ordonnée
dates = france_data['date']
cumulative_cases = france_data['total_cases']

# Sauvegarder les données dans un fichier texte
with open(f"./Data/cas_covid_cumule_{start_date}_{end_date}.txt", 'w') as file:
    file.write("Date\tNombre de cas cumulés\n")
    for date, cases in zip(dates, cumulative_cases):
        file.write(f"{date.strftime('%Y-%m-%d')}\t{int(cases)}\n")

print(f"Le fichier suivant a été créé : Data/cas_covid_cumule_{start_date}_{end_date}.txt")
