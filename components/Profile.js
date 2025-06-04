import React from 'react';
import { useStateValue } from './StateManagement';

const Profile = () => {
    const { state } = useStateValue();

    return (
        <div>
            <h1>Profile</h1>
            <p>Email: {state.user?.email}</p>
        </div>
    );
};

export default Profile;
