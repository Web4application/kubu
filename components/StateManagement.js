import React, { createContext, useReducer, useContext } from 'react';

const initialState = {
    user: null,
    isAuthenticated: false,
};

const reducer = (state, action) => {
    switch (action.type) {
        case 'LOGIN':
            return { ...state, user: action.payload, isAuthenticated: true };
        case 'LOGOUT':
            return { ...state, user: null, isAuthenticated: false };
        default:
            return state;
    }
};

const StateContext = createContext();

export const StateProvider = ({ children }) => {
    const [state, dispatch] = useReducer(reducer, initialState);
    return (
        <StateContext.Provider value={{ state, dispatch }}>
            {children}
        </StateContext.Provider>
    );
};

export const useStateValue = () => useContext(StateContext);
