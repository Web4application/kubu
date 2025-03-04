// import dotenv from 'dotenv';

dotenv.config();

const getRequiredEnv = (variable, defaultValue) => {
    const value = process.env[variable];
    if (!value && !defaultValue) {
        throw new Error(`Missing required environment variable: ${variable}`);
    }
    return value || defaultValue;
};

const config = {
    development: {
        apiUrl: getRequiredEnv('DEV_API_URL', 'http://localhost:3000/api'),
    },
    production: {
        apiUrl: getRequiredEnv('PROD_API_URL', 'https://mywebapp.com/api'),
    },
};

export default config;
