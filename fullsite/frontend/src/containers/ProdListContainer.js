import {React, useState, useEffect} from 'react'
import axios from 'axios'
import {Route} from 'react-router-dom'
import ProdList from '../components/List/ProdList'
import ShowProd from '../components/ItemList/ShowProd'
import UpdateProd from '../components/Form/UpdateProd'
import moment from 'moment'


const ProdListContainer = ({match}) => {
  
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
  console.log(newProd)
  useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get(
        'http://localhost:8000/RB/powerplant/',
      );
      setProd(result.data);
    };
     fetchData();
 
  }, []);


  const deleteProd = (id, e) => {
    axios.delete(`http://localhost:8000/RB/powerplant/${id}/delete/`)
    const elements = ProdData.filter(item => item.pk !== id);
    setProd([...elements])
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
    axios.put(`http://localhost:8000/RB/powerplant/${newProd.pk}/edit/`, newProd)
    
};
  

    return (
      <div>
    <Route path={`${match.url}`} exact >
      <ProdList data={ProdData} delFunc={deleteProd} />
    </Route>
    <Route path={`${match.url}/:id/show/`}><ShowProd 
    data={newProd}
    prev_match={match}
    setFunc={setNewProd}

    />
    </Route>
        <Route path={`${match.url}/:id/edit/`}><UpdateProd 
    updateStartFunc={updateStartField}
    updateEndFunc={updateEndField}
    submitFunc={handleSubmit}
    UpdateFunc={updateField}
    setFunc={setNewProd}
    data={newProd}
    />
    </Route>

    
      </div>
)}


export default ProdListContainer