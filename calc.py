from json_parser import load_json, parse


class Loan:

    _important_params = ['interest', 'loan amount', 'term']

    def __init__(self, params: dict):
        Loan._check(params)
        self.interest = Loan._interest_to_float(params['interest'])
        self.month_interest = self.interest / 12
        self.amount = params['loan amount']
        self._term = params['term']
        self._term_type = params['term type'] if 'term type' in params else 'year'
        self.term_in_months = Loan._term_to_month(self._term, self._term_type)
        self.repayment_method = params['repayment method'] if 'repayment method' in params else 'annuity'

        if self.repayment_method == 'annuity':
            N = self.term_in_months
            self.monthly_payment = self.amount * (self.month_interest +
                                                  self.month_interest /
                                                  ((1 + self.month_interest) ** N - 1))
        else:
            self.debt_payment = self.amount / self.term_in_months

        self._all_payments_table = None

    def _interest_to_float(interest):
        if interest >= 1:
            return interest / 100
        else:
            return interest

    def _term_to_month(term, ttype):
        if ttype == 'year':
            return term * 12
        elif ttype == 'month':
            return term
        else:
            raise ValueError('Unknown term type')

    def _check(params):
        check = True
        for p in Loan._important_params:
            check *= p in params
        if not check:
            raise ValueError(f'I cant find one of this params: {Loan._important_params}')

    def _annuity_payment(self, amount):
        if self.repayment_method != 'annuity':
            raise ValueError('Use .diff_payment() function')
        payment = self.monthly_payment
        interest_payment = amount * self.month_interest
        debt_payment = payment - interest_payment
        balance = amount - debt_payment
        balance = balance if balance > 1e-3 else 0
        return amount, payment, interest_payment, debt_payment, balance

    def _diff_payment(self, amount):
        if self.repayment_method == 'annuity':
            raise ValueError('Use .annuity_payment() function')
        debt_payment = self.debt_payment
        interest_payment = amount * self.month_interest
        payment = debt_payment + interest_payment
        balance = amount - debt_payment
        balance = balance if balance > 1e-3 else 0
        return amount, payment, interest_payment, debt_payment, balance

    def _eval_func(self):
        if self.repayment_method == 'annuity':
            return self._annuity_payment
        else:
            return self._diff_payment

    def all_payments(self):
        if self._all_payments_table is not None:
            return self._all_payments_table

        payments_cat = ['amount', 'payment', 'interest_payment', 'debt_payment', 'balance']
        start_amount = self.amount
        month_num = 1
        self._all_payments_table = {}
        eval_func = self._eval_func()

        while start_amount > 0:
            payments = eval_func(start_amount)
            start_amount = payments[-1]
            self._all_payments_table[month_num] = dict(zip(payments_cat, payments))
            month_num += 1

        return self._all_payments_table

    def __str__(self):
        if self._all_payments_table is None:
            return "Call all_payments method first"

        payments_cat = ['month'] + list(self._all_payments_table[1].keys())
        max_size = max(len(str(self._all_payments_table[1]['amount'])), len('interest_payment'))
        prt = ""
        for cat in payments_cat:
            prt += cat.center(max_size + 2) + '|'

        for month in self._all_payments_table.items():
            prt += '\n' + str(month[0]).center(max_size + 2) + '|'
            for val in month[1].values():
                val = round(val, 2)
                prt += str(val).center(max_size + 2) + '|'

        return prt

    def cumulative_interest(self, period: list):
        if self._all_payments_table is None:
            self.all_payments()

        if not isinstance(period, list):
            raise TypeError("'period' must be a list")
        if len(period) != 2:
            raise ValueError("'period' must contain 2 integer numbers")

        total_interest_payment = 0
        for month in range(period[0], period[1] + 1):
            total_interest_payment += self._all_payments_table[month]['interest_payment']

        return total_interest_payment


'''
if __name__ == '__main__':
    jsonData = load_json('data.json')
    json_dict, _ = parse(jsonData)
    loan = Loan(json_dict)
    print(loan)
    loan.all_payments()
    print(loan)
    print(loan.cumulative_interest([5, 9]))
'''
