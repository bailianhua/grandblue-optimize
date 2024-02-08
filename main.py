from flask import Flask, render_template, request

app = Flask(__name__)


damage_item = 50
crit_rate_item = 19
crit_dmg_item = 35
crit_damage_base = 225


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        base_damage = int(request.form['base_damage'])
        crit_rate = int(request.form['crit_rate_base'])
        total_items = int(request.form['total_items'])

    # Initialize variables to store the optimal solution
        optimal_solution = None
        max_final_damage = float('-inf')
        optimal_crit_rate = None
        optimal_crit_damage = None
        optimal_base_damage = None

        for x in range(min(total_items, 4) + 1):
            # Calculate initial crit rate with item bonus
            crit_rate_total_initial = min(
                crit_rate + crit_rate_item * 0, 100)  # y is 0 initially
            for y in range(min(total_items - x, 4) + 1):
                # Check if the initial crit rate is already at 100%
                if crit_rate_total_initial == 100 and y > 0:
                    break  # If initial crit rate is already at 100%, no need to increase y further
                # Calculate crit rate and ensure it does not exceed 100
                crit_rate_total = min(
                    crit_rate_total_initial + crit_rate_item * y, 100)
                # Check if crit_damage_base is already at maximum (50)
                if int(request.form['crit_damage_base']) == 50:
                    z = 0  # If crit_damage_base is 50, don't increase z
                else:
                    # Limit z to remaining item count or 4, whichever is smaller
                    z = min(total_items - x - y, 4)
                # Calculate base damage with item bonus
                base_damage_total = base_damage * \
                    (1 + min(damage_item * x, 70) / 100)
                # Calculate crit damage with item bonus
                crit_damage_total = crit_damage_base + \
                    min((crit_dmg_item * z) +
                        int(request.form['crit_damage_base']), 50)
                # Calculate final damage
                final_damage = base_damage_total * \
                    (1 + (crit_rate_total / 100) * ((crit_damage_total / 100) - 1))
                # Check if this combination produces better damage
                if final_damage > max_final_damage:
                    # Update optimal solution
                    max_final_damage = final_damage
                    optimal_solution = (x, y, z)
                    optimal_crit_rate = crit_rate_total
                    optimal_crit_damage = crit_damage_total
                    optimal_base_damage = base_damage_total
        return render_template('result.html',
                               optimal_base_damage_items=optimal_solution[0],
                               optimal_crit_rate_items=optimal_solution[1],
                               optimal_crit_damage_items=optimal_solution[2],
                               maximized_total_damage=max_final_damage,
                               crit_rate=optimal_crit_rate,
                               crit_damage=optimal_crit_damage,
                               total_base_damage=optimal_base_damage
                               )
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
