from __future__ import annotations
from enum import Enum
from matrix import Matrix
from utils import read_lines
from copy import deepcopy


class Pixel(Enum):
    ON = '#'
    OFF = '.'

    def __str__(self: Pixel) -> str:
        match self:
            case Pixel.OFF:
                return '.'
            case Pixel.ON:
                return '#'
        


EnhancementAlgorithm = list[Pixel]
Image = Matrix[Pixel]


def get_enhancement_algorithm(string: str) -> EnhancementAlgorithm:
    return [Pixel(character) for character in string]


def get_image(lines: list[str]) -> Image:
    pixels = [[Pixel(character) for character in line] for line in lines]
    return Matrix(pixels)


def get_input(path: str) -> tuple[EnhancementAlgorithm, Image]:
    lines = read_lines(path)
    enhancement_algorithm = get_enhancement_algorithm(lines[0])
    image = get_image(lines[2:])
    return enhancement_algorithm, image



def get_expanded_image(image: Image, fill_pixel: Pixel) -> Image:
    expanded_image: Image = Matrix.with_default(image.rows + 6, image.cols + 6, fill_pixel)
    for row in range(image.rows):
        for col in range(image.cols):
            expanded_image[row + 3, col + 3] = image[row, col]
    return expanded_image


def get_enhancement_algorithm_index(image: Image, row: int, col: int) -> int:
    binary_string = ''
    for row_offset in range(-1, 2):
        for col_offset in range(-1, 2):
            offseted_row = row + row_offset
            offseted_col = col + col_offset
            if image.has_coordinates((offseted_row, offseted_col)):
                match image[offseted_row, offseted_col]:
                    case Pixel.OFF:
                        binary_string += '0'
                    case Pixel.ON:
                        binary_string += '1'
    return int(binary_string, base=2)


def get_enhanced_image(image: Image, algorithm: EnhancementAlgorithm, fill_pixel: Pixel) -> tuple[Image, Pixel]:
    expanded_image = get_expanded_image(image, fill_pixel)
    temp_result = deepcopy(expanded_image)
    for row in range(1, expanded_image.rows - 1):
        for col in range(1, expanded_image.cols - 1):
            algorithm_index = get_enhancement_algorithm_index(expanded_image, row, col)
            temp_result[row, col] = algorithm[algorithm_index]
    result: Image = Matrix.with_default(temp_result.rows - 2, temp_result.cols - 2, fill_pixel)
    for row in range(result.rows):
        for col in range(result.cols):
            result[row, col] = temp_result[row + 1, col + 1]
    next_fill_pixel = algorithm[0] if fill_pixel == Pixel.OFF else algorithm[-1]
    return result, next_fill_pixel


def get_enhanced_image_after_iter(image: Image, algorithm: EnhancementAlgorithm, num_iter: int) -> Image:
    current_image = deepcopy(image)
    fill_pixel = Pixel.OFF
    for _ in range(num_iter):
        next_image, next_fill_pixel = get_enhanced_image(current_image, algorithm, fill_pixel)
        current_image = next_image
        fill_pixel = next_fill_pixel
    return current_image

def get_num_on_pixels(image: Image) -> int:
    return len([True for row in range(image.rows) for col in range(image.cols) if image[row, col] == Pixel.ON])


def solve_part_one() -> None:
    algorithm, image = get_input('day_twenty.txt')
    enhanced_image = get_enhanced_image_after_iter(image, algorithm, 50)
    num_on_pixels = get_num_on_pixels(enhanced_image)
    print(num_on_pixels)


if __name__ == '__main__':
    solve_part_one()