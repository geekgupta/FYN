# Pricing Module v2
$Price = (DBP + (Dn * DAP)) + (Tn * TMF) + WC$) *where D → Additional distance traveled

### How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/geekgupta/FYN.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Assignment
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser for Django Admin:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Access the Django Admin interface at [http://localhost:8000/admin](http://localhost:8000/admin) and log in with the superuser credentials.

### Running Tests

To run tests:

```bash
python manage.py test App.tests
```
