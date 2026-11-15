select city, governorate, latitude, longitude, population
from {{ ref('cities') }}
