# Calculated quantile #

### Specifications & requirements
1. Language Python 3.9+
2. Flask version: 1.1.2
3. pytest

### Project structure
```
homework
|__main.py
|__service.py
|__validate.py
|__test_pool.py
|__test_quantile.py
|__requirements.txt
|__README.md
|__pools_data.csv
```

### Setup Source code guideline
<ol>
<li> Install library:

``` 
pip install -r requirements.txt
```

<li> run server:

``` 
python main.py
```

<li> run test:

``` 
py.test
```

<li> Try to connect post url:

``` 
http://127.0.0.1:5000/pool
http://127.0.0.1:5000/pool-calculator
```
