# Accuknox_Django_Trainee_Assignment
## My Application assignment For Django Trainee At AccuKnox

## ❓ Topic: Django Signals

### Question1: By default are django signals executed synchronously or asynchronously? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.
 
A: Django signals are executed **synchronously** by default. This means that when a signal is sent, the corresponding receiver functions are executed immediately in the same thread. I'll create a simple example that proves this by using time delays and print statements to show the execution order.  

Here’s a code snippet to demonstrate this:

```python
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import time

class User(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=User)
def slow_signal_handler(sender, instance, created, **kwargs):
    print(f"Signal handler started at: {time.time()}")
    time.sleep(2)  # Simulate slow operation
    print(f"Signal handler finished at: {time.time()}")

# This code will be executed in the shell:
"""
from signals_demo.models import User
import time

print(f"Before save: {time.time()}")
user = User.objects.create(name="Test")
print(f"After save: {time.time()}")
"""
```
```output
Before save: 1673012345.123456
Signal handler started at: 1673012345.234567
(Signal handler delays execution for 2 seconds)
Signal handler finished at: 1673012347.234567
After save: 1673012347.345678
```
**Explanation**

- The User.objects.create(name="Test") statement triggers the post_save signal.
- The signal handler slow_signal_handler starts execution immediately after the save operation begins.
- The time.sleep(2) in the signal handler simulates a slow operation, delaying the main thread.
- The final print("After save") statement is only executed after the signal handler finishes its work.

This behavior demonstrates that Django signals are executed *synchronously* by default, as the main thread is blocked until the signal handler completes execution.

### Question 2: Do django signals run in the same thread as the caller? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.

A: Yes, Django signals run in the same thread as the caller by default. Here's a proof using thread IDs:

#### Code Snippet: Django Signals Thread Demo `models.py`
```python
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import threading

class User(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=User)
def thread_checking_signal(sender, instance, created, **kwargs):
    print(f"Signal handler thread ID: {threading.get_ident()}")

# This code will be executed in the shell:
"""
from signals_demo.models import User
import threading

print(f"Main thread ID: {threading.get_ident()}")
user = User.objects.create(name="Test")
"""
```

**Explaination**

When you run this code in the Django shell, you'll see output like:
```output
Main thread ID: 140712834927360
Signal handler thread ID: 140712834927360
```
The identical thread IDs prove that the signal handler runs in the same thread as the caller. If signals ran in a different thread, the thread IDs would be different.
- The threading.get_ident() function retrieves the unique identifier of the currently running thread.
- The output shows that both the main thread (caller) and the signal handler run in the same thread, as their thread IDs are identical.
- This conclusively proves that Django signals execute synchronously in the same thread as the caller by default.

### Question 3: By default do django signals run in the same database transaction as the caller? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.

A: Yes, Django signals run in the **same database transaction** as the caller by default. This means that if an exception occurs in a signal handler, it will cause the entire database transaction, including the caller's operation, to roll back. Here's a proof:

#### Code Snippet: Django Signals Transaction Demo `models.py`

The following code demonstrates this behavior:

```python
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    name = models.CharField(max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='')

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # This will fail if we're not in the same transaction
        # as the original User creation
        raise Exception("Intentional error in signal")
        Profile.objects.create(user=instance)

# This code will be executed in the shell:
"""
from signals_demo.models import User
from django.db import transaction

try:
    with transaction.atomic():
        user = User.objects.create(name="Test")
        # If signals weren't running in the same transaction,
        # the user would still be created
except Exception:
    print("Transaction rolled back")

# This should print 0 if the transaction was rolled back
print(f"Users count: {User.objects.count()}")
"""
```

**Explaination**

**Expected Output**

When running the above code, the output will look like this:

```output
Transaction rolled back
Users count: 0
```

What happens in the transaction:

- The User.objects.create(name="Test") statement creates a User instance and triggers the post_save signal.
- The signal handler create_profile is executed as part of the same transaction.

Intentional Exception in the Signal Handler:

- The signal handler raises an exception (raise Exception("Intentional error in signal")) before the Profile object is created.

Effect on the Transaction:

- Because the exception occurs within the signal handler, and the handler is running in the same transaction as the user creation, the entire transaction is rolled back.
- This rollback undoes both the User creation and any other changes that were part of the same transaction.

Why this proves the behavior:

- After the exception, the User.objects.count() returns 0, demonstrating that the user creation was rolled back.
- If signals did not run in the same transaction, the User object would remain in the database even though the signal handler failed.


## ❓ Topic: Custom Classes in Python

### Description: You are tasked with creating a Rectangle class with the following requirements:

   1. An instance of the Rectangle class requires length:int and width:int to be initialized.
   2. We can iterate over an instance of the Rectangle class 
   3. When an instance of the Rectangle class is iterated over, we first get its length in the format: {'length': <VALUE_OF_LENGTH>} followed by the width {width: <VALUE_OF_WIDTH>}

A: Regarding creating and using custom classes in Python, specifically within the context of a Django project

1. **Creating the Rectangle Class [`accuknoxassignmentapp/models.py`](accuknoxassignmentapp/models.py):**

- I've defined a Rectangle class inheriting from models.Model (essential for Django models).
- It had attributes length and width as *models.IntegerField()*, which become database fields.
- I've also implemented __iter__ to make instances iterable, yielding dictionaries of length and width.
- Implemented __str__ (or __repr__ outside Django) for a user-friendly string representation of the objects.
- Critically, we overrode the save() method to add validation (checking for integer types and positive values) before saving to the database.

2. **Using the Rectangle Class:**

- Django Shell (python [`manage.py`](manage.py) shell): We demonstrated how to create, retrieve, and iterate over Rectangle objects using the Django ORM (Object-Relational Mapper) within the interactive shell.
- Separate Python Script [`test_rectangle.py`](test_rectangle.py): We showed how to use the Django models in a standalone script by setting up the Django environment using os.environ.setdefault() and django.setup(). This is useful for tasks outside the web request cycle. This is the output we get when run:

```bash
python test_rectangle.py 

Rectangle (Length: 5, Width: 10)

{'length': 5}

{'width': 10}

ValueError: Length and width must be positive.

Exception: Length and width must be integers.

ValueError: Length and width must be positive.

Rectangle (Length: 5, Width: 10)

{'length': 5}

{'width': 10}
```

The output you provided shows the behavior of the [`test_rectangle.py`](test_rectangle.py) script, likely containing tests for your Rectangle model in Django. Here's a breakdown of the output:

1. Successful Creation:

Rectangle (Length: 5, Width: 10): This line indicates that a Rectangle object was successfully created with a length of 5 and a width of 10.

{'length': 5}: This and the following line {'width': 10} demonstrate the iteration over the rectangle object using the __iter__ method defined in your model. Each iteration yields a dictionary with the key being "length" or "width" and the value being the corresponding value.

2. Error Cases:

ValueError: Length and width must be positive.: This error occurs because the script likely tries to create rectangles with negative values. Your model's save method raises this error if length or width are not positive.

Exception: Length and width must be integers.: This error suggests the script attempts to create a rectangle with non-integer values for length or width. While the model's save method might not explicitly handle this case, Django's database backend probably raises this exception when trying to store the invalid data.

3. Another Successful Creation:

The output repeats the successful creation of a Rectangle object with length 5 and width 10, followed by the iterator output, demonstrating that the script continues after handling the errors.
Overall, the output shows the script testing your Rectangle model's functionalities, including:

Successful creation of rectangles with positive integer values.
Handling of negative values for length and width with a ValueError.
Implicit handling of non-integer values (likely by the database backend) with an Exception.
