# TODO: swagger file
# TODO: API Gateway
# TODO: API Gateway authentication: http://docs.aws.amazon.com/apigateway/latest/developerguide/use-custom-authorizer.html
# TODO: create swimlane branches; merge everything
# TODO: Send email
# TODO: get answers to QUESTIONs
# TODO: add data integrity check scripts
# TODO: add Google-riffic docstrings everywhere
# TODO: HTTP response codes
"""
Copyright (C) 2016 Ben Reece

This program is free software; you can redistribute it and/or
modify it under the terms of version 2 of the GNU General Public
License as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""


class ClientErrorException(Exception):
    """ Client error """
    pass
