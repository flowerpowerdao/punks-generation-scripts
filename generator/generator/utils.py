from pathlib import Path
from random import choice, uniform, choices
from typing import List


def calculate_weights(weights_1, weights_2):
    """Returns the product of the two lists, starting from the first element in weights_1 multiplied by all the elemnts in weights_2"""

    all_weights = []

    for weight_1 in weights_1:
        for weight_2 in weights_2:
            all_weights.append(weight_1*weight_2)

    return all_weights


def get_filenames(path, exclude_list: List[str]):
    """Returns a list of filenames in the given path relative to assets"""

    folder_path = Path(path)
    # filter out files that have lowres in their path so we don't
    # have twice the same flower
    relative_filenames = [str(file_path.relative_to("../assets/"))
                          for file_path in sorted(folder_path.glob("*")) if not any(excluded in file_path.stem for excluded in exclude_list)]
    return relative_filenames


def add_assets(soup, asset_canister, **kwargs):
    """Changes the layers of the template svg file"""

    for key, value in kwargs.items():
        soup.find('image', {'id': key})['href'] = asset_canister + value


def pick_choice(set, weights):
    choice = choices(set, weights)[0]
    lowres_choice = choice[:choice.rfind(
        "/")+1] + "_thumbnail_" + choice[choice.rfind("/")+1:]
    return choice, lowres_choice


def add_petal_animation(soups: list):
    """Add petal animations to the provided soups. This ensures all petals animations are the same accross the different resolutions"""

    base_styles = '''
    .st0 {
        fill: #00FD00;
    }

    /* The animation code */
    @keyframes example {
        from {
            opacity: 0.7;
        }

        to {
            opacity: 0;
        }
    }

'''

    for i in range(20):
        base_styles += (f'\t#petal{i+1} {{\n'
                        f'\t\tanimation-timing-function: {choice(["linear", "ease", "ease-in","ease-out"])};\n'
                        f'\t\tanimation-delay: {uniform(0,2):.2f}s;\n'
                        f'\t\tanimation-duration: {uniform(0.5,4):.2f}s;\n'
                        f'\t\tanimation-name: example;\n'
                        f'\t\tanimation-iteration-count: infinite;\n'
                        f'\t\tanimation-direction: alternate;\n'
                        f'\t\topacity: 0.7;\n'
                        '\t}\n\n'
                        )
    for soup in soups:
        soup.style.string = base_styles

    return soups


def get_trait(s: str, suffix=".png"):
    first = "/"
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(suffix, start)
        return s[start:end]
    except ValueError:
        return ""


def check_for_triples(triples_data, materials, flower, coin, grave):
    """Checks if the flower, coin and grave have the same trait and if increases the count of that trait"""

    for index, material in enumerate(materials):
        if material in flower and material in coin and material in grave:
            triples_data[index] += 1

# Print iterations progress


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
