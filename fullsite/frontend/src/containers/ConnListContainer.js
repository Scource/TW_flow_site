import React, { useState, useEffect } from 'react'
import axios from 'axios'
import {Route} from 'react-router-dom'
import ConnList from '../components/List/ConnList'
import UpdateConn from '../components/Form/UpdateConn'
import moment from 'moment'


const ConnListContainer = ({match}) => {

  const [connData, setConn] = useState([]);
  const [newConn, setNewConn] =useState({
      dt_from:'', 
      dt_to:'', 
      POB:'', 
      SE:'', 
      author:1, 
      modified_by:1 
  });
    useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get(
        'http://localhost:8000/RB/connection/',
      );
      console.log(result.data)
      setConn(result.data);

    };
     fetchData();
 
  }, []);
  
  const deleteConn = (id, e) => {
    axios.delete(`http://localhost:8000/RB/connection/${id}/delete/`)
    const newConn = connData.filter(item => item.pk !== id);
    setConn([...newConn])
     };

  const updateField = e => {
  setNewConn({...newConn, [e.target.name]: e.target.value})
  console.log(newConn)};

  const updateStartField = event => {
      setNewConn({...newConn, dt_from: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
      console.log(event)
  console.log(newConn)};

  const updateEndField = event => {
      setNewConn({...newConn, dt_to: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
  console.log(newConn)};

 const handleSubmit = (event) => {
    event.preventDefault();
    axios.put(`http://localhost:8000/RB/connection/${newConn.pk}/edit/`, newConn)
};



    return (
    <div>
    <Route path={`${match.url}`} exact >
      <ConnList data={connData} delFunc={deleteConn} />
    </Route>
    <Route path={`${match.url}/edit/:id/`}><UpdateConn 
    updateStartFunc={updateStartField}
    updateEndFunc={updateEndField}
    submitFunc={handleSubmit}
    UpdateFunc={updateField}
    setFunc={setNewConn}
    data={newConn}
    />
    </Route>
    </div>
    )

}


export default ConnListContainer