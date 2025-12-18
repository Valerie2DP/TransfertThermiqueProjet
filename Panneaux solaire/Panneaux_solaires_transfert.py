import csv
from datetime import datetime, timedelta

def extract_pvwatts_kwh(file_path, start_date, end_date):
    """
    Extrait l'output d'énergie en kWh entre deux dates
    
    Inputs:
        file_path (str): Path to the CSV file
        start_date (str): Start date in 'MM-DD' format
        end_date (str): End date in 'MM-DD' format
    """
    
    # On décide la date de début et de fin
    start_month, start_day = map(int, start_date.split('-'))
    end_month, end_day = map(int, end_date.split('-'))
    
    total_kwh = 0.0
    data_started = False
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            # Skip empty rows
            if not row:
                continue
                
            # On cherche le début des données
            if row[0] == 'Month' and row[1] == 'Day' and row[2] == 'Hour':
                data_started = True
                continue
                
            if data_started and len(row) >= 12:
                try:
                    month = int(row[0])
                    day = int(row[1])
                    hour = int(row[2])
                    
                    # W à kW
                    ac_output_w = float(row[11])
                    ac_output_kw = ac_output_w / 1000.0  
                    
                    # Check if date is within the specified range (considering year wrap-around)
                    date_in_range = False
                    
                    # Handle dates that cross year boundary (Dec 21 to Mar 5)
                    if start_month > end_month:  # Crosses year boundary (e.g., Dec to Mar)
                        if (month == 12 and day >= start_day) or \
                           (month == 1 or month == 2) or \
                           (month == 3 and day <= end_day):
                            date_in_range = True
                    else:  # Normal range within same year
                        if (month > start_month or (month == start_month and day >= start_day)) and \
                           (month < end_month or (month == end_month and day <= end_day)):
                            date_in_range = True
                    
                    if date_in_range:
                        # Add kW (since it's hourly data, each value is kWh for that hour)
                        total_kwh += ac_output_kw
                        
                except (ValueError, IndexError) as e:
                    # Skip rows that can't be parsed
                    continue
    
    return total_kwh



file_path = r'3117.csv'


# kwH entre 21 décembre et 5 mars
total_kwh = extract_pvwatts_kwh(file_path, '12-21', '03-05')

print(f"Total AC System Output between December 21st and March 5th: {total_kwh:.2f} kWh")
print(f"Total AC System Output: {total_kwh:.0f} kWh")

# Sauvegarde des données
with open('pvwatts_results.txt', 'w') as f:
    f.write(f"Total AC System Output between December 21st and March 5th: {total_kwh:.2f} kWh\n")
    f.write(f"Total AC System Output: {total_kwh:.0f} kWh")