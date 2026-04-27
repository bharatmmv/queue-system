import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_crowd():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT time FROM queue")
    data = cur.fetchall()

    conn.close()

    if len(data) < 5:
        return {"message": "Not enough data"}

    hours = []
    counts = {}

    for row in data:
        hour = int(row[0][11:13])
        counts[hour] = counts.get(hour, 0) + 1

    for h, c in counts.items():
        hours.append([h, c])

    hours = np.array(hours)
    X = hours[:, 0].reshape(-1, 1)
    y = hours[:, 1]

    model = LinearRegression()
    model.fit(X, y)

    pred = model.predict([[18]])  # example: 6PM

    return {
        "predicted_customers_at_6PM": int(pred[0])
    }