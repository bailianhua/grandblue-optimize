# Damage Optimization App

This web application is designed to optimize damage for a scenario based on user input.

## prerequisites
1. Python
2. Pip (optional)

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies using `python -m pip install -r requirements.txt` or if you have pip installed, `pip install -r requirements.txt` .
3. Run the Flask web application using `python main.py`.
4. Access the application in your web browser at `http://localhost:5000`.

## Usage

1. Input the base damage, critical rate, critical damage, and total items in the form.
2. Click the "Optimize Damage" button to calculate the optimal distribution of items.
3. View the optimized item distribution and maximized total damage on the results page.

## Configuration

You can adjust the default parameters such as `damage_item`, `crit_rate_item`, `crit_dmg_item`, `crit_damage_base` in the `main.py` file to customize the application for your specific scenario.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
