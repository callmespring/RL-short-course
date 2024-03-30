# Usage

## Play against AI
Run ```play.py``` with options

```
optional arguments:
  -h, --help            show this help message and exit
  --size [SIZE]         board size
  --win_length [WIN_LENGTH]
                        number in row to win
  --no_gui [NO_GUI]     Display GUI
  ```

The GUI is activated per default. So for example for a play ground of size 8 x 8 and for 5 stones in a row to win one would run

```
python play.py --size 8 --win_length 5
```

## Train Model

Similar syntax to playing against the AI

Run ```train.py``` with options

```
optional arguments:
  -h, --help            show this help message and exit
  --size [SIZE]         board size
  --win_length [WIN_LENGTH]
                        number in row to win
```

So for example to train on a play ground of size 8 x 8 and for 5 stones in a row to win one would run
