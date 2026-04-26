import random
import pandas as pd
import numpy as np
import math

def generate_data():
    data = []
    for i in range(1, 18):
        d = {
            "zone": i,
            "traffic": random.randint(0, 100),
            "air_quality": random.randint(0, 300),
            "energy": random.randint(0, 500)
        }
        data.append(d)
    data.append({"zone": 18, "traffic": 0, "air_quality": 50, "energy": 100})
    data.append({"zone": 19, "traffic": 90, "air_quality": 280, "energy": 450})
    data.append({"zone": 20, "traffic": 10, "air_quality": 250, "energy": 480})

    return data

def classify(record):
    if record["air_quality"] > 200 or record["traffic"] > 80:
        return "High Risk"
    elif record["energy"] > 400:
        return "Energy Critical"
    elif record["traffic"] < 30 and record["air_quality"] < 100:
        return "Safe Zone"
    else:
        return "Moderate"

def risk_score(record):
    score = (record["traffic"] * 0.3 +
             record["air_quality"] * 0.4 +
             record["energy"] * 0.3)
    return round(score, 2)

def custom_sort(data):
    return sorted(data, key=lambda x: x["traffic"], reverse=True)

def detect_patterns(df):
    threshold = df["risk_score"].mean()
    multi_risk = df[(df["risk_score"] > threshold) & (df["air_quality"].diff() > 0)]
    stability = np.var(df["traffic"]) < 500
    clusters = []
    temp = []
    for i in range(len(df)):
        if df.iloc[i]["risk_score"] > threshold:
            temp.append(df.iloc[i]["zone"])
        else:
            if len(temp) >= 2:
                clusters.append(temp)
            temp = []

    return multi_risk, stability, clusters

def main():
    roll_no = 646
    data = generate_data()
    data = custom_sort(data)
    for d in data:
        d["category"] = classify(d)
        d["risk_score"] = risk_score(d)
        d["sqrt_risk"] = round(math.sqrt(d["risk_score"]), 2)

    df = pd.DataFrame(data)

    print("\n--- City Data ---")
    print(df)

    arr = df[["traffic", "air_quality", "energy"]].values
    mean_values = np.mean(arr, axis=0)
    print("\nMean Values:", mean_values)

    sorted_data = sorted(data, key=lambda x: x["risk_score"], reverse=True)
    print("\nTop 3 Risk Zones:")
    for i in range(3):
        print(sorted_data[i])

    risks = df["risk_score"]
    print("\nRisk Tuple:", (risks.max(), risks.mean(), risks.min()))

    multi_risk, stability, clusters = detect_patterns(df)

    print("\nMulti-factor Risk Zones:")
    print(multi_risk[["zone", "risk_score"]])
    print("\nStability:", "Stable" if stability else "Unstable")
    print("Clusters:", clusters)

    avg = risks.mean()

    if avg < 100:
        decision = "City Stable"
    elif avg < 150:
        decision = "Moderate Risk"
    elif avg < 200:
        decision = "High Alert"
    else:
        decision = "Critical Emergency"
    print("\nFinal Decision:", decision)
    print("\nSmart City Definition:")
    print("A smart city focuses on protecting the environment by reducing pollution, managing energy efficiently, and using data to maintain a healthy and sustainable ecosystem.")

main()