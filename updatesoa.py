#!/usr/bin/python3
# File: updatesoa.py
# Authors: Bert JW Regeer <bertjw@regeer.org>, Leon M Lohse <llohse@kellnerweg.de>
# Created: 2013-02-15
# Updated: 2014-09-31


import os.path
import re
import datetime
import argparse

soa_regex = re.compile(r"@\s+((?P<record_ttl>[0-9]+[a-z]*)\s+)?IN\s+SOA\s+(?P<ns>[\w\.]+)\s+(?P<hostmaster>[\w\.]+)\s*\(\s*(;.*$)?"+
                      r"\s*(?P<serial>\d+)\s*(;.*$)?"+
                      r"\s*(?P<refresh>\d+)\s*(;.*$)?"+
                      r"\s*(?P<retry>\d+)\s*(;.*$)?"+
                      r"\s*(?P<expire>\d+)\s*(;.*$)?"+
                      r"\s*(?P<minttl>\d+)\s*(;.*$)?"
                      r"\s*\)\s*(;.*$)?", re.MULTILINE)
serial_regex = re.compile(r"(?P<date>[0-9]{8})(?P<inc>[0-9]{2})")

# Template
soa_record = """\
@ IN SOA {ns} {hostmaster} (
         {serial} ; Serial number
         {refresh} ; Refresh
         {retry} ; Retry
         {expire} ; Expiration
         {minttl} ; Min TTL
)"""


def main(zonefile, write):

    if os.path.isfile(zonefile) is False:
        print('Zonefile "{zf}" doesn\'t exist'.format(zf=zonefile))
        exit(-1)

    with open(zonefile, "r+") as f:
        zone = f.read()
        regsearch = soa_regex.search(zone)

        if not regsearch:
            print(zone)
            print('SOA not found.')
            exit(-1)

        oldsoastring = regsearch.group(0) 
        print('')
        print('Old SOA record:')
        print(oldsoastring)

        soa = regsearch.groupdict()

        cur_date = datetime.datetime.utcnow().strftime("%Y%m%d")
        serialmatch = serial_regex.match(soa['serial'])

        if not serialmatch:
            print('WARNING: Malformed serial!')
            serial = { 'date' : cur_date, 'inc' : 0 }

        else:
            serial = serialmatch.groupdict()
            if serial['date'] == cur_date:
                print('The SOA record has already been updated today... incrementing')
                serial['inc'] = int(serial['inc']) + 1
            else:
                serial['inc'] = int(serial['inc'])

            serial['date'] = cur_date

        soa['serial'] = '{date}{inc:0=2d}'.format(**serial)

        print('')
        print('New SOA record:')
        print(soa_record.format(**soa))

        print('')
        if not write:
            print('Not writing zone to disk.')
            exit(0)

        new_zone = soa_regex.sub(soa_record.format(**soa), zone)
        f.seek(0)
        f.truncate(0)
        f.write(new_zone)

        print('')
        print('Zone has been updated.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('zonefile')
    parser.add_argument('--write', action='store_true')

    args = parser.parse_args()

    main(args.zonefile, args.write)

