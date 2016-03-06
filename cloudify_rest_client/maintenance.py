########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


class MaintenanceModeClient(object):

    def __init__(self, api):
        self.api = api

    def post(self, state):
        """
        Activates and deactivates maintenance mode.

        :param
        :return:
        """
        assert state
        uri = '/maintenance/{0}'.format(state)
        response = self.api.post(uri)
        return response
