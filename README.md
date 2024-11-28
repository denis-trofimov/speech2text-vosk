# Speech to text transcription offline using VOSK

## Credits

Thanks goes to Telegram @Andrey_Totshin for solving this problem in the [article][article] (in Russian).

## Installation

To implement audio to text transcription, we need to solve the following problems:

Extract parts of speech from audio.
Add spaces between parts of speech.
Add punctuation to text.

I will do all the actions on a Linux Ubuntu 24 machine with (Python 3.12) with the following configuration:

    CPU Intel Core i5-6300U laptop.
    RAM 16GB.
    No GPU
    SSD 500GB.

The reason for using such a large amount of RAM is that we are doing recognition on a universal model, that is, a 50 MB model, which requires several times less RAM in operation than a full-fledged model. However, the quality of recognition in this case will decrease.

Clone this repo:

    git clone git@github.com:denis-trofimov/speech2text-vosk.git

Next, you need to install dependencies for Python:

    apt install python3-pip
    pip3 install ffmpeg
    pip3 install pydub
    pip3 install vosk
    pip3 install torch
    pip3 install transformers

Or use poetry:

    poetry install

*You can use any VOSK LM for any language available. There is no language selection in my code.*
*I've used Russian speech recognition LM for my task.*

Also download and unzip the model for Russian speech recognition by running the commands:

    curl -o ./model.zip https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip \
    && unzip model.zip \
    && mv vosk-model-ru-0.42/ model \
    && rm -rf model.zip

As a result of these actions, we copied the model to ourselves, unzipped it and renamed the directory. We also deleted the downloaded archive. After all, it weighs 1.5 GB. To arrange punctuation, we do similar actions: download another model weighing 1.5 GB.

    curl -o recasepunc.zip https://alphacephei.com/vosk/models/vosk-recasepunc-ru-0.22.zip \
    && unzip recasepunc.zip \
    && mv vosk-recasepunc-ru-0.22/ recasepunc \
    && rm -rf recasepunc.zip

## Usage

    python3 transcribe.py samples/test.mp3

  or

    poetry run python3 transcribe.py samples/test.mp3

## Help

    $ python3 transcribe.py -h
    usage: transcribe.py [-h] [-m MODEL] [-o OUTPUT] input

    Transcribes speech to text. Распознает речь в текст

    positional arguments:
      input                 Speech audio input path

    options:
      -h, --help            show this help message and exit
      -m MODEL, --model MODEL
                            model path
      -o OUTPUT, --output OUTPUT
                            optional output text path

    $ python3 predict_punctuation.py -h
    usage: predict_punctuation.py [-h] [-o OUTPUT] input

    Predicts text letters case and punctuation. Расставляет пунктуацию в тексте по подсказкам модели

    positional arguments:
      input                 plain text input path

    options:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            optional output text path

## Fixes

To workaround a bug in "recasepunc/recasepunc.py" and not having to downgrade **transformers** version, please apply my patch, overwriting the original "recasepunc/recasepunc.py".
It adds the keyword "strict=False" to every **model.load_state_dict** call.

    cp patches/recasepunc.py recasepunc/recasepunc.py

[article]: https://proglib.io/p/reshaem-zadachu-perevoda-russkoy-rechi-v-tekst-s-pomoshchyu-python-i-biblioteki-vosk-2022-06-30
