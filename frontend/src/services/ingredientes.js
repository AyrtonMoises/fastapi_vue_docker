import api from './api'


const getCarnesAll = () => {
    return api().get("/api/ingrediente/?tipo_ingrediente=C");
  };
  

const getPaesAll = () => {
    return api().get("/api/ingrediente/?tipo_ingrediente=P");
};

export const ingredienteService = {
    getCarnesAll,
    getPaesAll,
};