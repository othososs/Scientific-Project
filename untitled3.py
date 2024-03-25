import pandas as pd
import matplotlib.pyplot as plt

# Supposons que votre DataFrame s'appelle df et que vous l'ayez déjà groupé par mk id

# Durée moyenne des visites par client
average_time_spent = grouped_by_client['time spent per visit'].mean()

# Taux de rebond par client
total_sessions = grouped_by_client['session number'].count()
single_page_sessions = grouped_by_client.apply(lambda x: (x['exit pages'].count() == 1).sum())
bounce_rate = (single_page_sessions / total_sessions) * 100

# Distribution des sessions par jour de la semaine
df['day_of_week'] = df['date'].dt.dayofweek
sessions_by_day = grouped_by_client['day_of_week'].value_counts().unstack(fill_value=0)

# Graphiques
plt.figure(figsize=(12, 6))

# Durée moyenne des visites par client
plt.subplot(1, 3, 1)
average_time_spent.plot(kind='bar', color='skyblue')
plt.title('Durée moyenne des visites')
plt.xlabel('Client ID')
plt.ylabel('Durée moyenne (en secondes)')

# Taux de rebond par client
plt.subplot(1, 3, 2)
bounce_rate.plot(kind='bar', color='salmon')
plt.title('Taux de rebond')
plt.xlabel('Client ID')
plt.ylabel('Taux de rebond (%)')

# Distribution des sessions par jour de la semaine
plt.subplot(1, 3, 3)
sessions_by_day.plot(kind='bar', stacked=True)
plt.title('Distribution des sessions par jour de la semaine')
plt.xlabel('Client ID')
plt.ylabel('Nombre de sessions')
plt.legend(['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'], loc='upper right')

plt.tight_layout()
plt.show()
