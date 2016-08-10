#!/usr/bin/python3.5
import gcalender
import telegram

def Main():
    # get all the data from the google calender
    EventList = gcalender.main()

    print(EventList)
    print('Relieved all the calender events')

    telegram.main(EventList)

if __name__ == '__main__':
    print('Starting the TesLAN Telegram Python (3.5) script')
    print('Please stay tuned ...')
    Main()

