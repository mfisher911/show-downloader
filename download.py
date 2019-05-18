#!/usr/bin/env python3.7
"""Automate downloading radio shows from their show archive site.

Fairly specific to my needs (hard-coded day / show time).

Must define WEBHOST in the environment, which is just a bare FQDN
(like "www.google.com").

"""


from datetime import date, datetime
import math
import netrc
import os
import click
import requests
from tqdm import tqdm

try:
    WEBHOST = os.environ['WEBHOST']
except:
    raise KeyError("WEBHOST environment variable not defined")


@click.command()
@click.option('--showdate', default=str(date.today()),
              help='Show date to download')
def download(showdate):
    sd = datetime.strptime(showdate, '%Y-%m-%d')
    if sd.weekday() == 1:  # "Shift Change", 13:00 on Tuesday
        st = '1300'
    elif sd.weekday() == 5:  # "Still I Rise", 10:30 on Saturday
        st = '1000'
    else:
        raise ValueError(f'{sd.strftime("%Y-%m-%d-%a")} not on Tue/Sat')
    filename = f"{sd.strftime('%Y-%m-%d-%a')}-{st}.mp3"

    login = netrc.netrc().authenticators(WEBHOST)
    s = requests.Session()
    payload = {'username': login[0], 'password': login[2]}
    s.post(f'https://{WEBHOST}/login', json=payload)
    print(f'logged in as {login[0]} for {WEBHOST}')
    print(f'downloading {filename}')
    r = s.get(f'https://{WEBHOST}/airchecks?file={filename}',
              stream=True)

    length = int(r.headers.get('Content-Length', 0))
    bs = 1024 * 1024

    with open(filename, 'wb') as fd:
        for chunk in tqdm(r.iter_content(chunk_size=bs),
                          total=math.ceil(length//bs),
                          unit_divisor=1024,
                          unit='MB', unit_scale=True):
            fd.write(chunk)


if __name__ == '__main__':
    download()
