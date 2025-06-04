import React, { useState } from 'react';
import { useStateValue } from './StateManagement';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { dispatch } = useStateValue();

    const handleSubmit = (e) => {
        e.preventDefault();
        // Perform login logic here
        dispatch({ type: 'LOGIN', payload: { email } });
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Email:
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            </label>
            <label>
                Password:
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </label>
            <button type="submit">Login</button>
        </form>
    );
};

export default Login;
