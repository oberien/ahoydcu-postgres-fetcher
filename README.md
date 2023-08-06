# AhoyDTU Postgres Fetcher

# Superseded by [iot2db](https://github.com/oberien/iot2db)

Migration:
* setup and configure AhoyDTU and iot2db as explained in the iot2db AhoyDTU device example
* modify the postgres from within `psql` like this:
    ```sql
    SET ROLE airq;
    DROP INDEX measurements_persistent;
    -- use the create table command from the iot2db documentation with a different name
    CREATE TABLE measurements2 (...) PARTITION BY ...;
    BEGIN TRANSACTION;
    LOCK TABLE measurements;
    ALTER TABLE measurements RENAME TO measurements_old;
    INSERT INTO measurements2 (
        timestamp, persistent, ac_voltage, ac_current, ac_power, ac_frequency, ac_power_factor, ac_temperature, ac_yield_total, ac_yield_day, ac_power_dc, ac_efficiency, ac_reactive_power, ac_power_limit, a_voltage, a_current, a_power, a_yield_day, a_yield_total, a_irradiation, b_voltage, b_current, b_power, b_yield_day, b_yield_total, b_irradiation
    ) SELECT timestamp, persistent, ac_voltage, ac_current, ac_power, ac_frequency, ac_power_factor, ac_temperature, ac_yield_total, ac_yield_day, ac_power_dc, ac_efficiency, ac_reactive_power, ac_power_limit, a_voltage, a_current, a_power, a_yield_day, a_yield_total, a_irradiation, b_voltage, b_current, b_power, b_yield_day, b_yield_total, b_irradiation FROM measurements_old;
    ALTER TABLE measurements2 RENAME TO measurements;
    COMMIT;
    DROP TABLE measurements_old;
    ```

---

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
    timestamp timestamp with time zone PRIMARY KEY NOT NULL,
    persistent bool NOT NULL,
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
CREATE INDEX IF NOT EXISTS measurements_persistent ON measurements (timestamp) where persistent = false;
```

### Installation

```sh
sudo install -D -m 755 -o root -g root ahoydtu-postgres-fetcher.py /usr/local/bin/
sudo install -D -m 644 -o root -g root ahoydtu-postgres-fetcher.service /usr/lib/systemd/system/
```
