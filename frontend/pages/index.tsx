import axios from 'axios'
import type { NextPage } from 'next'
import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'
import { Button, Card, Col, Form, ListGroup, Nav, ProgressBar, Row, Tab } from 'react-bootstrap'
import { io, Socket} from 'socket.io-client'

function useSocket(url: string) {
  const [socket, setSocket] = useState<Socket | null>(null)

  useEffect(() => {
    const socketIo = io(url, {
			path: '/ws/socket.io'
		})

    setSocket(socketIo)

    function cleanup() {
      socketIo.disconnect()
    }
    return cleanup

    // should only run once and not on every re-render,
    // so pass an empty array
  }, [])

  return socket
}


const CardLink = (props: any) => {
  const {data} = props;

    const linkList = data.map((data: any, i: number) => 

          <ListGroup.Item key={i}>
            <Card.Link href={data.url} target="_blank">{data.url}</Card.Link>
          </ListGroup.Item>
        )

  return linkList;
  
}

const ResultCardList = (props: any) => {
  const {data} = props;
  if (data.length > 0) {
    const listData = data.map((data: any, i: number) =>
      <Card style={{marginBottom: "25px"}} key={i}>
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
  const [progress, setProgress] = useState<null | number>(null);
  const router = useRouter()
  const socket = useSocket("http://localhost:8006");

  useEffect(() => {
    if(!router.isReady) return;
    if (router?.query?.title) {
      fetch(router.query.title)
    }
    
  }, [router.isReady, router.query])

  useEffect(() => {
    if (socket) {
      console.log(socket)
      socket.on("connection", (event) => {
        console.log(socket)
        socket.emit('client_connected', { data: 'User connected' });
      })

      socket.on("search_data", (data) => {
        setData(data)
        setProgress(null)
      })
      socket.on("progress", (data) => {
        console.log(data)
        setProgress(data[0].progress)
      })
    }
  }, [socket])

  const fetch = async (title: any) => {
    
    if (title) {
      console.log("Pobieram dane")
      setData([])
      setProgress(null)
      //const url = process.env.API_URL || "https://apiwatch.jebzpapy.tk"
      //const response = await axios.get(`${url}/search?title=${title}`)
      //setData([])
      //setData(response.data)
      //console.log(response.data)
      socket?.emit("search", {title: title})
    }
    
  }

  const onFormSubmit = async (e: any) => {
    e.preventDefault()
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
      
      <Row style={{marginTop: "50px"}}>
        <Col>
        {progress && (
              <ProgressBar now={progress} label={`${progress}%`} />
          )}
          {data && data.length >= 1 &&  (
            <ResultCardList data={data}/>
          )}
        </Col>
      </Row>
      
    </div>
  )
}

export default Home
