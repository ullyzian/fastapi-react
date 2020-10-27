import React, { FC } from "react";
import {
  Datagrid,
  EditButton,
  List,
  NumberField,
  TextField,
} from "react-admin";

export const ItemList: FC = (props) => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="title" />
      <TextField source="description" />
      <NumberField source="quantity" />
      <NumberField source="price" />
      <EditButton />
    </Datagrid>
  </List>
);
