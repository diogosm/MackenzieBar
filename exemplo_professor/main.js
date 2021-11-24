let users = [];

const addUser = (e) => {
    e.preventDefault();
    let user = {
        Username: document.getElementById('username').value,
        Password: document.getElementById('password').value
    }
    users.push(user);
    document.forms[0].reset();

    console.warn('added', {
        users
    });

}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('btn').addEventListener('click', addUser)
})