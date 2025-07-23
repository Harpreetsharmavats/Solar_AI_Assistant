def calculate_roi(data):
    area = data["usable_area_m2"]
    panel_area = 1.6  # square meters per panel
    efficiency = 0.18  # 18%
    sunlight_hours_per_year = 1500
    panel_cost_inr = 20750
    savings_per_kwh_inr = 10

    num_panels = int(area / panel_area)
    annual_energy = num_panels * efficiency * sunlight_hours_per_year
    total_cost_inr = num_panels * panel_cost_inr
    annual_savings_inr = annual_energy * savings_per_kwh_inr
    payback = total_cost_inr / annual_savings_inr if annual_savings_inr > 0 else 0

    return {
        "Number of Panels": num_panels,
        "Estimated Annual Output (kWh)": round(annual_energy, 2),
        "Estimated Installation Cost (INR)": round(total_cost_inr, 2),
        "Annual Savings (INR)": round(annual_savings_inr, 2),
        "Payback Period (Years)": round(payback, 1),
        "Recommended Panel Type": "Monocrystalline"
    }
