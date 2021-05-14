import {React, useEffect, useState, Fragment} from 'react'
import Table from 'react-bootstrap/Table';

import moment from 'moment'
import { withRouter} from "react-router";
import {Link} from 'react-router-dom';
import axiosConfig from '../../actions/axiosConfig'

const  ElementConnections = (props) => {

 
    const [ConnData, setConnData] = useState([]);

    useEffect(() => {
    const fetchData = async () => {
      const result = await axiosConfig.get(
        '/RB/connection/',
      );
      setConnData(result.data);
    };
     fetchData();
 
  }, []);
  


    return (
    <Fragment>

        <h5>Historia konfiguracji handlowej</h5>

        <Table hover size="sm">
        <thead>
            <tr>
            <th>POB</th>
            <th>SE</th>
            <th>Data od</th>
            <th>Data do</th>
            </tr>
        </thead>
        <tbody>
            
            {ConnData.filter(p => 
            (p.POB === props.pk || p.SE===props.pk)).map(conn => (
            <tr key={conn.pk}>
            <td>{conn.POB_code}</td>
            <td>{conn.SE_code}</td>
            <td>{moment(conn.dt_from).format('YYYY-MM-DD HH:mm')}</td>
            <td>{moment(conn.dt_to).format('YYYY-MM-DD HH:mm')}</td>
            <td style={{width: '80px'}}><Link to={`/connections/${conn.pk}/edit`} className="btn btn-primary">Edytuj</Link>
            </td></tr>
            ))}
            
        </tbody> 
        </Table>

    </Fragment>
    
    )}

export default withRouter(ElementConnections)