# BoltTrip API - Validation Standards Reference

## Quick Reference Guide

### 1. Rating Fields (0-5 scale)

**Correct Implementation**:
```python
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

rating = models.DecimalField(
    max_digits=3,           # Max 999 (allows up to 5.0)
    decimal_places=1,       # One decimal place
    default=0.0,
    validators=[
        MinValueValidator(Decimal('0.0')),
        MaxValueValidator(Decimal('5.0'))
    ]
)
```

**Why max_digits=3?**
- `max_digits=2, decimal_places=1` → max value is 9.9 ❌ WRONG
- `max_digits=3, decimal_places=1` → max value is 99.9 (but limited to 5.0 by validator) ✅ CORRECT

---

### 2. Price Fields (Money)

**Correct Implementation**:
```python
from decimal import Decimal

price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    validators=[MinValueValidator(Decimal('0.00'))]
)
```

**Rules**:
- Always include `MinValueValidator(Decimal('0.00'))`
- max_digits should be 10 for flexibility
- decimal_places always 2 for cents

---

### 3. Age Fields

**Correct Implementation**:
```python
age = models.PositiveSmallIntegerField(
    blank=True,
    null=True,
    validators=[
        MinValueValidator(0),
        MaxValueValidator(110)  # Realistic human lifespan
    ]
)
```

**For Travel**:
```python
min_age = models.PositiveSmallIntegerField(
    blank=True,
    null=True,
    validators=[
        MinValueValidator(0),
        MaxValueValidator(110)
    ]
)
```

---

### 4. Duration Fields

**For Hours**:
```python
duration_hours = models.PositiveSmallIntegerField(
    default=1,
    validators=[
        MinValueValidator(1),  # At least 1 hour
        MaxValueValidator(24)  # Max 1 day
    ]
)
```

**For Days**:
```python
duration_days = models.PositiveSmallIntegerField(
    default=1,
    validators=[
        MinValueValidator(1),    # At least 1 day
        MaxValueValidator(365)   # Max 1 year
    ]
)
```

**For Minutes**:
```python
duration_minutes = models.PositiveIntegerField(
    validators=[
        MinValueValidator(1),     # At least 1 minute
        MaxValueValidator(1440)   # Max 24 hours
    ]
)
```

---

### 5. Capacity/Group Size Fields

**For Small Groups** (activities):
```python
max_group_size = models.PositiveSmallIntegerField(
    default=10,
    validators=[
        MinValueValidator(1),
        MaxValueValidator(50)  # Max 50 people
    ]
)
```

**For Larger Groups** (tours/packages):
```python
max_group_size = models.PositiveIntegerField(
    default=10,
    validators=[
        MinValueValidator(1),
        MaxValueValidator(500)  # Max 500 people
    ]
)
```

---

### 6. Room Capacity

```python
capacity = models.PositiveSmallIntegerField(
    default=2,
    validators=[
        MinValueValidator(1),   # Single bed minimum
        MaxValueValidator(20)   # Suite maximum
    ]
)
```

---

### 7. Experience Years

```python
years_of_experience = models.PositiveIntegerField(
    validators=[
        MinValueValidator(0),
        MaxValueValidator(70)  # Realistic career span
    ]
)
```

---

### 8. Travelers Count

**For Flight Search**:
```python
travelers = models.PositiveSmallIntegerField(
    default=1,
    validators=[
        MinValueValidator(1),
        MaxValueValidator(9)  # Most systems support 1-9
    ]
)
```

**For Bookings**:
```python
travelers_count = models.PositiveIntegerField(
    default=1,
    validators=[
        MinValueValidator(1),
        MaxValueValidator(500)
    ]
)
```

---

### 9. Quantity Fields

```python
quantity = models.PositiveIntegerField(
    default=1,
    validators=[MinValueValidator(0)]
)
```

**When you want to allow 0**:
```python
quantity = models.PositiveIntegerField(
    default=0,
    validators=[
        MinValueValidator(0),
        MaxValueValidator(1000)
    ]
)
```

---

### 10. Star Rating (1-5)

```python
star_rating = models.PositiveSmallIntegerField(
    default=0,
    validators=[
        MinValueValidator(0),  # Can be 0 if not rated
        MaxValueValidator(5)   # 1-5 star scale
    ]
)
```

---

## Serializer Level Validation

### Custom Field Validators

```python
from rest_framework import serializers

def validate_age(value):
    if value and value > 110:
        raise serializers.ValidationError(
            "Age must be realistic (max 110 years)."
        )
    return value

def validate_price(value):
    if value < 0:
        raise serializers.ValidationError(
            "Price cannot be negative."
        )
    return value

class MySerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(validators=[validate_age])
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_price]
    )
```

### Object-Level Validation

```python
class BookingSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError(
                "End date cannot be before start date."
            )
        if data['paid_amount'] > data['total_amount']:
            raise serializers.ValidationError(
                "Paid amount cannot exceed total amount."
            )
        return data
```

---

## Common Validation Mistakes

### ❌ WRONG
```python
# No validators
rating = models.DecimalField(max_digits=2, decimal_places=1)
price = models.DecimalField(max_digits=10, decimal_places=2)
age = models.PositiveSmallIntegerField()
```

### ✅ CORRECT
```python
# With validators
rating = models.DecimalField(
    max_digits=3,
    decimal_places=1,
    validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('5.0'))]
)
price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    validators=[MinValueValidator(Decimal('0.00'))]
)
age = models.PositiveSmallIntegerField(
    validators=[MinValueValidator(0), MaxValueValidator(110)]
)
```

---

## Import Requirements

```python
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
```

---

## Testing Validation

```python
import pytest
from django.core.exceptions import ValidationError

def test_rating_max_value():
    """Test rating field max value validation"""
    obj = MyModel(rating=6.0)  # Should fail
    with pytest.raises(ValidationError):
        obj.full_clean()

def test_price_negative():
    """Test price cannot be negative"""
    obj = MyModel(price=-10.00)  # Should fail
    with pytest.raises(ValidationError):
        obj.full_clean()

def test_age_max_value():
    """Test age field max value"""
    obj = MyModel(age=150)  # Should fail
    with pytest.raises(ValidationError):
        obj.full_clean()
```

---

## Database Constraints

After making model changes, create and run migrations:

```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Verify constraints in database
python manage.py dbshell
```

---

## Related Documentation

- [Django Validators](https://docs.djangoproject.com/en/4.2/ref/validators/)
- [Django DecimalField](https://docs.djangoproject.com/en/4.2/ref/models/fields/#decimalfield)
- [DRF Field Validators](https://www.django-rest-framework.org/api-guide/fields/#validators)

---

**Last Updated**: March 19, 2026
