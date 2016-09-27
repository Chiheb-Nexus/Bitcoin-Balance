#!/usr/bin/python3
#
#  This script use blockr.io API to fetch bitcoin addresses balance.
#
#  Copyright 2016 Chiheb Nexus
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from urllib.request import urlopen
from json import loads
import argparse, sys

class CheckAddress:
    def __init__(self, args):
        self.explorer = "http://btc.blockr.io/api/v1/address/info/"

        parser = argparse.ArgumentParser(description = """
        This script use blockr.io API to fetch bitcoin addresses balance.
        """)

        parser.add_argument('-F', '--file', help = "The path of the stored Bitcoin addresses file",\
        required = True, default = "addresses" )

        parser.add_argument('-O', '--out', help = "Output file name. PS: out_file will be stored within the script directory",\
        required = True, default = "balance_add")

        argument = parser.parse_args()
        self.in_file, self.out_file = argument.file, argument.out
        self.load()

    def check(self, address = ""):
        try:
            response = urlopen(self.explorer + address)
            data = loads(response.read().decode("utf8"))
            return data

        except Exception as e:
            print("Error occured during fetching addresses balance\n", e)
            return None

    def load(self):
        try:
            with open(self.in_file, 'r') as in_file:
                d = in_file.readlines()

                for add in d:
                    data = self.check(address = add)
                    print("%s : %s BTC" % (add.replace("\n", ""), data["data"]["balance"]))

                    with open(self.out_file, 'a') as out_file:
                        out_file.write("%s : %s BTC\n" % (add.replace("\n", ""), data["data"]["balance"]))
        except Exception as e:
            print("Error occured during importing addresses from file.\nPlease enter a valid path file.\n", e)

# Run the script !
if __name__ == '__main__':
    app = CheckAddress(sys.argv[1:])
