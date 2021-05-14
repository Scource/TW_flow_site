import React from 'react'
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/esm/Button';
import {Link} from 'react-router-dom';
import moment from 'moment'
import { withRouter } from "react-router";

const  ConnList = (props) => {
    return (
        
        <div>
        <h4>Lista połączeń użytkowników RB</h4>
        <Table hover bordered size="sm">
        <thead>
            <tr>
            <th>ID</th>
            <th>POB</th>
            <th>SE</th>
            <th>Data od</th>
            <th>Data do</th>
            </tr>
        </thead>
        <tbody>
            {props.data.map(conn => (
            <tr key={conn.pk}>
            <td>{conn.pk}</td>
            <td>{conn.POB_code}</td>
            <td>{conn.SE_code}</td>
            <td>{moment(conn.dt_from).format('YYYY-MM-DD HH:mm')}</td>
            <td>{moment(conn.dt_to).format('YYYY-MM-DD HH:mm')}</td>
            <td style={{width: '80px'}}><Link to={`${props.match.url}/${conn.pk}/show/`}><Button>Pokaż</Button></Link>
            </td>
            </tr>))}
        </tbody> 
        </Table>
        </div>
    
    )}

export default withRouter(ConnList)