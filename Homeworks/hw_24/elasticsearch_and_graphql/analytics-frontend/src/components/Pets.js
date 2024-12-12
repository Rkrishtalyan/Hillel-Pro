import React from "react";
import {useQuery, gql} from '@apollo/client';

const GET_PETS = gql`
  query {
    allPets {
        name
        species
        breed
        owner {
            firstName
            lastName
        }
    }
}
`;
const Pets = () => {
    const {loading, error, data} = useQuery(GET_PETS);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>Error: {error.message}</p>;
    }

    return (
        <div>
            <h1>Pets</h1>
            <ul>
                {data.allPets.map((pet) => (
                    <li key={pet.id}>
                        <h3>{pet.name}</h3>
                        <p>Species: {pet.species}</p>
                        <p>Breed {pet.breed}</p>
                        <p>Owner: {pet.owner.firstName} {pet.owner.lastName}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Pets;