# badminton_booking
booking for badminton courts Hall Oners

Uses python 3.11

Create a virtual environment and run
```
pip install -r requirements.txt
```
booking for badminton courts Hall Oners

## How to guide
Create a ```.env``` file and copy the contents of ```.env.template``` into it

Add your NTU username (@student.main.ntu.edu.sg) and password 

Enter the court number (1-6 accepted). If you want any courts to be selected, leave it as blank

Enter the Date (Format: dd-Mmm-yyyy)

Enter the Time (Start time, 24hrs format: 0800 - 2100)

Run ```python main.py``` afterward and watch it run

## Note

Existence of a forever loop if no courts are available for that date & timing