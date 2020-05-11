import pandas
import matplotlib.pyplot as plt
import itertools
import numpy as np
import time


def get_two_points_circle(a, b):
    a_x, a_y = a
    b_x, b_y = b
    center_x = (a_x + b_x) / 2
    center_y = (a_y + b_y) / 2
    radius = np.linalg.norm([a_x - b_x, a_y - b_y])
    return center_x, center_y, radius

def get_triangle_circle(b, c, d):
    temp = c[0]**2 + c[1]**2
    bc = (b[0]**2 + b[1]**2 - temp) / 2
    cd = (temp - d[0]**2 - d[1]**2) / 2
    det = (b[0] - c[0]) * (c[1] - d[1]) - (c[0] - d[0]) * (b[1] - c[1])

    if abs(det) < 1.0e-10:
        return None, None, None

    # Center of circle
    cx = (bc*(c[1] - d[1]) - cd*(b[1] - c[1])) / det
    cy = ((b[0] - c[0]) * cd - (c[0] - d[0]) * bc) / det

    radius = ((cx - b[0])**2 + (cy - b[1])**2)**.5

    return cx, cy, radius
  
  
def main():
    cities = pandas.read_csv('worldcities.csv', header=0, index_col='id')
    country_name = 'Canada'
    country_cities = cities[cities['country'] == country_name]
    total_population = country_cities['population'].sum()

    print(f'{country_name} has {len(country_cities)} cities, total population {total_population}')
    start_time = time.time()
    # Find the smallest circle for 50% of the cities
    city_pairs = itertools.combinations(country_cities.itertuples(), 2)
    minimal_radius = np.inf
    minimal_center = (0, 0)
    for city_pair in city_pairs:
        pair_points = [(c.lng, c.lat) for c in city_pair]
        circle_center_lng, circle_center_lat, radius = get_two_points_circle(*pair_points)
        if radius is None or radius > minimal_radius:
            continue

        cities_in_the_circle = (
            (country_cities['lng'] - circle_center_lng) ** 2 + 
            (country_cities['lat'] - circle_center_lat) ** 2 <= radius ** 2
        )
        population_in_cycle = country_cities[cities_in_the_circle]['population'].sum()
        if population_in_cycle >= total_population * 0.5:
            minimal_radius = radius
            minimal_center = (circle_center_lng, circle_center_lat)

    _, ax = plt.subplots()
    ax.scatter(country_cities['lng'], country_cities['lat'], country_cities['population'] / 100000)
    for _, city in country_cities.iterrows():
        ax.annotate(city['city'], (city['lng'], city['lat']))
    circle_center_lng, circle_center_lat = minimal_center
    print(f"Center at ({circle_center_lng}, {circle_center_lat}) with radius {minimal_radius}")
    print(f"Took {time.time() - start_time}s")
    circle = plt.Circle((circle_center_lng, circle_center_lat), minimal_radius, color='g', fill=False)
    ax.add_artist(circle)
    plt.show()


if __name__ == '__main__':
    main()