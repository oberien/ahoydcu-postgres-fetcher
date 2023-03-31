# Ahoy Postgres Fetcher

Tested against AhoyDTU version 0.5.66 with a HM-800 with 2 modules.

### Setup postgres

```sql
-- Create User
CREATE USER pv;

-- Create Database
CREATE DATABASE pv OWNER pv;
REVOKE CONNECT ON DATABASE pv FROM PUBLIC;

-- connect to db
\c pv

-- Create Tables
SET ROLE pv;
CREATE TABLE measurements (
    timestamp timestamp PRIMARY KEY,
    ac_voltage float4 NOT NULL,
    ac_current float4 NOT NULL,
    ac_power float4 NOT NULL,
    ac_frequency float4 NOT NULL,
    ac_power_factor float4 NOT NULL,
    ac_temperature float4 NOT NULL,
    ac_yield_total float4 NOT NULL,
    ac_yield_day float4 NOT NULL,
    ac_power_dc float4 NOT NULL,
    ac_efficiency float4 NOT NULL,
    ac_reactive_power float4 NOT NULL,
    ac_power_limit float4 NOT NULL,

    a_voltage float4 NOT NULL,
    a_current float4 NOT NULL,
    a_power float4 NOT NULL,
    a_yield_day float4 NOT NULL,
    a_yield_total float4 NOT NULL,
    a_irradiation float4 NOT NULL,

    b_voltage float4 NOT NULL,
    b_current float4 NOT NULL,
    b_power float4 NOT NULL,
    b_yield_day float4 NOT NULL,
    b_yield_total float4 NOT NULL,
    b_irradiation float4 NOT NULL
);
```

### Installation

```sh
sudo install -D -m 755 -o root -g root ahoydtu-postgres-fetcher.py /usr/local/bin/
sudo install -D -m 644 -o root -g root ahoydtu-postgres-fetcher.cron /etc/cron.d/ahoydtu-postgres-fetcher
```
