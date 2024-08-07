# Otodom Scraper Enterprise Edition

The project focuses on scraping, storing and evaluating apartments from the advertisements from the otodom.pl service.

The repository was named "Enterprise Edition" because the software has been expanded to enable cyclical searches of the website with advertisements, apartment valuations and sending email notifications with the most attractive ones.

Real estate valuation model is trained on the data from scraper. Whole analysis and training process is available here: [stepkos/real-estate-price-valuation](https://github.com/stepkos/real-estate-price-valuation)

## Tech Stack

- Python, Django - backend base, admin panel
- Celery, Redis - asynchronous tasks
- Postgres - database
- PyTorch - AI real estate valuation model
- Docker, Docker Compose - containerization

## From the user's side

As a result user receives email with attractive apartments from the last search.

![Result email screen](https://github.com/stepkos/otodom-scraper-enterprise-edition/blob/main/docs/screens/result_email.jpg)

## Authors

- **Jakub Stępkowski [(github: stepkos)](https://github.com/stepkos/)**
- **Szymon Kowaliński [(github: simon-the-shark)](https://github.com/simon-the-shark)**

## License

...
Django template based on [template from saasitive](https://github.com/saasitive/docker-compose-django-celery-redis-postgres/)

