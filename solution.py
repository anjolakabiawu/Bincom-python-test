import re
import random
import psycopg2
from collections import Counter
from statistics import median, variance

# Sample HTML table containing colors worn per day
html_data = """
<table>
    <tr><td>MONDAY</td><td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td></tr>
    <tr><td>TUESDAY</td><td>ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE</td></tr>
    <tr><td>WEDNESDAY</td><td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE</td></tr>
    <tr><td>THURSDAY</td><td>BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td></tr>
    <tr><td>FRIDAY</td><td>GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE</td></tr>
</table>
"""

# Extracting only the colors
def extract_colors(html):
    # Extract only the second column
    pattern = r'<td>([^<]+)</td>\s*<td>([^<]+)</td>'
    matches = re.findall(pattern, html)

    colors = []
    for _, color_list in matches:
        colors.extend(re.findall(r'\b[A-Z]+\b', color_list)) # Extract only the color

    return colors

colors = extract_colors(html_data)
color_counts = Counter(colors)

# Removing Non-color words (e.g ARSH and BLEW)
valid_colors = set([
    "RED", "BLUE", "GREEN", "YELLOW", "WHITE", "BLACK", "BROWN", "PINK", "ORANGE", "CREAM"
])
filtered_colors = {color: count for color, count in color_counts.items() if color in valid_colors}

# Question 1
mean_color = max(filtered_colors, key=filtered_colors.get)

# Question 2
color_most_worn = sorted(filtered_colors.items(), key=lambda x: x[1])

# Question 3
median_color = color_most_worn[len(color_most_worn) // 2][0]

# Question 4
color_values = list(filtered_colors.values())
color_variance = variance(color_values) if len(color_values) > 1 else 0

# Question 5
prob_red = filtered_colors.get('RED', 0) / sum(filtered_colors.values())

# Question 6
def save_to_db(data):
    try:
        conn = psycopg2.connect(database="colors_db", user="postgres", password="jvnjbjNrH6E8@sS", host="127.0.0.1", port="5432")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS color_frequency (color TEXT PRIMARY KEY, count INTEGER);")
        for color, count in data.items():
            cursor.execute("INSERT INTO color_frequency (color, count) VALUES (%s, %s) ON CONFLICT (color) DO UPDATE SET count = EXCLUDED.count;", (color, count))
        conn.commit()
        conn.close()
        print("Data saved successfully!")
    except Exception as e:
        print(f"Database Error: {e}")

save_to_db(filtered_colors)

# Question 7
def recursive_search(arr, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return recursive_search(arr, target, low, mid -1)
    else:
        return recursive_search(arr, target, mid + 1, high)

# Question 8
binary_num = ''.join(str(random.randint(0, 1)) for _ in range(4))
decimal_value = int(binary_num, 2)

# Question 9
def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n) :
        total += a
        a,b = b, a + b
        return total

fib_sum = fibonacci_sum(50)

# Display results
print(f"Most Common (Mean) Color: {mean_color}")
print(f"Median Color: {median_color}")
print(f"Variance of Colors: {color_variance}")
print(f"Probability of Choosing 'RED': {prob_red:.4f}")
print(f"Random 4-bit Binary: {binary_num}, Decimal Equivalent: {decimal_value}")
print(f"Sum of First 50 Fibonacci Numbers: {fib_sum}")