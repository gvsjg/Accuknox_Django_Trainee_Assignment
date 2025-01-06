import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accuknox_assignment.settings')  # Replace 'assignment.settings' with your project's settings file
django.setup()

from accuknoxassignmentapp.models import Rectangle

try:
    rect1 = Rectangle.objects.create(length=5, width=10)
    print(rect1)
    for item in rect1:
        print(item)

    rect2 = Rectangle.objects.create(length=-5, width=10)
except ValueError as e:
    print(f"ValueError: {e}")

try:
    rect3 = Rectangle.objects.create(length=5, width="10")
except Exception as e:
    print(f"Exception: {e}")

try:
    rect4 = Rectangle.objects.create(length=0,width=10)
except ValueError as e:
    print(f"ValueError: {e}")

rects = Rectangle.objects.all()
for rect in rects:
    print(rect)
    for item in rect:
        print(item)