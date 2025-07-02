for Mac/Ubuntu
```
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip && pip install -r requirements.txt 
```

```
python3 main.py --dir-path [CSV-PATH] --weight-list 0.7 0.3 
```
```
python3 main.py --dir-path [CSV-PATH] --weight-list 0.7 0.3 -o [OUTPUT]
```
```
python3 main.py --dir-path [CSV-PATH] --weight-list 0.7 0.3 -o [OUTPUT] --show-info
```