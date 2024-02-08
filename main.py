from flask import Flask, render_template, request
from scipy.optimize import minimize
import numpy as np

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

        def total_damage(items):
            x, y, z = items
            total_base_damage = base_damage * \
                (1 + min(base_damage_increase * z, 0.7))
            total_crit_rate = crit_rate_base + min(crit_rate_increase * x, 0.5)
            total_crit_damage = crit_damage_base + \
                min(crit_damage_increase * y, 0.5)
            return -total_base_damage * (1 + total_crit_rate * (total_crit_damage - 1))

        def constraints(items):
            x, y, z = items
            return [
                total_items - sum(items),
                1 - (crit_rate_base + (crit_rate_increase * x)),
                x - np.floor(x),
                y - np.floor(y),
                z - np.floor(z)
            ]

        initial_guess = [0, 0, 0]
        bounds = [(0, total_items), (0, total_items), (0, total_items)]
        result = minimize(total_damage, initial_guess, constraints={
                          'type': 'ineq', 'fun': constraints}, bounds=bounds, method='SLSQP')

        optimal_crit_rate_items = round(result.x[0])
        optimal_crit_damage_items = round(result.x[1])
        optimal_base_damage_items = round(result.x[2])
        maximized_total_damage = -result.fun
        print(optimal_base_damage_items, base_damage_increase)
        return render_template('result.html',
                               optimal_crit_rate_items=optimal_crit_rate_items,
                               optimal_crit_damage_items=optimal_crit_damage_items,
                               optimal_base_damage_items=optimal_base_damage_items,
                               maximized_total_damage=maximized_total_damage,
                               crit_rate=crit_rate_base +
                               min(0.5, crit_rate_increase *
                                   optimal_crit_rate_items),
                               crit_damage=crit_damage_base +
                               min(0.5, crit_damage_increase *
                                   optimal_crit_damage_items),
                               total_base_damage=base_damage *
                               (1 + min(0.7, optimal_base_damage_items *
                                        base_damage_increase)
                                )
                               )
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
