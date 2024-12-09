import axios from 'axios';

const api = axios.create({
    baseURL: 'http://yourapi.com/api', // Adjust this 
});

export const fetchComponentInfo = async (componentType, id) => {
    return api.get(`/${componentType}/info?${componentType}id=${id}`);
};

export const createComponent = async (componentType, data) => {
    return api.post(`/${componentType}/info`, data);
};

export const updateComponent = async (componentType, id, data) => {
    return api.put(`/${componentType}/info`, { ...data, [`${componentType}id`]: id });
};

export const deleteComponent = async (componentType, id) => {
    return api.delete(`/${componentType}/info`, { data: { [`${componentType}id`]: id } });
};

export const loginUser = async (username, password) => {
    return api.post('/login', { username, password });
};

export const logoutUser = async (usertoken) => {
    return api.post('/logout', { usertoken });
};
