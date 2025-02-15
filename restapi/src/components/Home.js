import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../auth'
import recipes from './recipes'
import { Modal ,Form,Button} from 'react-bootstrap'
import { useForm } from 'react-hook-form'





const LoggedinHome = () => {
    const [recipess, setrecipess] = useState([]);
    const [show, setShow] = useState(false)
    const {register,reset,handleSubmit,setValue,formState:{errors}}=useForm()
    const [recipesId,setrecipesId]=useState(0);

    useEffect(
        () => {
            fetch('/recipes/recipess')
                .then(res => res.json())
                .then(data => {
                    setrecipess(data)
                })
                .catch(err => console.log(err))
        }, []
    );

    const getAllrecipess=()=>{
        fetch('/recipes/recipess')
        .then(res => res.json())
        .then(data => {
            setrecipess(data)
        })
        .catch(err => console.log(err))
    }
    

    const closeModal = () => {
        setShow(false)
    }

    const showModal = (id) => {
        setShow(true)
        setrecipesId(id)
        recipess.map(
            (recipes)=>{
                if(recipes.id==id){
                    setValue('title',recipes.title)
                    setValue('description',recipes.description)
                }
            }
        )
    }


    let token=localStorage.getItem('REACT_TOKEN_AUTH_KEY')

    const updaterecipes=(data)=>{
        console.log(data)

        

        const requestOptions={
            method:'PUT',
            headers:{
                'content-type':'application/json',
                'Authorization':`Bearer ${JSON.parse(token)}`
            },
            body:JSON.stringify(data)
        }


        fetch(`/recipes/recipes/${recipesId}`,requestOptions)
        .then(res=>res.json())
        .then(data=>{
            console.log(data)

            const reload =window.location.reload()
            reload() 
        })
        .catch(err=>console.log(err))
    }



    const deleterecipes=(id)=>{
        console.log(id)
        

        const requestOptions={
            method:'DELETE',
            headers:{
                'content-type':'application/json',
                'Authorization':`Bearer ${JSON.parse(token)}`
            }
        }


        fetch(`/recipes/recipes/${id}`,requestOptions)
        .then(res=>res.json())
        .then(data=>{
            console.log(data)
            getAllrecipess()
        
        })
        .catch(err=>console.log(err))
    }




    return (
        <div className="recipess container">
            <Modal
                show={show}
                size="lg"
                onHide={closeModal}
            >
                <Modal.Header closeButton>
                    <Modal.Title>
                        Update recipes
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form>
                        <Form.Group>
                            <Form.Label>Title</Form.Label>
                            <Form.Control type="text"
                                {...register('title', { required: true, maxLength: 25 })}
                            />
                        </Form.Group>
                        {errors.title && <p style={{ color: 'red' }}><small>Title is required</small></p>}
                        {errors.title?.type === "maxLength" && <p style={{ color: 'red' }}>
                            <small>Title should be less than 25 characters</small>
                        </p>}
                        <Form.Group>
                            <Form.Label>Description</Form.Label>
                            <Form.Control as="textarea" rows={5}
                                {...register('description', { required: true, maxLength: 255 })}
                            />
                        </Form.Group>
                        {errors.description && <p style={{ color: 'red' }}><small>Description is required</small></p>}
                        {errors.description?.type === "maxLength" && <p style={{ color: 'red' }}>
                            <small>Description should be less than 255 characters</small>
                        </p>}
                        <br></br>
                        <Form.Group>
                            <Button variant="primary" onClick={handleSubmit(updaterecipes)}>
                                Save
                            </Button>
                        </Form.Group>
                    </form>
                </Modal.Body>
            </Modal>
            <h1>List of recipess</h1>
            {
                recipess.map(
                    (recipes,index) => (
                        <recipes
                             title={recipes.title}
                            key={index}
                            description={recipes.description}
                            onClick={()=>{showModal(recipes.id)}}

                            onDelete={()=>{deleterecipes(recipes.id)}}

                        />
                    )
                )
            }
        </div>
    )
}


const LoggedOutHome = () => {
    return (
        <div className="home container">
            <h1 className="heading">Welcome to the recipess</h1>
            <Link to='/signup' className="btn btn-primary btn-lg">Get Started</Link>
        </div>
    )
}

const HomePage = () => {

    const [logged] = useAuth()

    return (
        <div>
            {logged ? <LoggedinHome /> : <LoggedOutHome />}
        </div>
    )
}

export default HomePage