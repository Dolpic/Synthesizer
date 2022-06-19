# Synthesizer

## Install
Assuming you use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/), which is very good.
```bash
mkvirtualenv synthesizer
pip install -r requirements.txt
```

Also assuming you use Ubuntu or Debian. Please look for equivalent packages for your distribution.
```bash
apt install libportaudio2
apt install python3-tk
```

## Use the synthesizer in Jupyter Lab
Please see the included Synthesizer.ipynb, which will walk you through the process.

## Use the program in CLI
First activate the virtualenv.
```bash
workon synthesizer
```

Then run the `cli_main.py` file. Your OS may want you to precise `python3` instead of simply `python`.
```bash
python cli_main.py
```

You can then activate your MIDI keyboard and play with the default settings.

To change your settings, simply copy the `current_script.py` file and tinker with it! Look at all the available modules in the Modules and MIDI folders.

The class `MidiToFreq` specifies how MIDI messages should be converted to Frequency-Amplitudes tuples. This would be a nice place to put e.g. an Arpeggiator, which we did. All the filters of this type are in the `MIDI/filters` folder.

The class `FreqToAudio` directly takes the output of the previous one, and converts it to actual Left/Right-Channel sound. All available modules/filters are in the `Modules/filters` folder.

It is possible to tinker with the `parameters.py` file, notably with the `TEMPERAMENT` setting, which allows you to experience the automatic variable pitch algorithm.
