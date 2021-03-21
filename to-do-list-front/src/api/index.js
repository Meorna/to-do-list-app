import axios from 'axios';

export function authenticate(user) {
    var res = axios.post('http://0.0.0.0:5001/login', user)
    return res
}