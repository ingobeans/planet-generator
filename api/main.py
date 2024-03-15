from flask import Flask, render_template, request, jsonify
import random, os

file_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

def read_properties(file_name):
    with open(os.path.join(file_path, file_name), 'r') as file:
        properties = [line.strip() for line in file.readlines() if line.strip()]
    return properties

def generate_planet(seed=None):
    random.seed(seed) if seed != None else random.seed()
    names = read_properties('names.txt')
    suffixes = read_properties('suffixes.txt')
    types = read_properties('planet_types.txt')
    sky_colors = read_properties('sky_colors.txt')
    
    suffix = random.choice(suffixes) if random.randint(0, 10) == 0 else ""
    name = f"{random.choice(names)} {suffix}"
    planet_type = random.choice(types)
    
    sky_color_count = random.randint(1, 2)
    sky_color = random.sample(sky_colors, sky_color_count)
    
    if len(sky_color) == 1:
        sky_color_str = sky_color[0]
    else:
        sky_color_str = f"{sky_color[0]} and {sky_color[1]}"
    
    sky_appearance = random.choice(["uniform", "with bands", "with a gradient", "swirling"])
    
    if sky_appearance == "with bands":
        sky_description = f"{sky_color_str} with bands"
    elif sky_appearance == "with a gradient":
        sky_description = f"a gradient of {sky_color_str}"
    elif sky_appearance == "swirling":
        sky_description = f"swirling {sky_color_str}"
    else:
        sky_description = sky_color_str
    
    num_moons = random.randint(0, 5)
    moons = [(f"({i+1}) {random.choice(names)}" ) for i in range(num_moons)]
        
    size = round(random.uniform(0.5, 2), 2)
    radius = round((size ** (1 / 3)) * 6371, 2)
    gravity = round(6.674 * 10**-11 * (size * 5.972 * 10**24) / (radius * 1000)**2 / (9.81), 2)
    low_temp = round(random.uniform(-100, 50), 2)
    high_temp = round(random.uniform(50, 300), 2)
    avg_temp = round((low_temp + high_temp) / 2, 2)
    water_surface = round(random.uniform(0, 50), 2)
    water_subterranean = round(100 - water_surface, 2)
    
    length_day = round(random.uniform(10, 100), 2)
    length_year = round((radius * 2 * 3.14159) / (24 * length_day), 2)  # Assuming circular orbit
    
    if random.random() < 0.125:
        earth_life = "Suitable for Earth-based life."
    else:
        earth_life = "Unsuitable for Earth-based life (without additional support)."
    
    if random.random() < 0.5:
        seasonal_variations = "Mild: The planet's axial tilt results in mild seasonal variations."
    else:
        seasonal_variations = "Extreme: The planet's axial tilt results in extremely long-lasting seasons."
    
    planet_info = f"""
Name:   {name}
Type:   {planet_type}
Sky Color:  {sky_description}
Moons:  {num_moons}   {', '.join(moons)}
Planet Stats
Size:   {size} x Earth
Radius:   {radius} km / {radius * 0.621371} miles
Gravity:   {gravity} x Earth's gravity
Temperature range:  Low: {low_temp} °C
                High: {high_temp} °C
Average surface temperature:   {avg_temp} °C
Water Prevalence:   {water_surface}%: ({water_surface}% Surface water / {water_subterranean}% Subterranean)
Earth life:   {earth_life}
Planet Motion
Length of Day:   {length_day} hours
Length of Year:   {length_year} Earth days
Seasonal variations:  {seasonal_variations}
"""
    
    return planet_info

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        seed = None
        if request.form.get('seed'):
            seed = request.form.get('seed').strip()
            if seed.isnumeric():
                seed = int(seed)
        
        planet_info = generate_planet(seed)
        return jsonify({'planet_info': planet_info})
    return render_template('index.html')

if __name__ == '__main__':
    app.run()