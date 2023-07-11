db.createUser({
    user: 'bot',
    pwd: 'password',
    roles: [
        {
            role: 'readWrite',
            db: 'bot_db',
        },
    ],
});
