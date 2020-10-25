# -*- utf-8 -*-

# Created: 24th October 2020
# Author: Jerome Wynne
# Summary: a function for computing monthly net pay over one financial year.
# TODO:
#   write tests

from itertools import accumulate

def monthly_summary(gross_annual_salary: float, to_pension: float):
    ''' Computes deductions from gross monthly salary for UK in 20/21

    Args:
        gross_annual_salary: g.a.s. in GBP.
        to_pension: fraction of salary kicked to pension.

    Returns:
        dict: dict of lists containing monthly pay/tax/contribution values.
    '''
    gross_monthly_salary = gross_annual_salary/12.
    cum_gs = [n*gross_monthly_salary for n in range(1, 13)]
    gs = _diff_but_first(cum_gs)
    pc = [pension_contribution(gross_monthly_salary, to_pension)]*12
    cum_pc = accumulate(pc)
    cum_tx = [income_tax(gs - pc) for gs, pc in zip(cum_gs, cum_pc)]
    tx = _diff_but_first(cum_tx)
    ni = [ni_contribution(gross_monthly_salary)]*12
    p2 = [plan_2_contribution(gross_monthly_salary)]*12
    pg = [postgraduate_contribution(gross_monthly_salary)]*12

    summary_dct = {
        'Gross monthly salary':gs,
        'National Insurance': ni,
        'Net monthly salary': [vgs - sum([vni, vpc, vp2, vpg, vtx]) for
                                           vgs, vni, vpc, vp2, vpg, vtx in
                                                zip(gs, ni, pc, p2, pg, tx)],
        'Pension': pc,
        'Plan 2 loan': p2,
        'Postgraduate loan': pg,
        'Tax': tx
    }

    # round the values
    for key in summary_dct.keys():
        summary_dct[key] = [round(v, 2) for v in summary_dct[key]]

    return(summary_dct)

def _diff_but_first(lst: list):
    return [lst[0]] + [lst[j] - lst[j-1] for j in range(1, 12)]

def yearly_summary(gross_annual_salary: float, to_pension: float):

    gross_monthly_salary = gross_annual_salary/12.
    ni = ni_contribution(gross_monthly_salary)*12
    plan2 = plan_2_contribution(gross_monthly_salary)*12
    postgrad = postgraduate_contribution(gross_monthly_salary)*12
    pen_con = pension_contribution(gross_annual_salary, to_pension)
    gs_less_pension = gross_annual_salary - pen_con
    tax = income_tax(gs_less_pension)

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

def income_tax(gross_annual_salary: float):
    # ref: https://www.moneyadviceservice.org.uk/en/articles/tax-and-national-insurance-deductions
    tax_bands = [(0, 12500, 0.),
                 (12500, 50000, 0.2),
                 (50000, 150000, 0.4),
                 (150000, float('inf'), 0.45)] # 2020/21 income tax bands
    return(marginal_tax(gross_annual_salary, tax_bands))

def ni_contribution(gross_monthly_salary: float):
    # ref: https://www.moneyadviceservice.org.uk/en/articles/tax-and-national-insurance-deductions
    ni_bands = [(0, 792., 0.),
                (792., 4167., 0.12),
                (4167., float('inf'), 0.02)] # 2020/21 NI contribution bands
    return(marginal_tax(gross_monthly_salary, ni_bands))

def marginal_tax(gross_annual_salary: float, tax_bands: list):
    gas = gross_annual_salary
    tax_by_band = [b[2]*(max(b[0], min(gas, b[1])) - b[0]) for b in tax_bands]
    return(sum(tax_by_band))

def pension_contribution(gross_annual_salary: float,
                                        frac_contributed:float):
    return(gross_annual_salary*frac_contributed)

def plan_2_contribution(gross_monthly_salary: float):
    # ref: https://www.gov.uk/repaying-your-student-loan/what-you-pay
    plan_2_bands = [(0, 2214., 0.),
                    (2214., float('inf'), 0.09)]
    return(marginal_tax(gross_monthly_salary, plan_2_bands))

def postgraduate_contribution(gross_monthly_salary: float):
    # ref: https://www.gov.uk/repaying-your-student-loan/what-you-pay
    postgrad_bands = [(0, 1750., 0.),
                      (1750., float('inf'), 0.06)]
    return(marginal_tax(gross_monthly_salary, postgrad_bands))
