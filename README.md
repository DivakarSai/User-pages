# User-pages
Instructions for Installations

Make sure python is properly installed

Make sure pip is properly installed , [Installing pip if not present](https://pip.pypa.io/en/stable/installation/)

Install virtualenv
virtualenv is a tool to create isolated Python projects. Think of it, as a cleanroom, isolated from other virsions of Python and libriries.

Enter this command into terminal
```
sudo pip install virtualenv
```

or if you get an error

```
sudo -H pip install virtualenv
```

1. Run the follwoing command to create the virtual environment
```
python3 -m venv myenv
```

2. Activate the virtual environment:
```
source myenv/bin/activate
```

3. go to website
```
cd website
```

4. Install required libraries
```
pip install -r requirements.txt
```

5. run server
```
python manage.py runserver 
```

[server will be running at](http://127.0.0.1:8000/)




Incase any of the follwing libraries are missing try the following command
```
pip install django

pip install django-crispy-forms

pip install crispy-bootstrap5

pip install psycopg2-binary
```











