########
# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
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

from cloudify_rest_client.responses import ListResponse


class DeploymentUpdate(dict):

    def __init__(self, update):
        self.update(update)

    @property
    def id(self):
        """Deployment update id"""
        return self['id']

    @property
    def state(self):
        """Deployment update status"""
        return self['state']

    @property
    def deployment_id(self):
        """Deployment Id the outputs belong to."""
        return self['deployment_id']

    @property
    def steps(self):
        return self['steps']


class DeploymentUpdatesClient(object):

    def __init__(self, api):
        self.api = api

    def list(self, deployment_id=None, _include=None, **kwargs):
        """List deployment updates

        :param deployment_id: The deployment id (optional)
        :param kwargs: Optional filter fields. for a list of available fields
               see the REST service's models.DeploymentUpdate.fields
        """

        params = {}
        if deployment_id:
            params['deployment_id'] = deployment_id
        params.update(kwargs)
        uri = '/deployment-updates'

        response = self.api.get(uri, params=params, _include=_include)
        items = [DeploymentUpdate(item) for item in response['items']]
        return ListResponse(items, response['metadata'])

    def stage(self, deployment_id, blueprint=None):
        """Create a deployment update transaction.

        :param deployment_id: The deployment id
        :return: DeploymentUpdate dict
        :rtype: DeploymentUpdate
        """

        assert deployment_id
        data = {
            'deployment_id': deployment_id
        }
        if blueprint is not None:
            data['blueprint'] = blueprint

        uri = '/deployment-updates'
        response = self.api.post(uri, data,
                                 expected_status_code=201)
        return DeploymentUpdate(response)

    def get(self, update_id, _include=None):
        """Get  deployment update

        :param update_id: The update id
        """
        uri = '/deployment-updates/{0}'.format(update_id)
        response = self.api.get(uri, _include=_include)
        return DeploymentUpdate(response)

    def step(self, update_id, operation, entity_type, entity_id):
        assert update_id
        uri = '/deployment-updates/{0}/step'.format(update_id)
        response = self.api.post(uri,
                                 data=dict(operation=operation,
                                           entity_type=entity_type,
                                           entity_id=entity_id))
        return DeploymentUpdate(response)

    def add(self, update_id, entity_type, entity_id):
        return self.step(update_id,
                         operation='add',
                         entity_type=entity_type,
                         entity_id=entity_id)

    def remove(self, update_id, entity_type, entity_id):
        return self.step(update_id,
                         operation='remove',
                         entity_type=entity_type,
                         entity_id=entity_id)

    def commit(self, update_id):
        """Finish deployment update

        :param update_id: The update id
        """

        assert update_id
        uri = '/deployment-updates/{0}/commit'\
            .format(update_id)
        response = self.api.post(uri)
        return DeploymentUpdate(response)

    def rollback(self, update_id):
        """Rollback deployment update

        :param update_id: The update id
        """

        assert update_id
        uri = '/deployment-updates/{0}/revert'.format(update_id)
        response = self.api.post(uri)
        return DeploymentUpdate(response)
