import {React, useEffect, useState, Fragment} from 'react'
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/esm/Button';
import moment from 'moment'
import { withRouter } from "react-router";
import {Link} from 'react-router-dom';
import axiosConfig from '../../actions/axiosConfig'

const  ProdConnections = (props) => {

    const [ProdData, setProd] = useState([]);

    useEffect(() => {
    const fetchData = async () => {
      const result = await axiosConfig.get(
        `/RB/powerplant/connection/${props.pp_id}/`,
      );
      setProd(result.data);
    };
     fetchData();
 
  }, [props.pp_id]);
     return (
    <Fragment>

        <h5>Historia konfiguracji handlowej</h5>
        <Table hover size="sm">
        <thead>
            <tr>
            <th>Id</th>
            <th>POB</th>
            <th>Data od</th>
            <th>Data do</th>
            <th>Typ</th>
            </tr>
        </thead>
        <tbody>
            
            {ProdData.map(prod => (
            <tr key={prod.pk}>
            <td>{prod.pk}</td>
            <td>{prod.POB_code}</td>
            <td>{moment(prod.dt_from).format('YYYY-MM-DD HH:mm')}</td>
            <td>{moment(prod.dt_to).format('YYYY-MM-DD HH:mm')}</td>
            <td> {{ 0: 'Wytwórca',
                    1: 'Mikroinstalacja',
                    2: 'Prosument'
                    }[prod.element_type]
                    }</td>
            <td style={{width: '80px'}}><Link to={`${props.prev_match.url}/${prod.pk}/setup/edit`}
                ><Button>Edytuj</Button></Link>
            </td>
           </tr>
            ))}

        
        </tbody> 
        </Table>

    </Fragment>
    
    )}

export default withRouter(ProdConnections)