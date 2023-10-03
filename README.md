# Kiwi.com search API wrapper library
This wrapper library is a personal project and has no affiliation with Kiwi.com

## Account
The API is restricted by API key, so one has to create an account at https://tequila.kiwi.com/ . AFAIK, no human-in-the-loop approval process is required, so the creation is pretty much instant.

set the API key as env variable
```
export KIWI_APIKEY="..."
```

## Library Usage
This is a very experimental release, so the usage may change dramatically in the future.

```python
In [1]: from kiwi_berry.search import SearchParams, Client

In [2]: import asyncio

In [3]: query = SearchParams(fly_from='FRA', fly_to='HKT', date_from='2023-11-20', date_to='2023-11-30', adults=1, limit=10,sort='price')

In [4]: resp = asyncio.run(Client().search(query))

In [5]: resp.show()
+---- 471.0 ----
 \ 2023-11-29 FRA-DOH 20:40 \ QR 72
  \ 2023-11-30 DOH-HKT 08:30 \ QR 846

+---- 471.0 ----
 \ 2023-11-28 FRA-DOH 20:40 \ QR 72
  \ 2023-11-29 DOH-HKT 08:30 \ QR 846

+---- 473.0 ----
 \ 2023-11-27 FRA-DOH 20:40 \ QR 72
  \ 2023-11-28 DOH-HKT 08:30 \ QR 846

+---- 489.0 ----
 \ 2023-11-20 FRA-DOH 20:40 \ QR 72
  \ 2023-11-21 DOH-HKT 08:30 \ QR 846

+---- 489.0 ----
 \ 2023-11-23 FRA-DOH 20:40 \ QR 72
  \ 2023-11-24 DOH-HKT 08:30 \ QR 846

+---- 491.0 ----
 \ 2023-11-22 FRA-DOH 20:40 \ QR 72
  \ 2023-11-23 DOH-HKT 08:30 \ QR 846

+---- 491.0 ----
 \ 2023-11-26 FRA-DOH 20:40 \ QR 72
  \ 2023-11-27 DOH-HKT 08:30 \ QR 846

+---- 778.0 ----
 \ 2023-11-27 FRA-BKK 13:45 \ TG 921
  \ 2023-11-28 BKK-HKT 07:40 \ WE 2289

+---- 865.0 ----
 \ 2023-11-28 FRA-BKK 13:45 \ TG 921
  \ 2023-11-29 BKK-HKT 07:40 \ WE 2289

+---- 900.0 ----
 \ 2023-11-20 FRA-BKK 13:45 \ TG 921
  \ 2023-11-21 BKK-HKT 07:40 \ WE 2289


```
