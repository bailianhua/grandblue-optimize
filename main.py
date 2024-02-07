from flask import Flask, render_template, request
from scipy.optimize import minimize

app = Flask(__name__)

base_damage = 6000
crit_rate_base = 40
crit_damage_base = 225
base_damage_increase = 0.50
crit_rate_increase = 0.19
crit_damage_increase = 0.35
total_items = 4


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        base_damage = int(request.form['base_damage'])
        crit_rate_base = int(request.form['crit_rate_base']) / 100
        crit_damage_base = (225 + int(request.form['crit_damage_base'])) / 100
        total_items = int(request.form['total_items'])
        print(base_damage, crit_rate_base, crit_damage_base, total_items)

        def total_damage(items):
            x, y, z = items
            total_base_damage = base_damage * (1 + base_damage_increase * z)
            total_crit_rate = crit_rate_base + crit_rate_increase * x
            total_crit_damage = crit_damage_base + crit_damage_increase * y
            return -total_base_damage * (1 + total_crit_rate * (total_crit_damage - 1))

        def constraints(items):
            x, y, z = items
            return [
                total_items - sum(items),
                1 - (crit_rate_base + (crit_rate_increase * x)),
                0.7 - (base_damage_increase * z),
                0.5 - (crit_rate_increase * x),
                0.5 - (crit_damage_increase * y)
            ]

        initial_guess = [0, 0, 0]
        bounds = [(0, 3), (0, 2), (0, 2)]
        result = minimize(total_damage, initial_guess, constraints={
                          'type': 'ineq', 'fun': constraints}, bounds=bounds, method='SLSQP')
        optimal_crit_rate_items = round(result.x[0])
        optimal_crit_damage_items = round(result.x[1])
        optimal_base_damage_items = round(result.x[2])
        maximized_total_damage = -result.fun
        return render_template('result.html',
                               optimal_crit_rate_items=optimal_crit_rate_items,
                               optimal_crit_damage_items=optimal_crit_damage_items,
                               optimal_base_damage_items=optimal_base_damage_items,
                               maximized_total_damage=maximized_total_damage)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
