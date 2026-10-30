print("=== AutoRAY Vehicle Cost Calculator ===")

car_price = float(input("Vehicle price: $"))
years = int(input("How many years will you own it? "))
gas_per_year = float(input("Gas cost per year: $"))
maintenance_per_year = float(input("Maintenance cost per year: $"))
insurance_per_year = float(input("Insurance cost per year: $"))

gas_total = gas_per_year * years
maintenance_total = maintenance_per_year * years
insurance_total = insurance_per_year * years

operating_cost = gas_total + maintenance_total + insurance_total
total_cost = car_price + operating_cost
average_per_year = total_cost / years

print("\n=== Your Cost Report ===")
print("Operating costs: $", round(operating_cost, 2))
print("Total ownership cost: $", round(total_cost, 2))
print("Average cost per year: $", round(average_per_year, 2))
