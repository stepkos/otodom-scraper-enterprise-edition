# Otodom Scraper Enterprise Edition

The project focuses on scraping, storing and evaluating apartments from the advertisements from the otodom.pl service.

The repository was named "Enterprise Edition" because the software has been expanded to enable cyclical searches of the website with advertisements, apartment valuations and sending email notifications with the most attractive ones.

Real estate valuation model is trained on the data from scraper. Whole analysis and training process is available <br/>
here: [stepkos/real-estate-price-valuation](https://github.com/stepkos/real-estate-price-valuation)

## Tech Stack

- Python, Django - backend base, admin panel
- Celery, Redis - asynchronous tasks
- Postgres - database
- PyTorch - AI real estate valuation model
- Docker, Docker Compose - containerization

## From the user's side

To start tracking the offers, the user can setup configuration via the admin panel. 

The user can specify:
- Frequency of the search
- Link to otodom website with applied filters
- Email address/es to which the results will be sent
- Attractive price threshold (how much below market price is the apartment attractive)
- Limit of pages while scraping

As a result user receives email with attractive apartments from the last search.

<p>
  <img src="https://github.com/stepkos/otodom-scraper-enterprise-edition/blob/main/docs/screens/result_email.jpg" alt="Result email screen" width="530">
</p>

## Authors

- **Jakub Stępkowski [(github: stepkos)](https://github.com/stepkos/)**
- **Szymon Kowaliński [(github: simon-the-shark)](https://github.com/simon-the-shark)**

## License
This software was created for educational purposes only. Authors do not take any responsibility for any consequences resulting from the use or execution of this software.

Django template based on [template from saasitive](https://github.com/saasitive/docker-compose-django-celery-redis-postgres/)
