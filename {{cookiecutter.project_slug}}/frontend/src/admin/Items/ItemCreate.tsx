import React, { FC } from "react";
import { Create, SimpleForm, TextInput, NumberInput } from "react-admin";

export const ItemCreate: FC = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="title" />
      <TextInput multiline source="description" initialValue="Lorem Ipsum" />
      <NumberInput source="quantity" initialValue="1" />
      <NumberInput source="price" initialValue="1.00" />
    </SimpleForm>
  </Create>
);
