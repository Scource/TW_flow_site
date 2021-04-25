import {React, useEffect, useState, Fragment} from 'react'
import Table from 'react-bootstrap/Table';
import { Collapse } from 'reactstrap';
import Button from 'react-bootstrap/esm/Button';
import moment from 'moment'
import axios from 'axios'
import { withRouter } from "react-router";



const  ProdConnections = (props) => {

    const [isOpen, setIsOpen] = useState(false);
    const [ProdData, setProd] = useState([]);
    const [showEdit, setshowEdit] = useState(false);


    useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get(
        'http://localhost:8000/RB/powerplant/connection/',
      );
      setProd(result.data);
    };
     fetchData();
 
  }, []);
    console.log(ProdData)
    return (
    <Fragment>

        <h5>Historia konfiguracji handlowej<Button
        onClick={() => setIsOpen(!isOpen)}>Pokaż</Button></h5>
      <Collapse isOpen={isOpen}>
        { showEdit ? '<Results />' : null }
        <Table hover size="sm">
        <thead>
            <tr>
            <th>POB</th>
            <th>Data od</th>
            <th>Data do</th>
            <th>Typ</th>
            </tr>
        </thead>
        <tbody>
            
            {ProdData.map(prod => (
            <tr key={prod.pk}>
            <td>{prod.POB_code}</td>
            <td>{moment(prod.dt_from).format('YYYY-MM-DD HH:mm')}</td>
            <td>{moment(prod.dt_to).format('YYYY-MM-DD HH:mm')}</td>
            <td> {{ 0: 'Wytwórca',
                    1: 'Mikroinstalacja',
                    2: 'Prosument'
                    }[prod.element_type]
                    }</td>
            <td style={{width: '150px'}}><Button onClick={() => setshowEdit(prevshowEdit => !prevshowEdit)}>Edytuj</Button>
            <Button onClick={() => props.delFunc(prod.pk)}>Usuń</Button> </td>
           </tr>
            
            ))}
            
        
        </tbody> 
        </Table>
        </Collapse>
    </Fragment>
    
    )}

export default withRouter(ProdConnections)