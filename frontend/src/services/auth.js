import api from './api'


const qs = require('qs');

export const loginJWT = (loginData) => {
    var data = qs.stringify(loginData);

    return api().post(
       '/api/token', data, { 
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }
      )
}