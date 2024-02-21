# TaskBot

## Install requirements

<code> pythom -m pip install -r req.txt </code>


## Preparing

### Create tokens.txt in the base directory with same text:
<ul>
    <li>
    TEST==your_test_bot_token
    MAIN==your_main_bot_token
    </li>      
</ul>

### Create data base in the webApp directory
<ul>
    <li><code>python manage.py makemigrations</code></li>
    <li><code>python manage.py migrate</code></li>
</ul>


## Run

### Run taskBot from the taskBot directory
<ul>
    <li><code>python main.py</code></li>
</ul>

### Run webAdmin in debag mode from the webApp directory
<ul>
    <li><code>python manage.py runserver 0.0.0.0:8000</code></li>
</ul>

