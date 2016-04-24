#!/usr/bin/python3

from Adafruit_IO import Client
import os
import logging

SPEEDTEST_CMD = '/usr/local/bin/speedtest'          # Location of speedtest script - CHANGE FOR YOUR SETUP
LOG_FILE = '/home/user/speedtest.log'              # Location of log file - CHANGE FOR YOUR SETUP
aio = Client('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')    # Setup Adafruit.io rest client with YOUR CLIENT KEY


def main():
    # print("I am in main")  # For debugging
    setup_logging()
    logging.info('Finished setting up logging.')
    logging.info('Going to speedtest function.')
    try:
        ping, download, upload = get_speedtest_results()  # Assign results from get_speed_test tuple to variables
        logging.info('Received values from speedtest_results.')
        logging.info('Sending Upload value to Adafruit.io')
        aio.send('Upload', upload)  # Use Adafruit rest client to send upload to Upload Feed
        logging.info('Sending Download value to Adafruit.io')
        aio.send('Download', download)  # Use Adafruit rest client to send Download to Download Feed
        logging.info('Sending Latency value to Adafruit.io')
        aio.send('Ping', ping)  # Use Adafruit rest client to send Ping to Ping Feed
    except ValueError as err:
        logging.info(err)
    else:
        logging.info("%5.1f %5.1f %5.1f", ping, download, upload)
        logging.info('All values sent to Adafruit.IO successfully')


def setup_logging():
    # print("setup logging")  # For debugging
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M"
    )
    # print("leaving logging")   # For debugging


def get_speedtest_results():
    """
    Run test and parse results.
    Returns tuple of ping speed, download speed and upload speed,
    or raises ValueError if unable to parse data.
    """
    # print("I am in get speed")  # For debugging
    logging.info('Starting speedtest.')
    ping = download = upload = None
    # print(str(ping) + ' ' + str(download) + ' ' + str(upload))  # For debugging
    with os.popen(SPEEDTEST_CMD + ' --simple') as speedtest_output:
        for line in speedtest_output:
            label, value, unit = line.split()
            if 'Ping' in label:
                ping = float(value)
                logging.info('Ping value is:' + ' ' + str(ping))
                # print(ping)  # For debugging
            elif 'Download' in label:
                download = float(value)
                logging.info('Download value is:' + ' ' + str(download))
                # print(download)  # For debugging
            elif 'Upload' in label:
                upload = float(value)
                logging.info('Upload value is:' + ' ' + str(upload))
                # print(upload)  # For debugging
    if all((ping, download, upload)):  # if all 3 values were parsed
        logging.info('Finished running the speedtest.')
        return ping, download, upload
    else:
        raise ValueError('TEST FAILED')


if __name__ == '__main__':
    main()

