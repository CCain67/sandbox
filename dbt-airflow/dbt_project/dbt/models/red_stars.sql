{{config(materialized='table')}}

with stars as (
    select * from {{ source('public','stars') }}
)

select *, CURRENT_TIMESTAMP as query_timestamp
from stars
where star_color = 'Red'