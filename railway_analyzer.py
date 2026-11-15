# Railway Reservation Analyzer
# Reads bookings.csv and shows bookings per train and revenue per train.

import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "bookings.csv"


def load_data(file_name):
    """Read the CSV and return only the valid rows (valid fare)."""
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        print("Error: File '" + file_name + "' not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: File '" + file_name + "' is empty.")
        return None

    # Fare must be a number. Anything else becomes NaN.
    df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce")

    valid_rows = []
    for i in range(len(df)):
        row = df.iloc[i]
        if pd.isna(row["Fare"]):
            print("Warning: Row with PNR " + str(row["PNR"]) + " skipped - invalid fare.")
        else:
            valid_rows.append(i)

    df = df.iloc[valid_rows]
    print("Valid records analysed: " + str(len(df)))
    return df


def bookings_per_train(df):
    """Count bookings per train, plus Confirmed/Waiting/Cancelled split."""
    counts = df.groupby("Train").size()

    print("\nBookings per train:")
    for train in counts.index:
        print(train + " : " + str(counts[train]))
    print("Total bookings: " + str(len(df)))

    # Status-wise count for each train
    print("\nStatus-wise count:")
    status_counts = df.groupby(["Train", "Status"]).size()
    for train in counts.index:
        confirmed = status_counts.get((train, "Confirmed"), 0)
        waiting = status_counts.get((train, "Waiting"), 0)
        cancelled = status_counts.get((train, "Cancelled"), 0)
        print(train + " -> Confirmed: " + str(confirmed) +
              ", Waiting: " + str(waiting) +
              ", Cancelled: " + str(cancelled))

    # Bar chart
    plt.bar(counts.index, counts.values, color="skyblue")
    plt.title("Bookings per Train")
    plt.xlabel("Train")
    plt.ylabel("Number of Bookings")
    plt.show()


def revenue_per_train(df):
    """Total fare per train, only for Confirmed tickets."""
    confirmed = df[df["Status"] == "Confirmed"]
    revenue = confirmed.groupby("Train")["Fare"].sum()

    print("\nRevenue per train (Confirmed only):")
    for train in revenue.index:
        print(train + " : Rs. " + str(int(revenue[train])))
    print("Total confirmed revenue: Rs. " + str(int(revenue.sum())))

    # Bar chart
    plt.bar(revenue.index, revenue.values, color="lightgreen")
    plt.title("Revenue per Train (Confirmed only)")
    plt.xlabel("Train")
    plt.ylabel("Revenue (Rs.)")
    plt.show()


def main():
    df = load_data(FILE_NAME)
    if df is None:
        return  # file problem, stop the program nicely

    while True:
        print("\n===== Railway Reservation Analyzer =====")
        print("1. Bookings per train")
        print("2. Revenue per train (Confirmed only)")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            bookings_per_train(df)
        elif choice == "2":
            revenue_per_train(df)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")


main()
