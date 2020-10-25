# -*- utf-8 -*-

# Created: 24th October 2020
# Author: Jerome Wynne
# Summary: a function for computing monthly net pay over one financial year.

def monthly_summary(gross_annual_salary: float, to_pension: float):

    # compute cumulative salary by month
    gross_monthly_salary = gross_annual_salary/12.
    cum_gross_salary = [n*gross_monthly_salary for n in range(1, 13)]
    [income_tax(c) for c in cum_gross_salary]
    pass

def yearly_summary(gross_annual_salary: float, to_pension: float):

    ni = ni_contribution(gross_annual_salary)
    plan2 = plan_2_contribution(gross_annual_salary)
    postgrad = postgraduate_contribution(gross_annual_salary)
    pen_con = pension_contribution(gross_annual_salary, to_pension)
    salary_less_pension = gross_annual_salary - pen_con
    tax = income_tax(salary_less_pension)

    summary_dct = {
        'Gross annual salary': gross_annual_salary,
        'Pension': pen_con,
        'Tax': tax,
        'National Insurance': ni,
        'Plan 2 loan': plan2,
        'Postgraduate loan': postgrad,
        'Net annual salary': gross_annual_salary - sum([pen_con, tax,
                                                        ni, plan2, postgrad])
    }
    return summary_dct

    return (salary_less_pension -
            income_tax(salary_less_pension) -
            ni_contribution(salary_less_pension) -
            plan_2_contribution(salary_less_pension) -
            postgraduate_contribution(salary_less_pension))

def income_tax(gross_annual_salary: float):
    # ref: https://www.moneyadviceservice.org.uk/en/articles/tax-and-national-insurance-deductions
    tax_bands = [(0, 12500, 0.),
                 (12500, 50000, 0.2),
                 (50000, 150000, 0.4),
                 (150000, float('inf'), 0.45)] # 2020/21 income tax bands
    return(marginal_tax(gross_annual_salary, tax_bands))

def ni_contribution(gross_annual_salary: float):
    # ref: https://www.moneyadviceservice.org.uk/en/articles/tax-and-national-insurance-deductions
    ni_bands = [(0, 183.*52, 0.),
                (183.*52, 962.*52, 0.12),
                (962.*52, float('inf'), 0.02)] # 2020/21 NI contribution bands
    return(marginal_tax(gross_annual_salary, ni_bands))

def marginal_tax(gross_annual_salary: float, tax_bands: list):
    gas = gross_annual_salary
    tax_by_band = [b[2]*(max(b[0], min(gas, b[1])) - b[0]) for b in tax_bands]
    return(sum(tax_by_band))

def pension_contribution(gross_annual_salary: float,
                                        frac_contributed:float):
    return(gross_annual_salary*frac_contributed)

def plan_2_contribution(gross_annual_salary: float):
    # ref: https://www.gov.uk/repaying-your-student-loan/what-you-pay
    plan_2_bands = [(0, 2214.*12, 0.),
                    (2214.*12, float('inf'), 0.09)]
    return(marginal_tax(gross_annual_salary, plan_2_bands))

def postgraduate_contribution(gross_annual_salary: float):
    # ref: https://www.gov.uk/repaying-your-student-loan/what-you-pay
    postgrad_bands = [(0, 1750.*12, 0.),
                      (1750.*12, float('inf'), 0.06)]
    return(marginal_tax(gross_annual_salary, postgrad_bands))
