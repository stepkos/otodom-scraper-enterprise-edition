from modules.apartments.models import Apartment


def get_single_offer_template(apart: Apartment):
    return f"""
        <tr>
            <td><strong>{apart.title}</strong></td>
            <td>Price: {apart.price}</td>
            <td>Address: {apart.address}</td>
            <td>Rooms: {apart.rooms}</td>
            <td>Area: {apart.area} m²</td>
            <td>Floor: {apart.floor}</td>
            <td>Status: {apart.status}</td>
            <td><a href="{apart.get_abs_details_url()}">Link</a></td>
        </tr>
    """


def get_message_template(offers: list[Apartment]):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Apartment Offers</title>
            <style>
                /* Add your custom styles here */
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    padding: 20px;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                .offer {{
                    font-size: 18px;
                    margin-bottom: 20px;
                }}
                .cta-button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 5px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    padding: 8px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Exclusive Apartment Offers!</h1>
                <p class="offer">Check out our latest apartment deals:</p>
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Price</th>
                            <th>Address</th>
                            <th>Rooms</th>
                            <th>Area</th>
                            <th>Floor</th>
                            <th>Status</th>
                            <th>Link</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(get_single_offer_template(item) for item in offers)}
                    </tbody>
                </table>
                <p>Don't miss out! Click below to explore these amazing apartments:</p>
                <a href="{offers[0].subpage}" class="cta-button">Explore Apartments</a>
            </div>
        </body>
        </html>
    """
