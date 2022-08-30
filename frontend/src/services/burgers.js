import api from './api'


const getAll = () => {
    return api().get("/api/burger");
  };
  
  const get = id => {
    return api().get(`/api/burger/${id}/`);
  };
  
  const create = async data => {
    return api().post("/api/burger/", data);
  };
  
  const update = async (id, data) => {
    return api().patch(`/api/burger/${id}/`, data);
  };
  
  const remove = async id => {
    return api().delete(`/api/burger/${id}/`);
  };
  
  
  export const burgerService = {
    getAll,
    get,
    create,
    update,
    remove
  };