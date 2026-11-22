{#
    Macro: cents_to_dollars
    Converts an amount stored in cents to dollars with rounding.
    Demonstrates reusable Jinja SQL macros in dbt.
#}
{% macro cents_to_dollars(column_name, decimal_places=2) -%}
    round(cast({{ column_name }} as double) / 100.0, {{ decimal_places }})
{%- endmacro %}
