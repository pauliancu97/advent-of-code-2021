from utils import read_lines


def get_gamma_rate(numbers: list[str]) -> int:
    gamma_rate_binary = ''
    num_bits = len(numbers[0])
    for bit_index in range(0, num_bits):
        num_ones = len([1 for number in numbers if number[bit_index] == '1'])
        num_zeroes = len([1 for number in numbers if number[bit_index] == '0'])
        if num_ones > num_zeroes:
            gamma_rate_binary += '1'
        else:
            gamma_rate_binary += '0'
    return int(gamma_rate_binary, base=2)


def get_epsilon_rate(numbers: list[str]) -> int:
    epsilon_rate_binary = ''
    num_bits = len(numbers[0])
    for bit_index in range(0, num_bits):
        num_ones = len([1 for number in numbers if number[bit_index] == '1'])
        num_zeroes = len([1 for number in numbers if number[bit_index] == '0'])
        if num_ones < num_zeroes:
            epsilon_rate_binary += '1'
        else:
            epsilon_rate_binary += '0'
    return int(epsilon_rate_binary, base=2)


def get_power_rate(numbers: list[str]) -> int:
    gamma_rate = get_gamma_rate(numbers)
    epsilon_rate = get_epsilon_rate(numbers)
    return gamma_rate * epsilon_rate


def get_oxygen_rating(numbers: list[str]) -> int:
    current_numbers = numbers
    bit_index = 0
    bit_length = len(numbers[0])
    while len(current_numbers) != 1:
        num_ones = len([1 for number in current_numbers if number[bit_index] == '1'])
        num_zeroes = len([0 for number in current_numbers if number[bit_index] == '0'])
        most_common_bit = '0'
        if num_ones >= num_zeroes:
            most_common_bit = '1'
        current_numbers = [number for number in current_numbers if number[bit_index] == most_common_bit]
        bit_index = (bit_index + 1) % bit_length
    return int(current_numbers[0], 2)


def get_carbon_dioxide_rating(numbers: list[str]) -> int:
    current_numbers = numbers
    bit_index = 0
    bit_length = len(numbers[0])
    while len(current_numbers) != 1:
        num_ones = len([1 for number in current_numbers if number[bit_index] == '1'])
        num_zeroes = len([0 for number in current_numbers if number[bit_index] == '0'])
        least_common_bit = '0'
        if num_ones < num_zeroes:
            least_common_bit = '1'
        current_numbers = [number for number in current_numbers if number[bit_index] == least_common_bit]
        bit_index = (bit_index + 1) % bit_length
    return int(current_numbers[0], 2)


def get_life_support_rating(numbers: list[str]) -> int:
    return get_oxygen_rating(numbers) * get_carbon_dioxide_rating(numbers)


def solve_part_one():
    numbers = [line.replace('\n', '') for line in read_lines('day_three.txt')]
    print(get_power_rate(numbers))


def solve_part_two():
    numbers = [line.replace('\n', '') for line in read_lines('day_three.txt')]
    print(get_life_support_rating(numbers))


if __name__ == '__main__':
    solve_part_two()