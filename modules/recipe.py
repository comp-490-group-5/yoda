import requests
import click

def get_weather(location):
    # parsing location
    # the way the user enters the location does not matter as wttr
    # does a good job handling the text on it's own.

    #'+' replaces the white space as this is tested to work better with wttr
    location = location.strip().replace(" ", "+")

    weather_service = "http://wttr.in/"

    response = requests.get(weather_service + location)
    click.echo(response.text)