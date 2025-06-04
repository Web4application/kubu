import React from 'react';

const ErrorBoundary = ({ children }) => {
    return (
        <div>
            {children}
        </div>
    );
};

export default ErrorBoundary;
