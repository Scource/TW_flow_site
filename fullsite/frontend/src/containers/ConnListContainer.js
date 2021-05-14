import React, { useState, useEffect} from 'react'
import {Route} from 'react-router-dom'
import ConnList from '../components/List/ConnList'
import UpdateConn from '../components/Form/UpdateConn'
import ShowConn from '../components/ItemList/ShowConn'
import moment from 'moment'
import axiosConfig from '../actions/axiosConfig'

const ConnListContainer = ({match}) => {
 
  const [redirectUpdate, setRedirectUpdate]=useState(false)
  const [redirectDelete, setRedirectDelete]=useState(false)
  const [redirect, setRedirect]=useState(false)
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
      const result = await axiosConfig.get(
        '/RB/connection/',
      );
      setConn(result.data);
    };
     fetchData();
    setRedirectDelete(false)
  }, [redirectUpdate, redirect, redirectDelete]);
  
  const deleteConn = (id, e) => {
    axiosConfig.delete(`/RB/connection/${id}/delete/`)    
    .then(res => {
                if (res.status === 204) {
          setRedirectDelete(true)}})
    // const newConn = connData.filter(item => item.pk !== id);
    // setConn([...newConn])

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
    axiosConfig.put(`/RB/connection/${newConn.pk}/edit/`, newConn)
      .then(res => {
                if (res.status === 200) {
          setRedirectUpdate(true)}})
};


    return (
    <div>
    <Route path={`${match.url}`} exact >
      <ConnList data={connData}  />
    </Route>
    <Route path={`${match.url}/:id/show/`}><ShowConn 
    data={newConn}
    prev_match={match}
    delFunc={deleteConn}
    setFunc={setNewConn}
    redirect={redirect}
    redirectDelete={redirectDelete}
    />
    </Route>
        <Route path={`${match.url}/:id/edit/`}><UpdateConn 
    redirectUpdate={redirectUpdate}
    setRedirect={setRedirect}
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