import math
import argparse

parser = argparse.ArgumentParser(description='Loan Calculator')
parser.add_argument('--type', type=str, help='Type of loan payment')
parser.add_argument('--payment', type=float, help='monthly payment')
parser.add_argument('--principal', type=int, help='loan principal')
parser.add_argument('--periods', type=int, help='number of months')
parser.add_argument('--interest', type=float, help='interest rate')

args = parser.parse_args()

a_type = args.type
a_payment = args.payment
a_principal = args.principal
a_periods = args.periods
a_interest = args.interest

# проверки вводимых данных
def check_type(input_type, input_payment, input_principal,
               input_periods, input_interest) -> bool:
    if input_type not in ["annuity", "diff"]:
        print("Incorrect parameters")
        return False
    elif input_type == "diff":
        if input_payment is not None:
            print("Incorrect parameters")
            return False
        elif input_interest is None or input_principal is None or input_periods is None:
             print("Incorrect parameters")
             return False
        elif input_principal < 0 or input_periods < 0 or input_interest < 0:
            print("Incorrect parameters")
            return False
    return True

# расчет количества месяцев/лет платежей
def periods(payment, principal, interest):
    i = interest / (12 * 100)
    months = math.ceil(math.log( payment / (payment - i * principal), 1 + i))
    if months <= 0:
        print("Incorrect parameters")
    else:
        years = math.floor(months / 12)
        if months % 12 == 0:
            print("It will take", int(years), "years to repay this loan!")
        else:
            leaf_months = months - years * 12
            print("It will take", int(years), "years and", int(leaf_months), "months to repay this loan!")
        sum_overpay = round(payment * months - principal)
        print(f"Overpayment = {sum_overpay}")

# расчет основной суммы платежа
def principals(payment, period, interest):
    i = interest / (12 * 100)
    principal = math.floor(
        payment * ((1 + i) ** period - 1) / (i * (1 + i) ** period))  # округление в меньшую сторону
    print(f"Your loan principal = {principal}!")
    sum_overpay = round(payment * period - principal)
    print(f"Overpayment = {sum_overpay}")

# расчет ежемесячного платежа
# аннуитет
def annuity_payments(principal, period, interest):
    i = interest / (12 * 100)
    payment = math.ceil(
        principal * (i * (1 + i) ** period) / ((1 + i) ** period - 1))  # округление в большую сторону
    print(f"Your annuity payment = {payment}!")

# расчет ежемесячного платежа
# дифференцированный
def diff_payments(principal, period, interest):
    i = interest / (12 * 100)
    for m in range(1, period + 1):
        payment = math.ceil(principal / period + i * (principal - ((principal * (m - 1)) / period)))
        print(f"Month {m}: payment is {payment}")

# расчет переплаты
def diff_overpayment(principal, period, interest):
    i = interest / (12 * 100)
    sum_payment = 0
    for m in range(1, period + 1):
        payment = math.ceil(principal / period + i * (principal - ((principal * (m - 1)) / period)))
        sum_payment += payment
    sum_overpayment = sum_payment - principal
    print(f"Overpayment = {sum_overpayment}")



if check_type(a_type, a_payment, a_principal, a_periods, a_interest):
    if a_type.lower() == "annuity":
        if args.periods is None and a_payment is not None and a_principal is not None and a_interest is not None:
            periods(a_payment, a_principal, a_interest)
        elif args.payment is None and a_principal is not None and a_periods is not None and a_interest is not None:
            annuity_payments(a_principal, a_periods, a_interest)
        elif args.principal is None and a_payment is not None and a_periods is not None and a_interest is not None:
            principals(a_payment, a_periods, a_interest)
        else:
            print("Incorrect parameters")
    elif a_type.lower() == "diff":
            diff_payments(a_principal, a_periods, a_interest)
            print("")
            diff_overpayment(a_principal, a_periods, a_interest)