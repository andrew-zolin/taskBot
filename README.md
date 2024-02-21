### TaskBot

## Install requirements

<code> pythom -m pip install -r req.txt </code>


## Preparing

<ol>Create tokens.txt in the base directory
    <li><code>TEST==your_test_bot_token
MAIN==your_main_bot_token</code></li>
</ol>

<ol>Create data base in the webApp directory
    <li><code>python manage.py makemigrations</code></li>
    <li><code>python manage.py migrate</code></li>
</ol>


## Run

<ol>Run taskBot from the taskBot directory
    <li><code>python main.py</code></li>
</ol>
<ol>Run webAdmin in debag mode from the webApp directory
    <li><code>python manage.py runserver 0.0.0.0:8000</code></li>
</ol>

