import pandas as pd
df=pd.read_csv("data/Matrix_Database_2020_2024.csv", sep=";")
print(df.head())
print("Dimensão do dataset:", df.shape)
events_per_year = df.groupby("Calender_Year").size()
print(events_per_year)
df["Event_Date"]=pd.to_datetime(df["Event_Date"], dayfirst=True)
df=df.sort_values("Event_Date")
print(df[["Event_Date"]].head())

import matplotlib.pyplot as plt
events_per_year.plot(kind="bar")

plt.title("Number of Events per Year")
plt.xlabel("Year")
plt.ylabel("Number of Events")
plt.show()