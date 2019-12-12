### About project
Simple API for converting currencies. Celery task periodically (once in 30 seconds) 
fetches actual data from https://openexchangerates.org  and saves it to DB.

All secrets are stored in repo, containers run as root and DB instance, redis and 
celery worker/beat are left unconfigured for the sake of simplicity


#### How to test and measure coverage
Run `docker-compose run --rm test` for testing. Open `currency_converter/htmlcov/index.html`
to see coverage results

#### How to run
```
docker-compose up
```
#### How to check
- `/api/rates` - returns all rates in paginated form(limit & offset style). Single page contains  
  100 items. Run: `curl localhost:8000/api/rates`
- `/api/convert` - converts amount from one currency  to another.   

   Run: `curl "localhost:8000/api/convert?source_currency=USD&destination_currency=EUR&amount=500"`
