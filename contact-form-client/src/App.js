import './App.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from 'axios';
import React, { useState } from 'react';

function App() {
  const [contact, setContact] = useState({
    name: '',
    email: '',
    message: ''
  });

  const handleChange = (e) => {
    const{ name, value } = e.target;
    setContact((prev) =>({
      ...prev,
      [name]: value
    }));
  };

  const handleSendMsg = async (e) => {
    e.preventDefault();

    try{
      const response = await axios.post('http://localhost:8000/sendMsg', contact);
      console.log(response.data);
    } catch(error) {
      console.error(error);
    }

    setContact({name: '', email: '', message: ''});
  };

  return (
    <div className="container-fluid wrapper">
      <Form className="contact-form" onSubmit={handleSendMsg}>
        <h1 className="mb-3">Contact Us</h1>
        
        <Form.Group className="mb-3" controlId="formName">
          <Form.Control type="text" name="name" value={contact.name} onChange={handleChange} placeholder="Name" autoComplete='off' />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formEmail">
          <Form.Control type="email" name="email" value={contact.email} onChange={handleChange} placeholder="Email" autoComplete='off' />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formDescription">
          <Form.Control as="textarea" name="message" value={contact.message} onChange={handleChange} rows={6} placeholder="Message" autoComplete='off' />
        </Form.Group>

        <Button className="form-submit" variant="primary" type="submit">
          Send Message
        </Button>
      </Form>
    </div>
  );
}

export default App;