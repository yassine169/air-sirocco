select
    city,
    cast("time" as timestamp)     as measured_at,
    cast(pm2_5 as double)         as pm2_5,
    cast(pm10 as double)          as pm10,
    cast(dust as double)          as dust,
    cast(nitrogen_dioxide as double) as no2,
    cast(ozone as double)         as ozone,
    cast(ingested_at as timestamp) as ingested_at,
    city || '_' || "time"         as air_id
from {{ source('raw', 'air_quality') }}
