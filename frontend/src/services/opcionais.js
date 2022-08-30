import api from './api'


  const getAll = () => {
    return api().get("/api/opcional");
  };
  
  
  export const opcionalService = {
    getAll
  };