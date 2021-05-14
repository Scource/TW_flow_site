import {React, useState, useEffect} from 'react'
import Datetime from "react-datetime";
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import moment from 'moment'
import { withRouter, Redirect } from "react-router";
import axiosConfig from '../../actions/axiosConfig'

function ProdForm() {

    const [redirect, setRedirect]=useState(false)
    const [ppData, setPpData] = useState([])
    const [postPp, setPostPp] = useState({
        name:'',
        PPE:'',
        POB:'',
        dt_from:'',
        dt_to:'',
        author:1,
        modified_by:1,
        is_added: false,
        element_type:''
    });

    useEffect(() => {
    const fetchData = async () => {
      const result = await axiosConfig.get(
        '/RB/element/POB/',
      );
      setPpData(result.data);
    };
     fetchData();
  }, []);

    const updateField = e => {
    setPostPp({...postPp, [e.target.name]: e.target.value})
    };

    const updateStartField = event => {
        setPostPp({...postPp, dt_from: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
    };

    const updateEndField = event => {
        setPostPp({...postPp, dt_to: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
    };

    const handleSubmit = event => {
    event.preventDefault();
    axiosConfig.post('/RB/powerplant/create/', postPp)
        .then(res => {
                if (res.status === 201) {
          setRedirect(true)}})
};

if (redirect) {
return <Redirect to="/producers" />
}

return(
    <Container>
       <h3>Utwórz nowego wytwórcę</h3>
       <br/>
        <Form>
            <Form.Row>
                <Form.Group as={Col} controlId="formProcName">            
                    <Form.Label>Nazwa wytwórcy</Form.Label>
                    <Form.Control onChange={updateField} name='name' type="text" placeholder="Podaj nazwę" />
                </Form.Group>
                <Form.Group as={Col} controlId="formProdCode">            
                    <Form.Label>Kod PPE</Form.Label>
                    <Form.Control onChange={updateField} name='PPE' type="text" placeholder="Podaj kod" />
                </Form.Group>
            </Form.Row>

            <Form.Row>
            <Form.Group as={Col} md={5} controlId="formProdSelectPOB">
                <Form.Label>Przypisz POB</Form.Label>
                <Form.Control onChange={updateField} name='POB' as="select" htmlSize={7} custom>
                  {ppData.filter(el => 
                        el.element_type === 0).map(ele => (
                        <option key={ele.pk} value={ele.pk}>{ele.code}</option>
                    ))}
                </Form.Control>
            </Form.Group>
            </Form.Row>

            <Form.Row>
                <Form.Group as={Col} controlId="formProdFromDate">            
                    <Form.Label>Data początku bilansowania</Form.Label>
                    <Datetime onChange={updateStartField} dateFormat="YYYY-MM-DD" timeFormat="HH:mm"/>
                </Form.Group>
                <Form.Group as={Col} controlId="formProdToDate">            
                    <Form.Label>Data końca bilansowania</Form.Label>
                    <Datetime onChange={updateEndField} dateFormat="YYYY-MM-DD" timeFormat="HH:mm"/>
                </Form.Group>
            </Form.Row>

            <Form.Row>
            <Form.Group  as={Col} md={4} controlId="formProdSelectType">
                <Form.Label>Wybierz typ</Form.Label>
                <Form.Control as="select" name='element_type' onChange={updateField}>
                <option>---wybierz typ---</option>
                <option value='0'>Wytwórca</option>
                <option value='1'>Mikroinstalacja</option>
                <option value='2'>Prosument</option>

                </Form.Control>
            </Form.Group>
            </Form.Row>
            <Form.Row>
                <Col md={{ span: 2, offset: 11 }}><Button onClick={handleSubmit} type="submit">Utwórz</Button></Col>
                
            </Form.Row>
        </Form>
    </Container>
    )
};


export default withRouter(ProdForm)