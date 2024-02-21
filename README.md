<style>
    .ul {
        text-decoration: none
    }
</style>

# TaskBot

## Install requirements

<code> pythom -m pip install -r req.txt </code>


## Preparing

<ul>Create tokens.txt in the base directory with same text:
    <li>
    TEST==your_test_bot_token
    MAIN==your_main_bot_token
    </li>      
</ul>

<ul>Create data base in the webApp directory
    <li>-- <code>python manage.py makemigrations</code></li>
    <li>-- <code>python manage.py migrate</code></li>
</ul>


## Run

<ul>Run taskBot from the taskBot directory
    <li>-- <code>python main.py</code></li>
</ul>
<ul>Run webAdmin in debag mode from the webApp directory
    <li>-- <code>python manage.py runserver 0.0.0.0:8000</code></li>
</ul>

