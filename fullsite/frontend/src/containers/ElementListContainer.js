import {React, useState, useEffect} from 'react'
import axios from 'axios'
import {Route} from 'react-router-dom'
import ElementList from '../components/List/ElementList'
import UpdateElement from '../components/Form/UpdateElement'
import moment from 'moment'


const ElementListContainer = ({match}) => {

  const [ElementData, setElement] = useState([]);
  const [newElement, setNewElement] =useState({
    code:'', 
    name:'', 
    dt_from:'', 
    dt_to:'', 
    author:1, 
    modified_by:1,
    element_type:''
});
  
console.log(match)
  useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get(
        `http://localhost:8000/RB${match.path}/`,
      );
      setElement(result.data);
    };
     fetchData();
 
  }, [match.path]);


  const deleteElement = (id, e) => {
    axios.delete(`http://localhost:8000/RB/element/${id}/delete/`)
    const elements = ElementData.filter(item => item.pk !== id);
    setElement([...elements])
     };

  const updateField = e => {
    setNewElement({...newElement, [e.target.name]: e.target.value})
    };

  const updateStartField = event => {
    setNewElement({...newElement, dt_from: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
    };

  const updateEndField = event => {
    setNewElement({...newElement, dt_to: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
    };

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.put(`http://localhost:8000/RB/element/${newElement.pk}/edit/`, newElement)
    
    
};
  

    return (
      <div>
    <Route path={`${match.url}`} exact >
      <ElementList data={ElementData} delFunc={deleteElement} />
    </Route>
    <Route path={`${match.url}/edit/:id/`}><UpdateElement 
    updateStartFunc={updateStartField}
    updateEndFunc={updateEndField}
    submitFunc={handleSubmit}
    UpdateFunc={updateField}
    setFunc={setNewElement}
    data={newElement}
    />
    </Route>

    
      </div>
)}


export default ElementListContainer