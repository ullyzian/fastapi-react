import React, { FC } from 'react';
import {
    Edit,
    SimpleForm,
    TextInput,
    NumberInput,
} from 'react-admin';

export const ItemEdit: FC = (props) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
      <TextInput source="title" />
      <TextInput multiline source="description" />
      <NumberInput source="quantity" />
      <NumberInput source="price" />
    </SimpleForm>
  </Edit>
);
