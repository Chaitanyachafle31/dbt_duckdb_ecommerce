{#
    Custom schema naming macro.
    By default, dbt prepends target.schema (e.g. 'main_staging').
    In DuckDB Medallion architecture, we want clean, dedicated schemas:
    - raw
    - staging
    - intermediate
    - marts
#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
