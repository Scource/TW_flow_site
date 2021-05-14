import React from 'react'
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/esm/Button';
import {Link} from 'react-router-dom';
import moment from 'moment';
import { withRouter } from "react-router";


function ProdList(props) {

    return (
        <Table bordered hover size="sm">
        <thead>
            <tr>
            <th>ID</th>
            <th>Nazwa</th>
            <th>PPE</th>
            <th>POB</th>
            <th>Typ</th>
            <th>Data od</th>
            <th>Data do</th>
            </tr>
        </thead>
        <tbody>
            {props.data.map(pp => (
            <tr key={pp.pk}>
            <td>{pp.pk}</td>
            <td>{pp.name}</td>
            <td>{pp.PPE}</td>
            <td>{pp.POB}</td>            
            <td>{pp.element_type===0 ? "Wytwórca" 
                : props.data.element_type ===1 ? "Mikroinstalacja" : "Prosument"}</td>
            <td>{moment(pp.dt_from).format('YYYY-MM-DD HH:mm')}</td>
            <td>{moment(pp.dt_to).format('YYYY-MM-DD HH:mm')}</td>
            <td style={{width: '80px'}}><Link to={`${props.match.url}/${pp.pk}/show`}><Button>Pokaż</Button></Link>
            </td>
            </tr>))}
        </tbody>
        </Table>
    
    )}

export default withRouter(ProdList)