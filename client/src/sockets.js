import io from 'socket.io-client';

export const socket = io('http://localhost:5000')
export const socket_notifications = io('/notifications')
export const socket_parsers = io('/parsers')
