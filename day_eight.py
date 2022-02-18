from __future__ import annotations
from dataclasses import dataclass
from utils import read_lines

@dataclass
class Sample:
    digits: list[str]
    outputs: list[str]

    @staticmethod
    def from_line(line: str) -> Sample:
        digits_str_part, outputs_str_part = line.split('|')
        digits = digits_str_part.split()
        outputs = outputs_str_part.split()
        return Sample(digits, outputs)


def get_samples(path: str) -> list[Sample]:
    lines = read_lines(path)
    return [Sample.from_line(line) for line in lines]


def get_num_of_easy_outputs(samples: list[Sample]) -> int:
    outputs = sum([sample.outputs for sample in samples], [])
    return len([1 for output in outputs if len(output) in [2, 3, 4, 7]])


def get_signals_mapping(outputs: list[str]) -> dict[str, str]:
    result = dict[str, str]()
    config_one = [output for output in outputs if len(output) == 2][0]
    config_seven = [output for output in outputs if len(output) == 3][0]
    config_four = [output for output in outputs if len(output) == 4][0]
    config_eight = [output for output in outputs if len(output) == 7][0]
    output_letter_a = [letter for letter in config_seven if letter not in config_one][0]
    result[output_letter_a] = 'a'
    temp_config_1 = config_four + output_letter_a
    config_nine = [config for config in [output for output in outputs if len(output) == 6] if all(letter in config for letter in temp_config_1)][0]
    output_letter_g = [letter for letter in config_nine if letter not in temp_config_1][0]
    result[output_letter_g] = 'g'
    output_letter_e = [letter for letter in config_eight if letter not in config_nine][0]
    result[output_letter_e] = 'e'
    temp_config_2 = [output for output in outputs if len(output) == 6 and output != config_nine and all(letter in output for letter in config_seven)][0]
    output_letter_b = [letter for letter in temp_config_2 if letter not in (config_seven + output_letter_e + output_letter_g)][0]
    result[output_letter_b] = 'b'
    output_letter_d = [letter for letter in config_four if letter not in config_one + output_letter_b][0]
    result[output_letter_d] = 'd'
    config_five = [output for output in outputs if len(output) == 5 and output_letter_e not in output and not all(letter in output for letter in config_one)][0]
    output_letter_f = [letter for letter in config_five if letter not in output_letter_a + output_letter_b + output_letter_d + output_letter_g][0]
    result[output_letter_f] = 'f'
    output_letter_c = [letter for letter in config_one if letter != output_letter_f][0]
    result[output_letter_c] = 'c'
    return result

def get_digit(output: str) -> int:
    digits_dict = {
        'abcefg': 0, 
        'cf': 1,
        'acdeg': 2, 
        'acdfg': 3,
        'bcdf': 4,
        'abdfg': 5,
        'abdefg': 6,
        'acf': 7,
        'abcdefg': 8,
        'abcdfg': 9
    }
    sorted_output = ''.join(sorted(output))
    return digits_dict[sorted_output]


def get_correct_output(output: str, signal_mapping: dict[str, str]) -> str:
    return ''.join([signal_mapping[letter] for letter in output])


def get_correct_digit(output: str, signal_mapping: dict[str, str]) -> int:
    correct_output = get_correct_output(output, signal_mapping)
    return get_digit(correct_output)


def get_sample_output(sample: Sample, signal_mapping: dict[str, str]) -> int:
    result = 0
    for output in sample.outputs:
        result = result * 10 + get_correct_digit(output, signal_mapping)
    return result


def solve_part_one() -> None:
    samples = get_samples('day_eight.txt')
    print(get_num_of_easy_outputs(samples))


def solve_part_two() -> None:
    samples = get_samples('day_eight.txt')
    result = 0
    for sample in samples:
        signal_mapping = get_signals_mapping(sample.digits)
        sample_output = get_sample_output(sample, signal_mapping)
        result += sample_output
    print(result)


if __name__ == '__main__':
    solve_part_two()