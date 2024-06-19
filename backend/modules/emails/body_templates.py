from modules.apartments.models import Apartment, ApartmentDetails


def get_single_offer_template(apart: Apartment):
    return f"""
            <li>
                <strong>{apart.title}</strong><br>
                Price: {apart.price}<br>
                Address: {apart.address}<br>
                Rooms: {apart.rooms}<br>
                Area: {apart.area} m²<br>
                Floor: {apart.floor}<br>
                Status: {apart.status}<br>
                Link: {apart.subpage}
            </li>    
            """


def get_message_template(offers: list[Apartment]):
    return (
            """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Apartment Offers</title>
            <style>
                /* Add your custom styles here */
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    padding: 20px;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
                .offer {
                    font-size: 18px;
                    margin-bottom: 20px;
                }
                .cta-button {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Exclusive Apartment Offers!</h1>
                <p class="offer">Check out our latest apartment deals:</p>
                <ul>"""
            + (
                "\n".join(
                    list(get_single_offer_template(item) for item in offers)
                )
            )
            + """
            </ul>
            <p>Don't miss out! Click below to explore these amazing apartments:</p>
            <a href="{{ subpage }}" class="cta-button">Explore Apartments</a>
        </div>
    </body>
    </html>"""
    )
