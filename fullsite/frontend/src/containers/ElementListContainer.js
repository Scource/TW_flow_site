import {React, useState, useEffect} from 'react'
import {Route} from 'react-router-dom'
import ElementList from '../components/List/ElementList'
import UpdateElement from '../components/Form/UpdateElement'
import ShowElement from '../components/ItemList/ShowElement'
import moment from 'moment'
import axiosConfig from '../actions/axiosConfig'

const ElementListContainer = ({match}) => {
  const [redirectDelete, setRedirectDelete]=useState(false)
  const [redirect, setRedirect]=useState(false)
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

  useEffect(() => {
    const fetchData = async () => {
      const result = await axiosConfig.get(
        `/RB${match.path}/`,
      );
      setElement(result.data);
    };
    setRedirectDelete(false)
    fetchData();
    
  }, [match.path, redirectDelete]);


  const deleteElement = (id, e) => {
    axiosConfig.delete(`/RB/element/${id}/delete/`)
    // const elements = ElementData.filter(item => item.pk !== id);
    // setElement([...elements])
        .then(res => {
                if (res.status === 204) {
          setRedirectDelete(true)}})
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
    axiosConfig.put(`/RB/element/${newElement.pk}/edit/`, newElement)
    .then(res => {
      if (res.status === 200) {
      setRedirect(true)}})   
};
  

    return (
      <div>
    <Route path={`${match.url}`} exact >
      <ElementList data={ElementData} />
    </Route>
    <Route path={`${match.url}/:id/show/`}><ShowElement 
    setFunc={setNewElement}
    delFunc ={deleteElement}
    data={newElement}
    prev_match={match}
    redirectDelete={redirectDelete}
    />
    </Route>
        <Route path={`${match.url}/:id/edit/`}><UpdateElement 
    updateStartFunc={updateStartField}
    updateEndFunc={updateEndField}
    submitFunc={handleSubmit}
    UpdateFunc={updateField}
    setFunc={setNewElement}
    
    data={newElement}
    redirect={redirect}
    />
    </Route>

    
      </div>
)}


export default ElementListContainer