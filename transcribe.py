import argparse
import json
import os
import sys

from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment

from predict_punctuation import PredictPunctuation


# When using your own audio file make sure it has the correct format - PCM 16khz 16bit mono.
# Otherwise, if you have ffmpeg installed, you can use test_ffmpeg.py, which does the conversion for you.
# https://alphacephei.com/vosk/install
FRAME_RATE = 16000
CHANNELS = 1


def main(input, output, model):
    with open(input, "rb") as fi:
        # Используя библиотеку pydub делаем предобработку аудио
        audio = AudioSegment.from_file(fi)
        audio = audio.set_channels(CHANNELS)
        audio = audio.set_frame_rate(FRAME_RATE)

        scribed = Transcribe(audio, model)
        # Добавляем пунктуацию
        predicted = PredictPunctuation(scribed)

        with open(output, "w", encoding="utf8") as fo:
            fo.write(predicted)


def Transcribe(audio, model):
    SetLogLevel(0)
    model = Model("model")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)

    # Преобразуем вывод в json
    rec.AcceptWaveform(audio.raw_data)
    result = rec.Result()
    return json.loads(result)["text"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Transcribes speech to text.
        Распознает речь в текст""",
    )
    parser.add_argument("input", help="Speech audio input path", default="", type=str)
    parser.add_argument("-m", "--model", help="model path", default="model", type=str)
    parser.add_argument("-o", "--output", help="optional output text path", type=str)

    args = parser.parse_args()

    if not args.input:
        print('invalid input filename "%s"' % args.input)
        sys.exit(1)

    if not args.output:
        output = ".".join((args.input, "txt"))

    # Проверяем наличие модели
    if not os.path.exists(args.model):
        print(
            "Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder."
        )
        sys.exit(1)

    main(args.input, output, args.model)
