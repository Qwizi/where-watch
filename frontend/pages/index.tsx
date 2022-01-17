import axios from 'axios'
import type { NextPage } from 'next'
import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'
import { Button, Card, Col, Form, ListGroup, Nav, Row, Tab } from 'react-bootstrap'

const CardLink = (props: any) => {
  const {data} = props;

    const linkList = data.map((data: any, i: number) => 

          <ListGroup.Item>
            <Card.Link href={data.url} target="_blank">{data.url}</Card.Link>
          </ListGroup.Item>
        )

  return linkList;
  
}

const ResultCardList = (props: any) => {
  const {data} = props;
  if (data) {
    const listData = data.map((data: any, i: number) =>
      <Card style={{marginBottom: "25px"}}>
        <Card.Header>{data.name}</Card.Header>
        <Card.Body>
          <ListGroup variant="flush">
            <CardLink data={data.data}/>
          </ListGroup>
        </Card.Body>
      </Card>
    );
    return listData
  }
  
}



const Home: NextPage = () => {
  const [searchInput, setSearchInput] = useState("")
  const [data, setData] = useState([])
  const router = useRouter()

  useEffect(() => {
    if(!router.isReady) return;
    if (router?.query?.title) {
      fetch(router.query.title)
    }
    
  }, [router.isReady])

  useEffect(() => {
    if (router?.query?.title) {
      fetch(router.query.title)
    }
    
  }, [router.query])

  const fetch = async (title) => {
    
    if (title) {
      console.log("Pobieram dane")
      const response = await axios.get(`http://localhost:8000/search?title=${title}`)
      setData([])
      setData(response.data)
      console.log(response.data)
    }
    
  }

  const onFormSubmit = async (e: any) => {
    e.preventDefault()
    //const response = await axios.get(`http://localhost:8000/search?title=${searchInput}`)
    //setData(response.data)
    router.push({
      pathname: "/",
      query: {
        title: searchInput
      }
    }, undefined, {shallow: true})
  }

  return (
    <div style={{display: "flex", justifyContent: "center", marginTop: "100px", flexDirection: "column"}}>
      <Row>
        <Col>
        <h1>Co chcesz dzisiaj wyszukac?</h1>
        </Col>
      </Row>
      <Row>
        <Col style={{textAlign: "center"}}>
          <Form onSubmit={onFormSubmit}>
            <Form.Group>
              <Form.Control 
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
              ></Form.Control>
            </Form.Group>

            <Button variant="primary" type="submit" style={{marginTop: "10px"}}>
              Wyszukaj
            </Button>
          </Form>
        </Col>
      </Row>
      {data && data.length > 0 &&  (
      <Row style={{marginTop: "50px"}}>
        <Col>
            <ResultCardList data={data}/>
        </Col>
      </Row>
      )}
    </div>
  )
}

export default Home
