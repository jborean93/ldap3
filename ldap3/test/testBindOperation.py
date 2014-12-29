# Created on 2013.06.06
#
# @author: Giovanni Cannata
#
# Copyright 2015 Giovanni Cannata
#
# This file is part of ldap3.
#
# ldap3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ldap3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ldap3 in the COPYING and COPYING.LESSER files.
# If not, see <http://www.gnu.org/licenses/>.

import unittest

from ldap3 import Server, Connection, ServerPool, AUTH_ANONYMOUS, AUTH_SASL, STRATEGY_REUSABLE_THREADED
from test import test_server, test_port, test_user, test_password, test_authentication, test_strategy, test_port_ssl,\
    test_lazy_connection, test_pooling_strategy, test_pooling_active, test_pooling_exhaust,\
    test_get_info, test_server_mode, test_sasl_user, test_sasl_password

class Test(unittest.TestCase):
    def test_bind_clear_text(self):
        if isinstance(test_server, (list, tuple)):
            server = ServerPool(pool_strategy=test_pooling_strategy, active=test_pooling_active, exhaust=test_pooling_exhaust)
            for host in test_server:
                server.add(Server(host=host, port=test_port, allowed_referral_hosts=('*', True), get_info=test_get_info, mode=test_server_mode))
        else:
            server = Server(host=test_server, port=test_port, allowed_referral_hosts=('*', True), get_info=test_get_info, mode=test_server_mode)
        connection = Connection(server, auto_bind=False, version=3, client_strategy=test_strategy, user=test_user, password=test_password, authentication=test_authentication, lazy=test_lazy_connection, pool_name='pool1')
        connection.open()
        connection.bind()
        self.assertTrue(connection.bound)
        connection.unbind()
        if connection.strategy_type == STRATEGY_REUSABLE_THREADED:
            connection.strategy.terminate()
        self.assertFalse(connection.bound)

    def test_bind_ssl(self):
        if isinstance(test_server, (list, tuple)):
            server = ServerPool(pool_strategy=test_pooling_strategy, active=test_pooling_active, exhaust=test_pooling_exhaust)
            for host in test_server:
                server.add(Server(host=host, port=test_port, allowed_referral_hosts=('*', True), get_info=test_get_info, mode=test_server_mode))
        else:
            server = Server(host=test_server, port=test_port_ssl, use_ssl=True, get_info=test_get_info, mode=test_server_mode)
        connection = Connection(server, auto_bind=False, version=3, client_strategy=test_strategy, user=test_user, password=test_password, authentication=test_authentication, pool_name='pool1')
        connection.open()
        connection.bind()
        self.assertTrue(connection.bound)
        connection.unbind()
        if connection.strategy_type == STRATEGY_REUSABLE_THREADED:
            connection.strategy.terminate()
        self.assertFalse(connection.bound)

    def test_bind_anonymous(self):
        if isinstance(test_server, (list, tuple)):
            server = ServerPool(pool_strategy=test_pooling_strategy, active=test_pooling_active, exhaust=test_pooling_exhaust)
            for host in test_server:
                server.add(Server(host=host, port=test_port, allowed_referral_hosts=('*', True), get_info=test_get_info, mode=test_server_mode))
        else:
            server = Server(host=test_server, port=test_port, get_info=test_get_info, mode=test_server_mode, connect_timeout=1)
        connection = Connection(server, auto_bind=False, version=3, client_strategy=test_strategy, authentication=AUTH_ANONYMOUS, lazy=False, pool_name='pool1')
        connection.open()
        connection.bind()
        self.assertTrue(connection.bound)
        connection.unbind()
        if connection.strategy_type == STRATEGY_REUSABLE_THREADED:
            connection.strategy.terminate()
        self.assertFalse(connection.bound)

    def test_bind_sasl_digest_md5(self):
        if isinstance(test_server, (list, tuple)):
            server = ServerPool(pool_strategy=test_pooling_strategy, active=test_pooling_active, exhaust=test_pooling_exhaust)
            for host in test_server:
                server.add(Server(host=host, port=test_port, allowed_referral_hosts=('*', True), get_info=test_get_info, mode=test_server_mode))
        else:
            server = Server(host=test_server, port=test_port, get_info=test_get_info, mode=test_server_mode)
        connection = Connection(server, auto_bind=False, version=3, client_strategy=test_strategy, authentication=AUTH_SASL, sasl_mechanism='DIGEST-MD5', sasl_credentials=(None, test_sasl_user, test_sasl_password, None), pool_name='pool1')
        connection.open()
        connection.bind()
        self.assertTrue(connection.bound)
        connection.unbind()
        if connection.strategy_type == STRATEGY_REUSABLE_THREADED:
            connection.strategy.terminate()
        self.assertFalse(connection.bound)
