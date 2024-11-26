import argparse
import subprocess
import sys
import os
import platform


def main(input, output):
    with open(input, "r", encoding="utf8") as fi:
        predicted = PredictPunctuation(fi.read())
        with open(output, "w", encoding="utf8") as fo:
            fo.write(predicted)


def PredictPunctuation(text):
    # https://huggingface.co/docs/transformers/installation#cache-setup
    if not os.environ.get("HF_HOME"):
        if platform.system() == "Windows":
            os.environ["HF_HOME"] = r"C:\Users\user\.cache\huggingface"
        else:
            os.environ["HF_HOME"] = "~/.cache/huggingface"

    try:
        predicted = subprocess.check_output(
            "python3 recasepunc/recasepunc.py predict recasepunc/checkpoint",
            shell=True,
            text=True,
            input=text,
        )
        return predicted
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Predicts text letters case and punctuation.
        Расставляет пунктуацию в тексте по подсказкам модели""",
    )
    parser.add_argument("input", help="plain text input path", default="", type=str)
    parser.add_argument("-o", "--output", help="optional output text path", type=str)

    args = parser.parse_args()

    if not args.input:
        print('invalid input filename "%s"' % args.input)
        sys.exit(1)

    if not args.output:
        output = ".".join((args.input, "predicted", "txt"))

    main(args.input, output)
