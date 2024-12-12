import { ApolloClient, InMemoryCache, HttpLink } from "@apollo/client";

// Client for documents endpoint
export const documentsClient = new ApolloClient({
    link: new HttpLink({
        uri: "http://localhost:8000/documents/",
        fetchOptions: {
            method: "POST"
        },
    }),
    cache: new InMemoryCache()
});

// Client for clients endpoint
export const clientsClient = new ApolloClient({
    link: new HttpLink({
        uri: "http://localhost:8000/clients/",
        fetchOptions: {
            method: "POST"
        },
    }),
    cache: new InMemoryCache()
});

// Client for pets endpoint
export const petsClient = new ApolloClient({
    link: new HttpLink({
        uri: "http://localhost:8000/pets/",
        fetchOptions: {
            method: "POST"
        },
    }),
    cache: new InMemoryCache()
});
