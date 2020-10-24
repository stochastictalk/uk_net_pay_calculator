# -*- utf-8 -*-

# Created: 24th October 2020
# Author: Jerome Wynne
# Summary: a function for computing monthly net pay over one financial year.

import numpy as np

def uk_net_pay_calculator(gross_annual_salary:float):
    # For 2021
    # Tax year runs from 6 April to 5 April
    # Personal allowance of £12,500
    #   For the first £12,500 no tax is paid
    #   Only earnings above this sum are taxed
    # NI threshold is £8,632
    #
    # Income tax
    # [0, 12500]: 0
    # (12500, 50000]: 0.2
    # (50000, 150000]: 0.4
    # (150000, inf): 0.45

    # National insurance
    # Employees pay Class National Insurance Contributions
    # You pay NI contributions if you earn more than £183 a week
    # 12% of earnings > £183 and <= £962 a week
    # 2% of earnings > £962
    pass

def get_income_tax(gross_annual_salary: float):
    tax_bands = [(0, 12500, 0.),
                 (12500, 50000, 0.2),
                 (50000, 150000, 0.4),
                 (150000, np.inf, 0.45)] # 2020/21 income tax bands
    return(get_marginal_tax(gross_annual_salary, tax_bands))

def get_ni_contribution(gross_annual_salary: float):
    ni_bands = [(0, 183.*52, 0.),
                (183.*52, 962.*52, 0.12),
                (962.*52, np.inf, 0.02)] # 2020/21 NI contribution bands
    return(get_marginal_tax(gross_annual_salary, ni_bands))

def get_marginal_tax(gross_annual_salary: float, tax_bands: list):
    gas = gross_annual_salary
    tax_by_band = [b[2]*(max(b[0], min(gas, b[1])) - b[0]) for b in tax_bands]
    return(sum(tax_by_band))
