import React from 'react'
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/esm/Button';
import {Link} from 'react-router-dom';
import moment from 'moment'
import { withRouter } from "react-router";

const ElementList = (props) => {
    return (
    <div>
        <h4>Lista użytkowników RB</h4>
            <Table bordered hover size="sm" >
        <thead>
            <tr>
            <th>ID</th>
            <th>Nazwa</th>
            <th>Kod</th>
            <th>Data od</th>
            <th>Data do</th>
            </tr>
        </thead>
        <tbody > 
            {props.data.map(ele => (
            <tr key={ele.pk}>
            <td>{ele.pk}</td>
            <td>{ele.name}</td>
            <td>{ele.code}</td>
            <td>{moment(ele.dt_from).format('YYYY-MM-DD HH:mm')}</td>
            <td>{moment(ele.dt_to).format('YYYY-MM-DD HH:mm')}</td>
            <td style={{width: '80px'}}><Link to={`${props.match.url}/${ele.pk}/show/`}><Button>Pokaż</Button></Link>
            </td>
            </tr>))}
        </tbody>
        </Table>
    </div>
    )}

export default withRouter(ElementList)