import {React, useState, useEffect} from 'react'
import {Route} from 'react-router-dom'
import ProdList from '../components/List/ProdList'
import ShowProd from '../components/ItemList/ShowProd'
import ProdConnForm from '../components/Form/ProdConnForm';
import UpdateProdConn from '../components/Form/UpdateProdConn';
import UpdateProd from '../components/Form/UpdateProd'
import moment from 'moment'
import axiosConfig from '../actions/axiosConfig'

const ProdListContainer = ({match}) => {
  const [redirectDelete, setRedirectDelete]=useState(false)
  const [redirect, setRedirect]=useState(false)
  const [ProdData, setProd] = useState([]);
  const [newProd, setNewProd] =useState({
    name:'', 
    PPE:'', 
    dt_from:'', 
    dt_to:'',
    is_added:'',
    author:1, 
    modified_by:1,
    element_type:''
});

  useEffect(() => {
    const fetchData = async () => {
      const result = await axiosConfig.get(
        '/RB/powerplant/',
      );
      setProd(result.data);
    };
    setRedirectDelete(false)
     fetchData();
    
 
  }, [redirectDelete]);

  const deleteProd = (id, e) => {
    axiosConfig.delete(`/RB/powerplant/${id}/delete/`)
    // const elements = ProdData.filter(item => item.pk !== id);
    // setProd([...elements])
    .then(res => {
      if (res.status === 204) {
      setRedirectDelete(true)}})
     };

  const updateField = e => {
    setNewProd({...newProd, [e.target.name]: e.target.value})
    };

  const updateStartField = event => {
    setNewProd({...newProd, dt_from: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
    };

  const updateEndField = event => {
    setNewProd({...newProd, dt_to: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
    };

  const handleSubmit = (event) => {
    event.preventDefault();
    axiosConfig.put(`/RB/powerplant/${newProd.pk}/edit/`, newProd)
    .then(res => {
      if (res.status === 200) {
      setRedirect(true)}})   
};
  

    return (
      <div>
    <Route path={`${match.url}`} exact >
      <ProdList data={ProdData} />
    </Route>
    <Route path={`${match.url}/:id/show/`}><ShowProd 
    data={newProd}
    prev_match={match}
    setFunc={setNewProd}
    delFunc={deleteProd}
    redirectDelete={redirectDelete}
    />
    </Route>
    <Route path={`${match.url}/:id/edit/`}><UpdateProd 
    updateStartFunc={updateStartField}
    updateEndFunc={updateEndField}
    submitFunc={handleSubmit}
    UpdateFunc={updateField}
    setFunc={setNewProd}
    data={newProd}
    redirect={redirect}
    />
    </Route>
    <Route path={`${match.url}/:id/setup/new`}> 
    <ProdConnForm 
    data={newProd}/> </Route>
    <Route path={`${match.url}/:id/setup/edit`}> <UpdateProdConn data={newProd} /> </Route>
    
      </div>
)}


export default ProdListContainer