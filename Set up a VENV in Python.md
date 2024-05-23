# Set up a Virtual Environment in Python
**Using virtual environments (venv) in Python helps isolate project dependencies and prevent conflicts between projects or system packages.**

Creates a Python Virtual Environment named "ENV", isolating project dependencies from the global Python environment.
```bash
python -m venv ENV
```
Activates the Python Virtual Environment named "ENV", allowing you to work within that isolated environment.
```bash
ENV\Scripts\activate
```
Installs the specified Python package in your current Python environment.
```bash
pip install <python_package_name>
```
Installs all the Python packages listed in the "requirements.txt" file.
```bash
pip install -r requirements.txt
```
