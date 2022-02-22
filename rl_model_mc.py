import streamlit as st
import random
from  matplotlib import pyplot as plt
import pandas as pd
import numpy as np

st.title('Reversed Logistics Model - Monte Carlo Simulation')

def total_net_benefits(net_benefits, periods, invest):    
    
    tnb = - invest

    for i in range(periods):
        tnb += net_benefits
    return tnb

st.write('General Parameters')
num_sim = int(st.number_input('Number of simulations'))
labor_cost = st.number_input('Labor cost')
years = int(st.number_input('Time span in years')) # years, generally the period for all times considered in this model
units_min = int(st.number_input('Estimated minimum amount of units'))
units_mode = int(st.number_input('Estimated most likely amount of units'))
units_max = int(st.number_input('Estimated maximum amount of units'))

st.write('Benefits - Reusable Material')
savings_unit_min = int(st.number_input('Estimated minimum saving per reused unit (can be negative)'))
savings_unit_mode = int(st.number_input('Estimated most likely saving per reused unit'))
savings_unit_max = int(st.number_input('Estimated maximum saving per reused unit'))

st.write('Benefits - More Business')
add_projects_min = int(st.number_input('Estimated minimum number of additional projects'))
add_projects_mode = int(st.number_input('Estimated most likely number of additional projects'))
add_projects_max = int(st.number_input('Estimated maximum number of additional projects'))

cf_min = int(st.number_input('Estimated minimum average cash flow of additional projects'))
cf_mode = int(st.number_input('Estimated most likely average cash flow of additional projects'))
cf_max = int(st.number_input('Estimated maximum average cash flow of additional projects'))

st.write('Cost  - Opex - Recycling Process')
process_min = int(st.number_input('Estimated minimum cost of process per unit'))
process_mode = int(st.number_input('Estimated most likely cost of process per unit'))
process_max = int(st.number_input('Estimated maximum cost of process per unit'))

st.write('Cost  - Opex - Transportation')
cost_km_unit_min = int(st.number_input('Estimated minimum cost of transportation per km and unit'))
cost_km_unit_mode = int(st.number_input('Estimated most likely cost of transportation per km and unit'))
cost_km_unit_max = int(st.number_input('Estimated maximum cost of transportation per km and unit'))

km_min = int(st.number_input('Estimated minimum km per year'))
km_mode = int(st.number_input('Estimated most likely km per year'))
km_max = int(st.number_input('Estimated maximum km per year'))

st.write('Cost  - Capex')
hours_min = int(st.number_input('Estimated minimum development hours'))
hours_mode = int(st.number_input('Estimated most development hours'))
hours_max = int(st.number_input('Estimated maximum development hours'))

invest_min = int(st.number_input('Estimated minimum development investment'))
invest_mode = int(st.number_input('Estimated most development investment'))
invest_max = int(st.number_input('Estimated maximum development investment'))

scenarios_tnb = []

for i in range(num_sim):
    
    units = random.triangular(units_min, units_mode, units_max)
    

    # Benefits

        # reusable material
    savings_per_unit = random.triangular(savings_unit_min, savings_unit_mode, savings_unit_max)

    material_savings = units* savings_per_unit

        # more business
    add_projects = random.triangular(add_projects_min, add_projects_mode, add_projects_max)

    cf_per_project = random.triangular(cf_min, cf_mode, cf_max)

    add_business = add_projects * cf_per_project

    benefits = material_savings + add_business

    # Cost

        # Opex

            # recycling process
    cost_per_unit = random.triangular(process_min, process_mode, process_max)

    recycling_cost = cost_per_unit * units

            # transportation
    cost_per_km_and_unit = random.triangular(cost_km_unit_min, cost_km_unit_mode, cost_km_unit_max)

    km = random.triangular(km_min, km_mode, km_max)

    transport_cost = cost_per_km_and_unit * km

    opex = recycling_cost + transport_cost

        # net benefits

    net_benefits = benefits - opex
        # Capex

    dev_hours = random.triangular(hours_min, hours_mode, hours_max)

    add_dev_invest = random.triangular(invest_min, invest_mode, invest_max)

    capex = dev_hours*labor_cost + add_dev_invest

    tnb = total_net_benefits(net_benefits, years, capex)
    scenarios_tnb.append(tnb)

fig, ax = plt.subplots(figsize=(15,8))
ax.hist(scenarios_tnb, bins=100)
plt.xlabel('Total Net Benefits')
plt.ylabel('Occurence')
plt.title('Distribution of Total Net Benefits Scenarios')
plt.show()
st.pyplot(fig)

df_scenarios = pd.DataFrame(scenarios_tnb)
st.write(df_scenarios.describe())