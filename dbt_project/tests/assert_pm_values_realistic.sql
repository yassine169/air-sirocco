-- Échoue si une valeur de particules est négative ou absurde
select *
from {{ ref('fct_air_hourly') }}
where pm2_5 < 0 or pm2_5 > 1000
   or pm10  < 0 or pm10  > 2000
