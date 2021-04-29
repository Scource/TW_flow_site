import {React, useEffect, useState, Fragment} from 'react'
import Table from 'react-bootstrap/Table';
import { Collapse } from 'reactstrap';
import Button from 'react-bootstrap/esm/Button';
import moment from 'moment'
import axios from 'axios'
import { withRouter} from "react-router";
import {Link} from 'react-router-dom';


const  ElementConnections = (props) => {

    const [isOpen, setIsOpen] = useState(false);
    const [ConnData, setConnData] = useState([]);

    useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get(
        'http://localhost:8000/RB/connection/',
      );
      setConnData(result.data);
    };
     fetchData();
 
  }, []);
  


    return (
    <Fragment>

        <h5>Historia konfiguracji handlowej<Button
        onClick={() => setIsOpen(!isOpen)}>Pokaż</Button></h5>
      <Collapse isOpen={isOpen}>

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
            <td style={{width: '150px'}}><Link to={`/connections/${conn.pk}/edit`} className="btn btn-primary">Edytuj</Link>
            </td>
           </tr>
            ))}
        </tbody> 
        </Table>
        </Collapse>
    </Fragment>
    
    )}

export default withRouter(ElementConnections)