import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

INPUT_FILE = "on_corridor.csv"

df = pd.read_csv(INPUT_FILE, dtype={"Timestamp": str})

# Keep digits, colon, hyphen, and whitespace in the timestamp field.
df["Timestamp"] = df["Timestamp"].str.replace(
    r"[^0-9:\-\s]", "", regex=True
)

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    format="%d-%m-%Y %H:%M",
    dayfirst=True,
    errors="coerce",
)

df = df.dropna(subset=["Timestamp"])
df = df.sort_values("Timestamp")

main_date = df["Timestamp"].dt.date.mode()[0]
df = df[df["Timestamp"].dt.date == main_date]

print("DATA CLEANED SUCCESSFULLY")
print(f"Selected Measurement Date: {main_date}")
print("Data Preview:")
print(df.head())

df_grouped = df.groupby(
    ["Location", "Timestamp"],
    as_index=False
).mean(numeric_only=True)

parameters = [
    "Temperature (°C)",
    "Humidity (%)",
    "Pressure (hPa)",
    "Gas (ADC)",
]

# Save one plot for each parameter and location.
for param in parameters:
    for loc, subdf in df_grouped.groupby("Location"):
        plt.figure(figsize=(10, 4))
        plt.plot(
            subdf["Timestamp"],
            subdf[param],
            marker="o",
            linewidth=2,
        )

        plt.title(f"{param} over Time ({loc}) — {main_date}")
        plt.xlabel("Time (HH:MM)")
        plt.ylabel(param)
        plt.grid(True, alpha=0.3)

        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.set_xlim(
            subdf["Timestamp"].min(),
            subdf["Timestamp"].max(),
        )

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        output_name = (
            f"{param.replace(' ', '_').replace('(', '').replace(')', '')}"
            f"_{loc}_{main_date}.png"
        )

        if os.path.exists(output_name):
            os.remove(output_name)

        plt.savefig(output_name, dpi=300)
        plt.close()
        print(f"Saved: {output_name}")

# Save combined plots for all locations.
for param in parameters:
    plt.figure(figsize=(10, 4))

    for loc, subdf in df_grouped.groupby("Location"):
        plt.plot(
            subdf["Timestamp"],
            subdf[param],
            label=loc,
            linewidth=2,
        )

    plt.title(f"{param} over Time (All Locations) — {main_date}")
    plt.xlabel("Time (HH:MM)")
    plt.ylabel(param)
    plt.legend()
    plt.grid(True, alpha=0.3)

    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.set_xlim(
        df_grouped["Timestamp"].min(),
        df_grouped["Timestamp"].max(),
    )

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_name = (
        f"{param.replace(' ', '_').replace('(', '').replace(')', '')}"
        f"_All_Locations_{main_date}.png"
    )

    if os.path.exists(output_name):
        os.remove(output_name)

    plt.savefig(output_name, dpi=300)
    plt.close()
    print(f"Saved combined plot: {output_name}")

# Correlation matrix.
corr = df_grouped[parameters].corr()
print("\nCorrelation Matrix:")
print(corr)

# Linear regression for humidity prediction.
X = df_grouped[["Temperature (°C)", "Pressure (hPa)"]]
y = df_grouped["Humidity (%)"]

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)

r2 = r2_score(y, y_pred)
rmse = mean_squared_error(y, y_pred) ** 0.5

print("\nRegression Results:")
print(f"R² Score: {r2:.3f}")
print(f"RMSE: {rmse:.3f}")
print(
    "Equation: Humidity = "
    f"{model.coef_[0]:.3f}*Temp + "
    f"{model.coef_[1]:.3f}*Pressure + "
    f"{model.intercept_:.3f}"
)

# Predict humidity for new values.
new_data = pd.DataFrame(
    {
        "Temperature (°C)": [22.5, 23.0, 25.0, 28.0],
        "Pressure (hPa)": [987.5, 987.8, 988.0, 989.0],
    }
)

predicted_humidity = model.predict(new_data)
new_data["Predicted Humidity (%)"] = predicted_humidity

print("\nPredicted Humidity for New Values:")
print(new_data)

output_file = "predicted_humidity.csv"

if os.path.exists(output_file):
    os.remove(output_file)

new_data.to_csv(output_file, index=False)
print(f"Predictions saved to '{output_file}'")

# Air-quality boxplot by location.
if df_grouped["Location"].nunique() > 1:
    plt.figure(figsize=(8, 5))
    df_grouped.boxplot(
        column="Gas (ADC)",
        by="Location",
        grid=False,
    )

    plt.title(f"Air Quality (Gas ADC) Across Locations — {main_date}")
    plt.suptitle("")
    plt.xlabel("Location")
    plt.ylabel("Gas (ADC)")
    plt.tight_layout()

    output_name = f"AirQuality_Boxplot_{main_date}.png"

    if os.path.exists(output_name):
        os.remove(output_name)

    plt.savefig(output_name, dpi=300)
    plt.close()
    print(f"Saved: {output_name}")
else:
    print("Only one location found — skipping boxplot.")

# Actual versus predicted humidity scatter plot.
plt.figure(figsize=(7, 5))
plt.scatter(y, y_pred)
plt.plot(
    [y.min(), y.max()],
    [y.min(), y.max()],
    linewidth=2,
)

plt.xlabel("Actual Humidity (%)")
plt.ylabel("Predicted Humidity (%)")
plt.title(f"Linear Regression Fit (R² = {r2:.3f})")
plt.grid(True, alpha=0.3)
plt.tight_layout()

output_name = f"Linear_Regression_Fit_{main_date}.png"
plt.savefig(output_name, dpi=300)
plt.close()

print(f"Saved: {output_name}")
