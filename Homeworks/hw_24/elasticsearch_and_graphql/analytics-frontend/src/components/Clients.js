import React from "react";
import {useQuery, gql} from '@apollo/client';

const GET_CLIENTS = gql`
  query {
    allClients {
        firstName
        lastName
        email
        isActive
        registeredAt
    }
}
`;
const Clients = () => {
    const {loading, error, data} = useQuery(GET_CLIENTS);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>Error: {error.message}</p>;
    }

    return (
        <div>
            <h1>Clients</h1>
            <ul>
                {data.allClients.map((client) => (
                    <li key={client.id}>
                        <h3>{client.firstName} {client.lastName}</h3>
                        <p>{client.email}</p>
                        <p>Is Active: {client.isActive}</p>
                        <p>Registered At: {client.registeredAt}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Clients;