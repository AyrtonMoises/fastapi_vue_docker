import api from './api'


  const getAll = () => {
    return api().get("/api/status");
  };
  
  
  export const statusService = {
    getAll
  };