import axios from 'axios';

export async function APICall(endpoint) {
    const response = await axios.get(endpoint)
        .catch(function (error) {
            console.log(error);
        });
    return response?.data
}