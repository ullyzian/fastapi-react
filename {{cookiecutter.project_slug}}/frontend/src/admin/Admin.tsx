import React, { FC } from 'react';
import { Admin as ReactAdmin, fetchUtils, Resource } from 'react-admin';
import simpleRestProvider from 'ra-data-simple-rest';
import authProvider from './authProvider';

import { UserCreate, UserEdit, UserList } from './Users';
import { ItemCreate, ItemList, ItemEdit } from './Items';

const httpClient = (url: any, options: any) => {
  if (!options) {
    options = {};
  }
  if (!options.headers) {
    options.headers = new Headers({ Accept: 'application/json' });
  }
  const token = localStorage.getItem('token');
  options.headers.set('Authorization', `Bearer ${token}`);
  return fetchUtils.fetchJson(url, options);
};

const dataProvider = simpleRestProvider('api/v1', httpClient);

export const Admin: FC = () => {
  return (
    <ReactAdmin dataProvider={dataProvider} authProvider={authProvider}>
      {(permissions: 'admin' | 'user') => [
        permissions === 'admin'
          ? [
              <Resource
                name="users"
                list={UserList}
                edit={UserEdit}
                create={UserCreate}
              />,
              <Resource
                name="items"
                list={ItemList}
                edit={ItemEdit}
                create={ItemCreate}
              />,
            ]
          : null,
      ]}
    </ReactAdmin>
  );
};
